import numpy as np


def zmapping(bZ, aZ, Nz, Dz):
    # Coefficient Orders
    bzord = (len(bZ) - 1) * (len(Nz) - 1)
    azord = (len(aZ) - 1) * (len(Dz) - 1)

    # Initialization of Output Coefficients
    bz = np.zeros(bzord + 1)
    az = np.zeros(azord + 1)

    # Z-Mapping for Numerator (bz)
    for k in range(bzord + 1):
        pln = np.poly1d([1])
        for l in range(k):
            pln = np.convolve(pln, Nz)
        pld = np.poly1d([1])
        for l in range(bzord - k):
            pld = np.convolve(pld, Dz)
        bz += bZ[k] * np.convolve(pln, pld)

    # Z-Mapping for Denominator (az)
    for k in range(azord + 1):
        pln = np.poly1d([1])
        for l in range(k):
            pln = np.convolve(pln, Nz)
        pld = np.poly1d([1])
        for l in range(azord - k):
            pld = np.convolve(pld, Dz)
        az += aZ[k] * np.convolve(pln, pld)
    # Normalization
    az1 = az[0]
    az /= az1
    bz /= az1
    return bz, az
