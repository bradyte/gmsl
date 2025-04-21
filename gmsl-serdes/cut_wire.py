#%%
# import serdespy as sdp
import numpy as np
import matplotlib.pyplot as plt
import skrf as rf
import scipy as sp


# %%

cable_cut_wire_base =       './sparams/cut/cut_wire_base.s2p'
cable_cut_wire_copper =     './sparams/cut/cut_wire_copper.s2p'
cable_cut_wire_bare =       './sparams/cut/cut_wire_copper_bare.s2p'
cable_cut_wire_copper_ur1 = './sparams/cut/cut_wire_copper_ur1.s2p'
cable_cut_wire_copper_ur2 = './sparams/cut/cut_wire_copper_ur2.s2p'
cable_cut_wire_copper_ur3 = './sparams/cut/cut_wire_copper_ur3.s2p'



# %%
nw = rf.Network('./sparams/cableA_2m.s2p')
nw.s22.plot_z_time_step(0, 0, label='meas')
plt.ylim([45, 55])
# nw.s22.plot_s_db()
plt.grid(True)
# %%

nw1 = rf.Network(cable_cut_wire_base)
nw2 = rf.Network(cable_cut_wire_copper)
nw3 = rf.Network(cable_cut_wire_copper_ur1)
nw4 = rf.Network(cable_cut_wire_copper_ur2)
nw5 = rf.Network(cable_cut_wire_copper_ur3)
nw6 = rf.Network(cable_cut_wire_bare)

nw1.s22.plot_s_db(linewidth = 1)
nw2.s22.plot_s_db(linewidth = 1)
nw3.s22.plot_s_db(linewidth = 1)
nw4.s22.plot_s_db(linewidth = 1)
nw5.s22.plot_s_db(linewidth = 1)
nw6.s22.plot_s_db(linewidth = 1)

plt.grid(True)

import numpy as np
import matplotlib.pyplot as plt


def channel_gmsl2(f):
    if f >= 2e6 and f < 10e6:
        return -6 - 0.9 * np.sqrt(f * 1e-6)
    elif f >= 10e6 and f < 200e6:
        return -(14.2 + 0.28 * np.sqrt(f * 1e-6) + 0.8 * (f * 1e-9))
    elif f >= 200e6 and f < 400e6:
        return -18.3 + 0.02 * ((f * 1e-6) - 200)
    elif f >= 400e6 and f < 1.5e9:
        return 5.7e-3 * (f * 1e-6) - 16.6
    elif f >= 1.5e9 and f < 3.5e9:
        return -8
    
def channel_gmsl3_short(f):
    if f >= 2e6 and f < 10e6:
        return -9 - 0.9 * (f * 1e-6)
    elif f >= 10e6 and f < 800e6:
        return -18
    elif f >= 800e6 and f < 3e9:
        return -16.9 + 8 * (f * 1e-9 - 1) / 1.5
    elif f >= 3e9 and f < 3.5e9:
        return -6.2
    
def channel_gmsl3_long(f):
    if f >= 2e6 and f < 10e6:
        return -9 - 0.9 * (f * 1e-6)
    elif f >= 10e6 and f < 1e9:
        return -18
    elif f >= 1e9 and f < 2.5e9:
        return -23.33 + 5.33 * (f * 1e-9)
    elif f >= 2.5e9 and f < 3.5e9:
        return -10


f = np.arange(2e6, 3.5e9, 1e4)
il_gmsl2 = np.vectorize(channel_gmsl2)(f)
il_gmsl3_short = np.vectorize(channel_gmsl3_short)(f)
il_gmsl3_long = np.vectorize(channel_gmsl3_long)(f)


plt.plot(f, il_gmsl2, 'r-')
plt.plot(f, il_gmsl3_short, 'k-')
plt.plot(f, il_gmsl3_long, 'g-')


plt.title('Maximum Pin-to-Pin Return Loss')
plt.xlabel('Frequency (GHz)')
plt.ylabel('Return Loss (dB)')
plt.axis([0, 3.5e9, -50, 0])
plt.grid(True)
plt.show()


# %%
