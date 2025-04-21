#%%
import serdespy as sdp
import numpy as np
import matplotlib.pyplot as plt
import skrf as rf
import scipy as sp

# %%
nw = rf.Network('./sparams/cableA_2m.s2p')

H = nw.s21.s[:,0,0]
h    = np.real(np.fft.ifft(H))
plt.plot(h)
plt.title("Channel Impulse Response - Direct Conversion")
plt.axis(xmin=0, xmax=100)
plt.show()

# %%
f = nw.s21.f
fmin = f[0]
if(fmin == 0):   # If the d.c. point was included in the Touchstone file...
    fmin = f[1]  # then the next element contains the real fmin.
fmax = f[-1]
Hdc  = 1
HNyq = nw.s21.s[-1, 0, 0]
f = np.arange(fmin, fmax, fmin)    # Enforcing uniform frequency steps. (See #2 above.)
F = rf.Frequency.from_f(f / 1e9)   # skrf.Frequency.from_f() expects its argument to be in units of GHz.
# %%
# Form impulse response from frequency response.
H     = nw.s21.interpolate(F).s[:, 0, 0]
Hconj = np.flip(np.conj(H))
H = np.concatenate((np.insert(H, 0, Hdc), np.insert(Hconj, 0, HNyq)))  # Forming the vector that fft() would've outputted.
h = np.real(np.fft.ifft(H))

# Form time vector.
t0 = 1. / (2. * fmax)  # Sampling interval = 1 / (2 fNyquist).
t  = np.array([n * t0 for n in range(len(h))])

plt.figure(figsize=(7, 5))
plt.plot(t * 1e9, h)
plt.title("Channel Impulse Response - Manually Constructed H(f)")
plt.xlabel("Time (ns)")
#plt.ylabel("h(t) (?)")
plt.axis(xmin=1, xmax=1.5)
plt.show()
# %%
import pybert as pb
# %%
