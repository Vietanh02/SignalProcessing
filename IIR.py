import numpy as np
from scipy.signal import ellip, ellipord, sos2tf, tf2zpk
import matplotlib.pyplot as plt
from scipy.signal import (
    freqz,
    group_delay,
    butter,
    cheby1,
    cheby2,
    buttord,
    cheb1ord,
    cheb2ord,
)

pi = float(np.pi)
np.set_printoptions(precision=5, suppress=True)


def on_scroll(event):
    ax = event.inaxes
    if ax is None:
        return

    x, y = event.xdata, event.ydata
    xlim = ax.get_xlim()
    ylim = ax.get_ylim()

    # Zoom factor
    zoom_factor = 1.2

    if event.button == "up":
        ax.set_xlim(x - (x - xlim[0]) / zoom_factor, x + (xlim[1] - x) / zoom_factor)
        ax.set_ylim(y - (y - ylim[0]) / zoom_factor, y + (ylim[1] - y) / zoom_factor)
    elif event.button == "down":
        ax.set_xlim(x - (x - xlim[0]) * zoom_factor, x + (xlim[1] - x) * zoom_factor)
        ax.set_ylim(y - (y - ylim[0]) * zoom_factor, y + (ylim[1] - y) * zoom_factor)
    plt.draw()


def freqz_m(b, a):
    w, H = freqz(b, a, 1000, "whole")
    H = H[:501]
    w = w[:501]

    mag = np.abs(H)
    db = 20 * np.log10((mag + np.finfo(float).eps) / np.max(mag))
    pha = np.angle(np.conjugate(H))
    grd = group_delay((b, a), w)[1]

    return db, mag, pha, grd, w


def cplxpair(x, tol=100):
    """
    Sort complex numbers into complex conjugate pairs.

    This function replaces MATLAB's cplxpair for vectors.
    """
    x = np.array(x)
    x = np.atleast_1d(x.squeeze())
    x = x.tolist()
    x = [np.real_if_close(i, tol) for i in x]
    xreal = np.array(list(filter(np.isreal, x)))
    xcomplex = np.array(list(filter(np.iscomplex, x)))
    xreal = np.sort_complex(xreal)
    xcomplex = np.sort_complex(xcomplex)
    xcomplex_ipos = xcomplex[xcomplex.imag > 0.0]
    xcomplex_ineg = xcomplex[xcomplex.imag <= 0.0]
    if len(xcomplex_ipos) != len(xcomplex_ineg):
        raise ValueError("Complex numbers can't be paired.")
    res = []
    for i, j in zip(xcomplex_ipos, xcomplex_ineg):
        if not abs(i - np.conj(j)) < tol * np.finfo(float).eps:
            raise ValueError("Complex numbers can't be paired.")
        res += [j, i]
    return np.hstack((np.array(res), xreal))


def dir2cas(b, a):
    # Compute gain coefficient b0
    b0 = b[0]
    a0 = a[0]
    b = b / a0
    a = a / a0
    b0 = b0 / a0

    M = len(b)
    N = len(a)

    if N > M:
        b = np.concatenate((b, np.zeros(N - M)))
    elif M > N:
        a = np.concatenate((a, np.zeros(M - N)))
        N = M

    K = N // 2
    B = np.zeros((K, 3))
    A = np.zeros((K, 3))

    if K * 2 == N:
        b = np.concatenate((b, [0]))
        a = np.concatenate((a, [0]))

    broots = cplxpair(np.roots(b))
    aroots = cplxpair(np.roots(a))

    for i in range(0, 2 * K, 2):
        Brow = broots[i : i + 2]
        Brow = np.real(np.poly(Brow))
        B[i // 2, :] = Brow

        Arow = aroots[i : i + 2]
        Arow = np.real(np.poly(Arow))
        A[i // 2, :] = Arow

    return b0, B, A


def lowpass(wp, ws, Rp, As, cuaso):
    T = 1
    OmegaP = (2 / T) * np.tan(wp * pi / 2)
    OmegaS = (2 / T) * np.tan(ws * pi / 2)
    ep = np.sqrt(10 ** (Rp / 10) - 1)
    Ripple = np.sqrt(1 / (1 + ep * ep))
    Attn = 1 / (10 ** (As / 20))
    N = np.ceil(
        (np.log10((10 ** (Rp / 10) - 1) / (10 ** (As / 10) - 1)))
        / (2 * np.log10(OmegaP / OmegaS))
    )
    OmegaC = OmegaP / ((10 ** (Rp / 10) - 1) ** (1 / (2 * N)))
    wn = 2 * np.arctan((OmegaC * T) / 2)
    wn = wn / pi
    # cuaso
    if cuaso == "Butterworth":
        b, a = butter(N, wn)
    elif cuaso == "Chebyshev 1":
        b, a = cheby1(N, Rp, wn)
    elif cuaso == "Chebyshev 2":
        b, a = cheby2(N, As, wn)
    elif cuaso == "Elliptic":
        b, a = ellip(N, Rp, As, wn)
    return b, a, N, Ripple, Attn


def lowpassDraw(wp, ws, Rp, As, cuaso):
    b, a, N, Ripple, Attn = lowpass(wp, ws, Rp, As, cuaso)
    b0, B, A = dir2cas(b, a)
    # Convert filter to second-order sections
    [db, mag, pha, grd, w] = freqz_m(b, a)

    # Plot frequency response
    fig, axs = plt.subplots(2, 2, figsize=(8, 8))
    fig.set_size_inches(10, 6)
    fig.suptitle(f"{cuaso} Filter Order = {N}", fontsize=16)
    for ax in axs:
        fig.canvas.mpl_connect("scroll_event", on_scroll)
    xtickLabel = [
        np.min(w / np.pi),
        wp,
        ws,
        np.max(w / np.pi),
    ]
    plt.subplot(2, 2, 1)
    plt.plot(w / np.pi, mag)
    plt.grid(True)
    plt.title("Magnitude Response")
    plt.xlabel("Frequency in pi units")
    plt.axis(
        [
            int(np.min(w / np.pi) + 0.5) * 1.2,
            int(np.max(w / np.pi) + 0.5) * 1.2,
            int(np.min(mag) + 0.5) * 1.2,
            int(np.max(mag) + 0.5) * 1.2,
        ]
    )
    plt.xticks(xtickLabel)
    plt.yticks([np.min(mag), Attn, Ripple, np.max(mag)])

    # Subplot 2: Magnitude in dB
    plt.subplot(2, 2, 3)
    plt.plot(w / np.pi, db)
    plt.grid(True)
    plt.title("Magnitude in dB")
    plt.xlabel("Frequency in pi units")
    plt.ylabel("dB")
    plt.axis(
        [
            int(np.min(w / np.pi) + 0.5) * 1.2,
            int(np.max(w / np.pi) + 0.5) * 1.2,
            int(np.min(db) + 0.5) * 1.2,
            int(np.max(db) + 0.5) * 1.2,
        ]
    )
    plt.xticks(xtickLabel)
    plt.yticks([-As, 0])

    # Subplot 3: Phase Response
    plt.subplot(2, 2, 2)
    plt.plot(w / np.pi, pha / np.pi)
    plt.grid(True)
    plt.title("Phase Response")
    plt.xlabel("Frequency in pi units")
    plt.ylabel("Phase in pi units")
    plt.xticks(xtickLabel)

    # Subplot 4: Group Delay
    plt.subplot(2, 2, 4)
    plt.plot(w / np.pi, grd)
    plt.grid(True)
    plt.title("Group Delay")
    plt.xlabel("Frequency in pi units")
    plt.ylabel("Samples")
    plt.xticks(xtickLabel)

    plt.tight_layout()
    plt.show()


def bandpass(wp, ws, Rp, As, cuaso):
    T = 1
    ep = np.sqrt(10 ** (Rp / 10) - 1)
    Ripple = np.sqrt(1 / (1 + ep * ep))
    Attn = 1 / (10 ** (As / 20))
    # cuaso
    if cuaso == "Butterworth":
        N, wn = buttord(wp, ws, Rp, As, analog=False)
        b, a = butter(N, wn, analog=False, output="ba", btype="bandpass")
    elif cuaso == "Chebyshev 1":
        N, wn = cheb1ord(wp, ws, Rp, As, analog=False)
        b, a = cheby1(N, Rp, wn, analog=False, output="ba", btype="bandpass")
    elif cuaso == "Chebyshev 2":
        N, wn = cheb2ord(wp, ws, Rp, As, analog=False)
        b, a = cheby2(N, As, wn, analog=False, output="ba", btype="bandpass")
    elif cuaso == "Elliptic":
        N, wn = ellipord(wp, ws, Rp, As, analog=False)
        b, a = ellip(N, Rp, As, wn, analog=False, output="ba", btype="bandpass")
    return b, a, N, Ripple, Attn


def bandpassDraw(wp, ws, Rp, As, cuaso):
    b, a, N, Ripple, Attn = bandpass(wp, ws, Rp, As, cuaso)
    b0, B, A = dir2cas(b, a)
    # Convert filter to second-order sections
    [db, mag, pha, grd, w] = freqz_m(b, a)
    # Plot frequency response
    fig, axs = plt.subplots(2, 2, figsize=(8, 8))
    fig.set_size_inches(10, 6)
    fig.suptitle(f"{cuaso} Filter Order = {N}", fontsize=16)
    for ax in axs:
        fig.canvas.mpl_connect("scroll_event", on_scroll)
    xtickLabel = np.concatenate(
        (
            [np.min(w / np.pi)],
            wp,
            ws,
            [np.max(w / np.pi)],
        )
    )
    plt.subplot(2, 2, 1)
    plt.plot(w / np.pi, mag)
    plt.grid(True)
    plt.title("Magnitude Response")
    plt.xlabel("Frequency in pi units")
    plt.axis(
        [
            int(np.min(w / np.pi) + 0.5) * 1.2,
            int(np.max(w / np.pi) + 0.5) * 1.2,
            int(np.min(mag) + 0.5) * 1.2,
            int(np.max(mag) + 0.5) * 1.2,
        ]
    )
    plt.xticks(xtickLabel)
    plt.yticks([np.min(mag), Attn, Ripple, np.max(mag)])

    # Subplot 2: Magnitude in dB
    plt.subplot(2, 2, 3)
    plt.plot(w / np.pi, db)
    plt.grid(True)
    plt.title("Magnitude in dB")
    plt.xlabel("Frequency in pi units")
    plt.ylabel("dB")
    plt.axis(
        [
            int(np.min(w / np.pi) + 0.5) * 1.2,
            int(np.max(w / np.pi) + 0.5) * 1.2,
            int(np.min(db) + 0.5) * 1.2,
            int(np.max(db) + 0.5) * 1.2,
        ]
    )
    plt.xticks(xtickLabel)
    plt.yticks([-As, 0])

    # Subplot 3: Phase Response
    plt.subplot(2, 2, 2)
    plt.plot(w / np.pi, pha / np.pi)
    plt.grid(True)
    plt.title("Phase Response")
    plt.xlabel("Frequency in pi units")
    plt.ylabel("Phase in pi units")
    plt.xticks(xtickLabel)

    # Subplot 4: Group Delay
    plt.subplot(2, 2, 4)
    plt.plot(w / np.pi, grd)
    plt.grid(True)
    plt.title("Group Delay")
    plt.xlabel("Frequency in pi units")
    plt.ylabel("Samples")
    plt.xticks(xtickLabel)

    plt.tight_layout()
    plt.show()


def highpass(wp, ws, Rp, As, cuaso):
    T = 1
    ep = np.sqrt(10 ** (Rp / 10) - 1)
    Ripple = np.sqrt(1 / (1 + ep * ep))
    Attn = 1 / (10 ** (As / 20))
    # cuaso
    if cuaso == "Butterworth":
        N, wn = buttord(wp, ws, Rp, As, analog=False)
        b, a = butter(N, wn, analog=False, output="ba", btype="highpass")
    elif cuaso == "Chebyshev 1":
        N, wn = cheb1ord(wp, ws, Rp, As, analog=False)
        b, a = cheby1(N, Rp, wn, analog=False, output="ba", btype="highpass")
    elif cuaso == "Chebyshev 2":
        N, wn = cheb2ord(wp, ws, Rp, As, analog=False)
        b, a = cheby2(N, As, wn, output="ba", btype="highpass")
    elif cuaso == "Elliptic":
        N, wn = ellipord(wp, ws, Rp, As, analog=False)
        b, a = ellip(N, Rp, As, wn, output="ba", btype="highpass")
    return b, a, N, Ripple, Attn


def highpassDraw(wp, ws, Rp, As, cuaso):
    b, a, N, Ripple, Attn = highpass(wp, ws, Rp, As, cuaso)
    b0, B, A = dir2cas(b, a)
    # Convert filter to second-order sections
    [db, mag, pha, grd, w] = freqz_m(b, a)

    # Plot frequency response
    fig, axs = plt.subplots(2, 2, figsize=(8, 8))
    fig.set_size_inches(10, 6)
    fig.suptitle(f"{cuaso} Filter Order = {N}", fontsize=16)
    for ax in axs:
        fig.canvas.mpl_connect("scroll_event", on_scroll)
    xtickLabel = [
        np.min(w / np.pi),
        wp,
        ws,
        np.max(w / np.pi),
    ]
    plt.subplot(2, 2, 1)
    plt.plot(w / np.pi, mag)
    plt.grid(True)
    plt.title("Magnitude Response")
    plt.xlabel("Frequency in pi units")
    plt.axis(
        [
            int(np.min(w / np.pi) + 0.5) * 1.2,
            int(np.max(w / np.pi) + 0.5) * 1.2,
            int(np.min(mag) + 0.5) * 1.2,
            int(np.max(mag) + 0.5) * 1.2,
        ]
    )
    plt.xticks(xtickLabel)
    plt.yticks([np.min(mag), Attn, Ripple, np.max(mag)])

    # Subplot 2: Magnitude in dB
    plt.subplot(2, 2, 3)
    plt.plot(w / np.pi, db)
    plt.grid(True)
    plt.title("Magnitude in dB")
    plt.xlabel("Frequency in pi units")
    plt.ylabel("dB")
    plt.axis(
        [
            int(np.min(w / np.pi) + 0.5) * 1.2,
            int(np.max(w / np.pi) + 0.5) * 1.2,
            int(np.min(db) + 0.5) * 1.2,
            int(np.max(db) + 0.5) * 1.2,
        ]
    )
    plt.xticks(xtickLabel)
    plt.yticks([-As, 0])

    # Subplot 3: Phase Response
    plt.subplot(2, 2, 2)
    plt.plot(w / np.pi, pha / np.pi)
    plt.grid(True)
    plt.title("Phase Response")
    plt.xlabel("Frequency in pi units")
    plt.ylabel("Phase in pi units")
    plt.xticks(xtickLabel)

    # Subplot 4: Group Delay
    plt.subplot(2, 2, 4)
    plt.plot(w / np.pi, grd)
    plt.grid(True)
    plt.title("Group Delay")
    plt.xlabel("Frequency in pi units")
    plt.ylabel("Samples")
    plt.xticks(xtickLabel)

    plt.tight_layout()
    plt.show()


def bandstop(wp, ws, Rp, As, cuaso):
    T = 1
    ep = np.sqrt(10 ** (Rp / 10) - 1)
    Ripple = np.sqrt(1 / (1 + ep * ep))
    Attn = 1 / (10 ** (As / 20))
    # cuaso
    if cuaso == "Butterworth":
        N, wn = buttord(wp, ws, Rp, As, analog=False)
        b, a = butter(N, wn, analog=False, output="ba", btype="bandstop")
    elif cuaso == "Chebyshev 1":
        N, wn = cheb1ord(wp, ws, Rp, As, analog=False)
        b, a = cheby1(N, Rp, wn, analog=False, output="ba", btype="bandstop")
    elif cuaso == "Chebyshev 2":
        N, wn = cheb2ord(wp, ws, Rp, As, analog=False)
        b, a = cheby2(N, As, wn, analog=False, output="ba", btype="bandstop")
    elif cuaso == "Elliptic":
        N, wn = ellipord(wp, ws, Rp, As, analog=False)
        b, a = ellip(N, Rp, As, wn, analog=False, output="ba", btype="bandstop")
    return b, a, N, Ripple, Attn


def bandstopDraw(wp, ws, Rp, As, cuaso):
    b, a, N, Ripple, Attn = bandstop(wp, ws, Rp, As, cuaso)
    b0, B, A = dir2cas(b, a)
    # Convert filter to second-order sections
    [db, mag, pha, grd, w] = freqz_m(b, a)
    # Plot frequency response
    fig, axs = plt.subplots(2, 2, figsize=(8, 8))
    fig.set_size_inches(10, 6)
    fig.suptitle(f"{cuaso} Filter Order = {N}", fontsize=16)
    for ax in axs:
        fig.canvas.mpl_connect("scroll_event", on_scroll)
    xtickLabel = np.concatenate(
        (
            [np.min(w / np.pi)],
            wp,
            ws,
            [np.max(w / np.pi)],
        )
    )
    plt.subplot(2, 2, 1)
    plt.plot(w / np.pi, mag)
    plt.grid(True)
    plt.title("Magnitude Response")
    plt.xlabel("Frequency in pi units")
    plt.axis(
        [
            int(np.min(w / np.pi) + 0.5) * 1.2,
            int(np.max(w / np.pi) + 0.5) * 1.2,
            int(np.min(mag) + 0.5) * 1.2,
            int(np.max(mag) + 0.5) * 1.2,
        ]
    )
    plt.xticks(xtickLabel)
    plt.yticks([np.min(mag), Attn, Ripple, np.max(mag)])

    # Subplot 2: Magnitude in dB
    plt.subplot(2, 2, 3)
    plt.plot(w / np.pi, db)
    plt.grid(True)
    plt.title("Magnitude in dB")
    plt.xlabel("Frequency in pi units")
    plt.ylabel("dB")
    plt.axis(
        [
            int(np.min(w / np.pi) + 0.5) * 1.2,
            int(np.max(w / np.pi) + 0.5) * 1.2,
            int(np.min(db) + 0.5) * 1.2,
            int(np.max(db) + 0.5) * 1.2,
        ]
    )
    plt.xticks(xtickLabel)
    plt.yticks([-As, 0])

    # Subplot 3: Phase Response
    plt.subplot(2, 2, 2)
    plt.plot(w / np.pi, pha / np.pi)
    plt.grid(True)
    plt.title("Phase Response")
    plt.xlabel("Frequency in pi units")
    plt.ylabel("Phase in pi units")
    plt.xticks(xtickLabel)

    # Subplot 4: Group Delay
    plt.subplot(2, 2, 4)
    plt.plot(w / np.pi, grd)
    plt.grid(True)
    plt.title("Group Delay")
    plt.xlabel("Frequency in pi units")
    plt.ylabel("Samples")
    plt.xticks(xtickLabel)

    plt.tight_layout()
    plt.show()
