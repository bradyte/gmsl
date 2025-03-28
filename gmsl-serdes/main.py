import skrf as rf
import matplotlib.pyplot as plt

cableA = './sparams/cableA_2m.s2p'
cableB = './sparams/cableA+D+B_4.3m.s2p'
cableC = './sparams/cableA+D+B+E+C_6.45m.s2p'

nwA = rf.Network(cableA)
nwB = rf.Network(cableB)
nwC = rf.Network(cableC)
nwA.plot_s_db(m=0, n=0)
nwB.plot_s_db(m=0, n=0)
nwC.plot_s_db(m=0, n=0)
plt.xlim([0, 3.5e9])
plt.ylim([-50, 0])
plt.grid(True)
plt.show()