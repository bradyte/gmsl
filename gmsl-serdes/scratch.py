#%%
import serdespy as sdp
import numpy as np
import matplotlib.pyplot as plt
import skrf as rf
import scipy as sp

#%%
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


def plot_return_loss():
    f = np.arange(2e6, 3.5e9, 1e4)
    rl_gmsl2 = np.vectorize(channel_gmsl2)(f)
    rl_gmsl3_short = np.vectorize(channel_gmsl3_short)(f)
    rl_gmsl3_long = np.vectorize(channel_gmsl3_long)(f)

    plt.plot(f, rl_gmsl2, 'r-')
    plt.plot(f, rl_gmsl3_short, 'k-')
    plt.plot(f, rl_gmsl3_long, 'g-')


def func(x, a, b, c):
    return (a + b * np.sqrt(x * 1e-6) + c * (x * 1e-9))

def plot_insertion_loss():
    f = np.linspace(2e6, 3.5e9, 1000, endpoint=True)

    il_gmsl2 = -func(f, 2.74, 0.25, 1.56)
    il_gmsl3_short = -func(f, 1.45, 0.101, 1.01)
    il_gmsl3_long = -func(f, 1.62, 0.182, 2.14)

    plt.plot(f, il_gmsl2, 'r-')
    plt.plot(f, il_gmsl3_short, 'k-')
    plt.plot(f, il_gmsl3_long, 'g-')





#%%

#load in touchstone file containing s-params of 2m copper cable connector
cable_2m= './sparams/cableA_2m.s2p'
cable_4m= './sparams/cableA_4m_2interconnect.s2p'
cable_6m= './sparams/cableA_6m_4interconnect.s2p'
cable_8m= './sparams/cableA_8m_6interconnect.s2p'
cable_10m= './sparams/cableA_10m_8interconnect.s2p'
cable_2m_20C = './sparams/cableA_2m_-20C.s2p'
cable_2m_85C = './sparams/cableA_2m_85C.s2p'
cable_2m_B = './sparams/cableB_2m.s2p'

#%% temperature comparison
nwA = rf.Network(cable_2m)
nwB = rf.Network(cable_2m_20C)
nwC = rf.Network(cable_2m_85C)

nwA.plot_s_db(m=0, n=1)
nwB.plot_s_db(m=0, n=1)
nwC.plot_s_db(m=0, n=1)
plot_insertion_loss()
# plt.xlim([0, 3.5e9])
# plt.ylim([-25, 0])
# plt.grid()

plt.xlim([2.5e9, 3.5e9])
plt.ylim([-5, 0])
plt.grid()

# nwA.plot_s_db(m=0, n=0)
# nwB.plot_s_db(m=0, n=0)
# nwC.plot_s_db(m=0, n=0)
# plot_return_loss()
# plt.xlim([0, 3.5e9])
# plt.ylim([-50, 0])
# plt.grid()
# plt.title("Comparison plot of cables at -20C, 25C, and 85C")

# %% cable length comparison

nwA = rf.Network(cable_2m)
nwB = rf.Network(cable_4m)
nwC = rf.Network(cable_6m)
nwD = rf.Network(cable_8m)
nwE = rf.Network(cable_10m)

nwA.plot_s_db(m=0, n=1)
nwB.plot_s_db(m=0, n=1)
nwC.plot_s_db(m=0, n=1)
nwD.plot_s_db(m=0, n=1)
nwE.plot_s_db(m=0, n=1)

# nwA.plot_s_db(m=0, n=1, logx='True')
# nwB.plot_s_db(m=0, n=1, logx='True')
# nwC.plot_s_db(m=0, n=1, logx='True')
# nwD.plot_s_db(m=0, n=1, logx='True')
# nwE.plot_s_db(m=0, n=1, logx='True')

# plot_insertion_loss()
plt.xlim([0, 3.5e9])
plt.ylim([-25, 0])
plt.grid()

# nwA.plot_s_db(m=0, n=0)
# nwB.plot_s_db(m=0, n=0)
# nwC.plot_s_db(m=0, n=0)
# nwD.plot_s_db(m=0, n=0)
# nwE.plot_s_db(m=0, n=0)
# plot_return_loss()
# plt.xlim([0, 3.5e9])
# plt.ylim([-50, 0])
# plt.grid()

plt.title("Comparison plot of various cable lengths")

# %%
nwA = rf.Network(cable_2m)
nwB = rf.Network(cable_2m_B)

# nwA.plot_s_db(m=0, n=1)
# nwB.plot_s_db(m=0, n=1)
# plot_insertion_loss()
# plt.xlim([0, 3.5e9])
# plt.ylim([-25, 0])
# plt.grid()

nwA.plot_s_db(m=0, n=0)
nwB.plot_s_db(m=0, n=0)
plot_return_loss()
plt.xlim([0, 3.5e9])
plt.ylim([-50, 0])
plt.grid()


plt.title("Comparison plot of different cable manufacturers")
# %%
