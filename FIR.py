import numpy as np
import matplotlib.pyplot as plt
from numpy import blackman, bartlett
from scipy.signal import freqz, group_delay, firwin2
from scipy.fft import ifft, fft

# setting
np.set_printoptions(precision=6, suppress=True)
# pre val
windown = [
    ["Chữ nhật", 21],
    ["Barlett", 25],
    ["Hanning", 44],
    ["Hamming", 53],
    ["BlackMan", 74],
]


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


def thongthap(wp, ws, As):
    np.set_printoptions(precision=4, suppress=True)
    pi = np.pi
    wp = wp * pi
    ws = ws * pi
    tr_width = ws - wp  # Transition width
    # Assuming pi and eps have been defined previously
    for i in windown:
        if i[1] > As:
            cuaso = i
            break

    # Generate a Hamming window of length M
    if cuaso[0] == "Chữ nhật":
        # Calculate the filter length (M) using the formula
        M = int(np.ceil(1.8 * pi / tr_width)) + 1
        # Ensure M is an odd number
        if M % 2 != 1:
            M = M - 1
        w_use = np.ones(M)
    elif cuaso[0] == "Barlett":
        # Calculate the filter length (M) using the formula
        M = int(np.ceil(6.1 * pi / tr_width)) + 1
        # Ensure M is an odd number
        if M % 2 != 1:
            M = M - 1
        w_use = np.bartlett(M)
    elif cuaso[0] == "Hanning":
        # Calculate the filter length (M) using the formula
        M = int(np.ceil(6.2 * pi / tr_width)) + 1
        # Ensure M is an odd number
        if M % 2 != 1:
            M = M - 1
        w_use = np.hanning(M)
    elif cuaso[0] == "Hamming":
        # Calculate the filter length (M) using the formula
        M = int(np.ceil(6.6 * pi / tr_width)) + 1
        # Ensure M is an odd number
        if M % 2 != 1:
            M = M - 1
        w_use = np.hamming(M)
    elif cuaso[0] == "BlackMan":
        # Calculate the filter length (M) using the formula
        M = int(np.ceil(11 * pi / tr_width)) + 1
        # Ensure M is an odd number
        if M % 2 != 1:
            M = M + 1
        w_use = blackman(M)
    else:
        w_use = None
    # Define the discrete-time variable 'n'
    n = np.arange(0, M)
    # Calculate the normalized cutoff frequency
    wc = (ws + wp) / 2
    # Calculate the alpha parameter for the window
    alpha = (M - 1) / 2
    # Create the time vector 'm' with a small epsilon correction
    m = n - alpha + np.finfo(float).eps
    # Calculate the ideal impulse response of the filter
    hd = np.sin(wc * m) / (pi * m)
    # Apply the window to the ideal impulse response
    h = hd * w_use
    # Calculate frequency response
    w, H = freqz(h, 1, 1000, "whole")
    # Select the range of interest
    # Calculate magnitude, phase, and group delay
    H = np.conj(H)
    mag = abs(H)
    db = 20 * np.log10((mag + np.finfo(float).eps) / np.max(mag))
    pha = np.angle(H)
    grd = group_delay((h, 1), w)
    # Calculate delta_w
    delta_w = 2 * np.pi / 1000

    # Calculate Rp and As
    Rp = -np.min(db[: int(wp / delta_w)])
    As = -np.round(np.max(db[int(ws / delta_w + 1) - 1 : 501]))
    # Plot frequency response
    fig, axs = plt.subplots(2, 2)
    fig.set_size_inches(10, 6)
    fig.suptitle("Bậc của bộ lọc: " + str(M) + "\nChọn cửa sổ " + cuaso[0], fontsize=16)
    for ax in axs:
        fig.canvas.mpl_connect("scroll_event", on_scroll)
    # plt.subplot(1, 1, 1)
    plt.subplot(2, 2, 1)
    plt.stem(n, hd)
    plt.title("Ideal Impulse Response")
    plt.axis([0, M - 1, round(np.min(hd) * 1.2, 1), round(np.max(hd) * 1.2, 1)])
    plt.xlabel("n")
    plt.ylabel("hd(n)")
    plt.subplot(2, 2, 2)
    plt.stem(n, w_use)
    plt.title(cuaso[0] + " Window")
    plt.axis([0, M - 1, 0, round(np.max(w_use) * 1.2, 1)])
    plt.xlabel("n")
    plt.ylabel("w(n)")

    plt.subplot(2, 2, 3)
    plt.stem(n, h)
    plt.title("Actual Impulse Response")
    plt.axis([0, M - 1, round(np.min(h) * 1.2, 1), round(np.max(h) * 1.2, 1)])
    plt.xlabel("n")
    plt.ylabel("h(n)")

    plt.subplot(2, 2, 4)
    if cuaso[0] == "BlackMan":
        plt.plot(w / pi, db, color="blue")
        plt.plot(-w / pi, db, color="blue")
        plt.title("Magnitude Response in dB")
        plt.grid()
        plt.axis(
            [
                -1,
                1,
                round(np.min(db) * 1.2, 1),
                round(np.max(db) * 1.2, 1) + 10,
            ]
        )
    else:
        plt.plot(w / pi, db, color="blue")
        plt.title("Magnitude Response in dB")
        plt.grid()
        plt.axis(
            [
                0,
                1,
                round(np.min(db) * 1.2, 1),
                round(np.max(db) * 1.2, 1) + 10,
            ]
        )
    plt.xlabel("frequency in pi units")
    plt.ylabel("Decibels")

    # Set y-axis tick marks
    plt.tight_layout()
    plt.show()


def thongcao(wp, ws, As):
    np.set_printoptions(precision=4, suppress=True)
    pi = np.pi
    wp = wp * pi
    ws = ws * pi
    tr_width = ws - wp  # Transition width
    # Assuming pi and eps have been defined previously
    for i in windown:
        if i[1] > As:
            cuaso = i
            break

    # Generate a Hamming window of length M
    if cuaso[0] == "Chữ nhật":
        # Calculate the filter length (M) using the formula
        M = int(np.ceil(1.8 * pi / tr_width)) + 1
        # Ensure M is an odd number
        if M % 2 != 1:
            M = M - 1
        w_use = np.ones(M)
    elif cuaso[0] == "Barlett":
        # Calculate the filter length (M) using the formula
        M = int(np.ceil(6.1 * pi / tr_width)) + 1
        # Ensure M is an odd number
        if M % 2 != 1:
            M = M - 1
        w_use = np.bartlett(M)
    elif cuaso[0] == "Hanning":
        # Calculate the filter length (M) using the formula
        M = int(np.ceil(6.2 * pi / tr_width)) + 1
        # Ensure M is an odd number
        if M % 2 != 1:
            M = M - 1
        w_use = np.hanning(M)
    elif cuaso[0] == "Hamming":
        # Calculate the filter length (M) using the formula
        M = int(np.ceil(6.6 * pi / tr_width)) + 1
        # Ensure M is an odd number
        if M % 2 != 1:
            M = M - 1
        w_use = np.hamming(M)
    elif cuaso[0] == "BlackMan":
        # Calculate the filter length (M) using the formula
        M = int(np.ceil(11 * pi / tr_width)) + 1
        # Ensure M is an odd number
        if M % 2 != 1:
            M = M + 1
        w_use = blackman(M)
    else:
        w_use = None
    # Define the discrete-time variable 'n'
    n = np.arange(0, M)
    # Calculate the normalized cutoff frequency
    wc = (ws + wp) / 2
    # Calculate the alpha parameter for the window
    alpha = (M - 1) / 2
    # Create the time vector 'm' with a small epsilon correction
    m = n - alpha + np.finfo(float).eps
    # Calculate the ideal impulse response of the filter
    hd = -np.sin(wc * m) / (pi * m)
    # Apply the window to the ideal impulse response
    h = hd * w_use
    # Calculate frequency response
    w, H = freqz(h, 1, 1000, "whole")
    # Select the range of interest
    # Calculate magnitude, phase, and group delay
    H = np.conj(H)
    mag = abs(H)
    db = 20 * np.log10((mag + np.finfo(float).eps) / np.max(mag))
    pha = np.angle(H)
    grd = group_delay((h, 1), w)
    # Calculate delta_w
    delta_w = 2 * np.pi / 1000

    # Calculate Rp and As
    Rp = -np.min(db[: int(wp / delta_w)])
    As = -np.round(np.max(db[int(ws / delta_w + 1) - 1 : 501]))
    # Plot frequency response
    fig, axs = plt.subplots(2, 2)
    fig.set_size_inches(10, 6)
    fig.suptitle("Bậc của bộ lọc: " + str(M) + "\nChọn cửa sổ " + cuaso[0], fontsize=16)
    for ax in axs:
        fig.canvas.mpl_connect("scroll_event", on_scroll)
    # plt.subplot(1, 1, 1)
    plt.subplot(2, 2, 1)
    plt.stem(n, hd)
    plt.title("Ideal Impulse Response")
    plt.axis([0, M - 1, round(np.min(hd) * 1.2, 1), round(np.max(hd) * 1.2, 1)])
    plt.xlabel("n")
    plt.ylabel("hd(n)")
    plt.subplot(2, 2, 2)
    plt.stem(n, w_use)
    plt.title(cuaso[0] + " Window")
    plt.axis([0, M - 1, 0, round(np.max(w_use) * 1.2, 1)])
    plt.xlabel("n")
    plt.ylabel("w(n)")

    plt.subplot(2, 2, 3)
    plt.stem(n, h)
    plt.title("Actual Impulse Response")
    plt.axis([0, M - 1, round(np.min(h) * 1.2, 1), round(np.max(h) * 1.2, 1)])
    plt.xlabel("n")
    plt.ylabel("h(n)")

    plt.subplot(2, 2, 4)
    if cuaso[0] == "BlackMan":
        plt.plot(w / pi, db, color="blue")
        plt.plot(-w / pi, db, color="blue")
        plt.title("Magnitude Response in dB")
        plt.grid()
        plt.axis(
            [
                -1,
                1,
                round(np.min(db) * 1.2, 1),
                round(np.max(db) * 1.2, 1) + 10,
            ]
        )
    else:
        plt.plot(w / pi, db, color="blue")
        plt.title("Magnitude Response in dB")
        plt.grid()
        plt.axis(
            [
                0,
                1,
                round(np.min(db) * 1.2, 1),
                round(np.max(db) * 1.2, 1) + 10,
            ]
        )
    plt.xlabel("frequency in pi units")
    plt.ylabel("Decibels")

    # Set y-axis tick marks
    plt.tight_layout()
    plt.show()


# thong dai
def thongdai(wp1, ws1, wp2, ws2, As):
    np.set_printoptions(precision=4, suppress=True)
    pi = np.pi
    wp1 = wp1 * pi
    ws1 = ws1 * pi
    wp2 = wp2 * pi
    ws2 = ws2 * pi
    tr_width = np.min([(ws1 - wp1), (ws2 - wp2)])  # Transition width
    # Assuming pi and eps have been defined previously
    for i in windown:
        if i[1] > As:
            cuaso = i
            break

    # Generate a Hamming window of length M
    if cuaso[0] == "Chữ nhật":
        # Calculate the filter length (M) using the formula
        M = int(np.ceil(1.8 * pi / tr_width)) + 1
        # Ensure M is an odd number
        if M % 2 != 1:
            M = M - 1
        w_use = np.ones(M)
    elif cuaso[0] == "Barlett":
        # Calculate the filter length (M) using the formula
        M = int(np.ceil(6.1 * pi / tr_width)) + 1
        # Ensure M is an odd number
        if M % 2 != 1:
            M = M - 1
        w_use = np.bartlett(M)
    elif cuaso[0] == "Hanning":
        # Calculate the filter length (M) using the formula
        M = int(np.ceil(6.2 * pi / tr_width)) + 1
        # Ensure M is an odd number
        if M % 2 != 1:
            M = M - 1
        w_use = np.hanning(M)
    elif cuaso[0] == "Hamming":
        # Calculate the filter length (M) using the formula
        M = int(np.ceil(6.6 * pi / tr_width)) + 1
        # Ensure M is an odd number
        if M % 2 != 1:
            M = M - 1
        w_use = np.hamming(M)
    elif cuaso[0] == "BlackMan":
        # Calculate the filter length (M) using the formula
        M = int(np.ceil(11 * pi / tr_width)) + 1
        # Ensure M is an odd number
        if M % 2 != 1:
            M = M + 1
        w_use = blackman(M)
    else:
        w_use = None
    # Define the discrete-time variable 'n'
    n = np.arange(0, M)
    # Calculate the normalized cutoff frequency
    wc1 = (ws1 + wp1) / 2
    wc2 = (ws2 + wp2) / 2
    # Calculate the alpha parameter for the window
    alpha = (M - 1) / 2
    # Create the time vector 'm' with a small epsilon correction
    m = n - alpha + np.finfo(float).eps
    # Calculate the ideal impulse response of the filter
    hd = np.sin(wc2 * m) / (pi * m) - np.sin(wc1 * m) / (pi * m)
    Y, i = np.max(np.abs(hd)), np.argmax(np.abs(hd))
    hd[i] = (wc2 - wc1) / pi
    # Apply the window to the ideal impulse response
    h = hd * w_use
    # Calculate frequency response
    w, H = freqz(h, 1, 1000, "whole")
    # Select the range of interest
    # Calculate magnitude, phase, and group delay
    H = np.conj(H)
    mag = abs(H)
    db = 20 * np.log10((mag + np.finfo(float).eps) / np.max(mag))
    pha = np.angle(H)
    grd = group_delay((h, 1), w)
    # Calculate delta_w
    delta_w = 2 * np.pi / 1000
    # Plot frequency response
    fig, axs = plt.subplots(2, 2)
    fig.set_size_inches(10, 6)
    fig.suptitle("Bậc của bộ lọc: " + str(M) + "\nChọn cửa sổ " + cuaso[0], fontsize=16)
    for ax in axs:
        fig.canvas.mpl_connect("scroll_event", on_scroll)
    # plt.subplot(1, 1, 1)
    plt.subplot(2, 2, 1)
    plt.stem(n, hd)
    plt.title("Ideal Impulse Response")
    plt.axis([0, M - 1, round(np.min(hd) * 1.2, 1), round(np.max(hd) * 1.2, 1)])
    plt.xlabel("n")
    plt.ylabel("hd(n)")
    plt.subplot(2, 2, 2)
    plt.stem(n, w_use)
    plt.title(cuaso[0] + " Window")
    plt.axis([0, M - 1, 0, round(np.max(w_use) * 1.2, 1)])
    plt.xlabel("n")
    plt.ylabel("w(n)")

    plt.subplot(2, 2, 3)
    plt.stem(n, h)
    plt.title("Actual Impulse Response")
    plt.axis([0, M - 1, round(np.min(h) * 1.2, 1), round(np.max(h) * 1.2, 1)])
    plt.xlabel("n")
    plt.ylabel("h(n)")

    plt.subplot(2, 2, 4)
    if cuaso[0] == "BlackMan":
        plt.plot(w / pi, db, color="blue")
        plt.plot(-w / pi, db, color="blue")
        plt.title("Magnitude Response in dB")
        plt.grid()
        plt.axis(
            [
                -1,
                1,
                round(np.min(db) * 1.2, 1),
                round(np.max(db) * 1.2, 1) + 10,
            ]
        )
    else:
        plt.plot(w / pi, db, color="blue")
        plt.title("Magnitude Response in dB")
        plt.grid()
        plt.axis(
            [
                0,
                1,
                round(np.min(db) * 1.2, 1),
                round(np.max(db) * 1.2, 1) + 10,
            ]
        )
    plt.xlabel("frequency in pi units")
    plt.ylabel("Decibels")

    # Set y-axis tick marks
    plt.tight_layout()
    plt.show()


# chan dai
def chandai(wp1, ws1, wp2, ws2, As):
    np.set_printoptions(precision=4, suppress=True)
    pi = np.pi
    wp1 = wp1 * pi
    ws1 = ws1 * pi
    wp2 = wp2 * pi
    ws2 = ws2 * pi
    tr_width = np.min([(ws1 - wp1), (ws2 - wp2)])  # Transition width
    # Assuming pi and eps have been defined previously
    for i in windown:
        if i[1] > As:
            cuaso = i
            break

    # Generate a Hamming window of length M
    if cuaso[0] == "Chữ nhật":
        # Calculate the filter length (M) using the formula
        M = int(np.ceil(1.8 * pi / tr_width)) + 1
        # Ensure M is an odd number
        if M % 2 != 1:
            M = M - 1
        w_use = np.ones(M)
    elif cuaso[0] == "Barlett":
        # Calculate the filter length (M) using the formula
        M = int(np.ceil(6.1 * pi / tr_width)) + 1
        # Ensure M is an odd number
        if M % 2 != 1:
            M = M - 1
        w_use = np.bartlett(M)
    elif cuaso[0] == "Hanning":
        # Calculate the filter length (M) using the formula
        M = int(np.ceil(6.2 * pi / tr_width)) + 1
        # Ensure M is an odd number
        if M % 2 != 1:
            M = M - 1
        w_use = np.hanning(M)
    elif cuaso[0] == "Hamming":
        # Calculate the filter length (M) using the formula
        M = int(np.ceil(6.6 * pi / tr_width)) + 1
        # Ensure M is an odd number
        if M % 2 != 1:
            M = M - 1
        w_use = np.hamming(M)
    elif cuaso[0] == "BlackMan":
        # Calculate the filter length (M) using the formula
        M = int(np.ceil(11 * pi / tr_width)) + 1
        # Ensure M is an odd number
        if M % 2 != 1:
            M = M + 1
        w_use = blackman(M)
    else:
        w_use = None
    # Define the discrete-time variable 'n'
    n = np.arange(0, M)
    # Calculate the normalized cutoff frequency
    wc1 = (ws1 + wp1) / 2
    wc2 = (ws2 + wp2) / 2
    # Calculate the alpha parameter for the window
    alpha = (M - 1) / 2
    # Create the time vector 'm' with a small epsilon correction
    m = n - alpha + np.finfo(float).eps
    # Calculate the ideal impulse response of the filter
    hd = -np.sin(wc2 * m) / (pi * m) + np.sin(wc1 * m) / (pi * m)
    Y, i = np.max(np.abs(hd)), np.argmax(np.abs(hd))
    hd[i] = (wc2 - wc1) / pi
    # Apply the window to the ideal impulse response
    h = hd * w_use
    # Calculate frequency response
    w, H = freqz(h, 1, 1000, "whole")
    # Select the range of interest
    # Calculate magnitude, phase, and group delay
    H = np.conj(H)
    mag = abs(H)
    db = 20 * np.log10((mag + np.finfo(float).eps) / np.max(mag))
    pha = np.angle(H)
    grd = group_delay((h, 1), w)
    # Calculate delta_w
    delta_w = 2 * np.pi / 1000
    # Plot frequency response
    fig, axs = plt.subplots(2, 2)
    fig.set_size_inches(10, 6)
    fig.suptitle("Bậc của bộ lọc: " + str(M) + "\nChọn cửa sổ " + cuaso[0], fontsize=16)
    for ax in axs:
        fig.canvas.mpl_connect("scroll_event", on_scroll)
    # plt.subplot(1, 1, 1)
    plt.subplot(2, 2, 1)
    plt.stem(n, hd)
    plt.title("Ideal Impulse Response")
    plt.axis([0, M - 1, round(np.min(hd) * 1.2, 1), round(np.max(hd) * 1.2, 1)])
    plt.xlabel("n")
    plt.ylabel("hd(n)")
    plt.subplot(2, 2, 2)
    plt.stem(n, w_use)
    plt.title(cuaso[0] + " Window")
    plt.axis([0, M - 1, 0, round(np.max(w_use) * 1.2, 1)])
    plt.xlabel("n")
    plt.ylabel("w(n)")

    plt.subplot(2, 2, 3)
    plt.stem(n, h)
    plt.title("Actual Impulse Response")
    plt.axis([0, M - 1, round(np.min(h) * 1.2, 1), round(np.max(h) * 1.2, 1)])
    plt.xlabel("n")
    plt.ylabel("h(n)")

    plt.subplot(2, 2, 4)
    if cuaso[0] == "BlackMan":
        plt.plot(w / pi, db, color="blue")
        plt.plot(-w / pi, db, color="blue")
        plt.title("Magnitude Response in dB")
        plt.grid()
        plt.axis(
            [
                -1,
                1,
                round(np.min(db) * 1.2, 1),
                round(np.max(db) * 1.2, 1) + 10,
            ]
        )
    else:
        plt.plot(w / pi, db, color="blue")
        plt.title("Magnitude Response in dB")
        plt.grid()
        plt.axis(
            [
                0,
                1,
                round(np.min(db) * 1.2, 1),
                round(np.max(db) * 1.2, 1) + 10,
            ]
        )
    plt.xlabel("frequency in pi units")
    plt.ylabel("Decibels")

    # Set y-axis tick marks
    plt.tight_layout()
    plt.show()
