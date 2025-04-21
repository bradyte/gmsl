#%%
import serdespy as sdp
import numpy as np
import matplotlib.pyplot as plt
import skrf as rf
import scipy as sp

cableA = './sparams/cableA_2m.s2p'
cableB = './sparams/cableA+D+B_4.3m.s2p'
cableC = './sparams/cableA+D+B+E+C_6.45m.s2p'

#load in touchstone file containing s-params of 2m copper cable connector
thru_file = './sparams/cableA_2m.s2p'
nw = rf.Network(thru_file)

#%%
# generate prbs data with 2e13-1 elements
binary_data = sdp.prbs13(1)

# standard NRZ signal
voltage_levels = np.array([-1, 1])

# baud rate samples signal generated from the binary data and voltage levels
signal_BR = sdp.nrz_input_BR(binary_data, voltage_levels)

# number of samples per NRZ symbol
samples_per_symbol = 100

# oversample the baud rate signal
signal = np.repeat(signal_BR, samples_per_symbol)

# 1Gbps data rate
data_rate = 3e9

# time per bit or unit interval
UI = 1 / data_rate

# timestep in NRZ
dt = UI / samples_per_symbol

# generate eye diagram of ideal signal with 3 UI
sdp.simple_eye(signal, samples_per_symbol*3, 100, dt, f'{data_rate/1e9}Gbps NRZ Signal')





# %% LPF

# 500MHz cutoff frequency
freq_bw = 3e9

# max frequency for constructing discrete transfer function
max_f = 1 / dt

# max_f in rad/s
max_w = max_f * 2 * np.pi

# impulse response length
ir_length = 800

# calculate discrete transfer function of LPF with pole at freq_bw
w, H = sp.signal.freqs([freq_bw * (2 * np.pi)], [1, freq_bw * (2 * np.pi)], np.linspace(0, 0.5 * max_w, ir_length * 4))

# frequency vector for discrete transfer function in Hz
f = w / (2 * np.pi)

#plot frequency response of the LPF
plt.figure(dpi=800)
plt.semilogx(1e-9 * f, 20 * np.log10(abs(H)))
plt.ylabel("Magnitude Response (dB)")
plt.xlabel("Frequency (GHz)")
plt.title(f"Low Pass Filter with {round(freq_bw * 1e-6)}MHz Cutoff Magnitude Bode Plot")
plt.grid()
plt.axvline(x=1e-9*freq_bw, color='grey')
plt.show()

# %%
# find impulse response of LPF
h, t = sdp.freq2impulse(H, f)

# plot impulse response of LPF
plt.figure(dpi=800)
plt.plot(t[:400] * 1e12, h[:400])
plt.title(f"Low Pass Filter with {round(freq_bw * 1e-6)}MHz Cutoff Impulse Response")
plt.xlabel("Time (ps)")
plt.ylabel("Voltage (V)")
plt.show()
# %%

# filtered signal is convoltuion of the impulse response with the signal
signal_filtered = sp.signal.fftconvolve(signal, h[:400])

sdp.simple_eye(signal_filtered[samples_per_symbol*100:], samples_per_symbol*3, 100, UI/samples_per_symbol, f"{data_rate/1e9}Gbps NRZ Signal with {round(freq_bw * 1e-6)}MHz Cutoff Filter")
# # %%

#%%
# t, y = nw.impulse_response()

s12_gated = nw.s12.time_gate(center=0, span=25, t_unit='ns')
# s12_gated.plot_s_db_time()
t, h = s12_gated.impulse_response()

nw.s12.plot_s_db()


# t_start = 545
# t_stop = 600
# plt.stem(t[t_start:t_stop],h[t_start:t_stop])
# plt.show()

# signal_cable = sp.signal.fftconvolve(signal,h[t_start:t_stop])

# sdp.simple_eye(signal_cable[samples_per_symbol*100:], samples_per_symbol*3, 100, UI/samples_per_symbol, title="convolved")

# %%
