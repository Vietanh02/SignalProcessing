import numpy as np
from scipy.signal import ellip, ellipord, sos2tf, tf2zpk
import matplotlib.pyplot as plt
from scipy.signal import freqz, group_delay

pi = float(np.pi)
np.set_printoptions(precision=5, suppress=True)


def freqz_m(b, a):
    w, H = freqz(b, a, 1000, "whole")
    H = H[:501]
    w = w[:501]

    mag = np.abs(H)
    db = 20 * np.log10((mag + np.finfo(float).eps) / np.max(mag))
    pha = np.angle(np.conjugate(H))
    grd = group_delay((b, a), w)[1]

    return db, mag, pha, grd, w


# Define stopband and passband edge frequencies
ws = [0.3, 0.75]
wp = [0.4, 0.6]

# Set passband ripple and stopband attenuation
Rp = 1  # Passband ripple in dB
As = 40  # Stopband attenuation in dB

# Convert ripple and attenuation to amplitude factors
Ripple = 10 ** (-Rp / 20)
Attn = 10 ** (-As / 20)

# Calculate filter order and natural frequency
N, wn = ellipord(wp, ws, Rp, As, analog=False)

# Design digital elliptic bandpass filter
b, a = ellip(N, Rp, As, wn, analog=False, output="ba", btype="bandpass")
fig, axs = plt.subplots(2, 2, figsize=(8, 8))
fig.set_size_inches(10, 6)
cuaso = "Elliptic"
fig.suptitle(f"{cuaso} Filter Order = {N}", fontsize=16)
# Convert filter to second-order sections
[db, mag, pha, grd, w] = freqz_m(b, a)
plt.subplot(2, 2, 1)
plt.plot(w / np.pi, mag)
plt.grid(True)
plt.title("Magnitude Response")
plt.xlabel("Frequency in pi units")
plt.axis([0, 1, 0, 1])
plt.xticks([0, 0.3, 0.4, 0.6, 0.75, 1])
plt.yticks([0, Ripple, 1])

# Subplot 2: Magnitude in dB
plt.subplot(2, 2, 3)
plt.plot(w / np.pi, db)
plt.grid(True)
plt.title("Magnitude in dB")
plt.xlabel("Frequency in pi units")
plt.ylabel("dB")
plt.axis([0, 1, -50, 0])
plt.xticks([0, 0.3, 0.4, 0.6, 0.75, 1])
plt.yticks([-40, 0])

# Subplot 3: Phase Response
plt.subplot(2, 2, 2)
plt.plot(w / np.pi, pha / np.pi)
plt.grid(True)
plt.title("Phase Response")
plt.xlabel("Frequency in pi units")
plt.ylabel("Phase in pi units")
plt.xticks([0, 0.3, 0.4, 0.6, 0.75, 1])

# Subplot 4: Group Delay
plt.subplot(2, 2, 4)
plt.plot(w / np.pi, grd)
plt.grid(True)
plt.title("Group Delay")
plt.xlabel("Frequency in pi units")
plt.ylabel("Samples")
plt.xticks([0, 0.3, 0.4, 0.6, 0.75, 1])

plt.tight_layout()
plt.show()
