import numpy as np
import matplotlib.pyplot as plt

class ChannelSpec:
    MIN_FREQ = 2e6  # 2MHz
    MAX_FREQ = 3.5e9  # 3.5GHz
    MIN_MAG = -25  # -25dB
    MAX_MAG = 0  # 0dB
    def __init__(self, points=1000,type='p2p'):
        self.points = points
        self.type = type
        self.f = np.linspace(self.MIN_FREQ, self.MAX_FREQ, self.points, endpoint=True)
        self.il_6Gbps = self.get_6Gbps_IL_limits()


    def get_6Gbps_IL_limits(self):
        if self.type == 'p2p':
            return np.piecewise(self.f,
                        [self.f < 500e6, self.f >= 500e6],
                        [lambda x: -(3.2 + 0.25 * np.sqrt(x * 1e-6) + 0.64 * (x * 1e-9)),
                        lambda x: -(2.74 + 0.25 * np.sqrt(x * 1e-6) + 1.56 * (x * 1e-9))])
        elif self.type == 'cable':
            return np.piecewise(self.f,
                        [self.f < 500e6, self.f >= 500e6],
                        [lambda x: -(3.2 + 0.25 * np.sqrt(x * 1e-6) + 0.64 * (x * 1e-9) - 4),
                        lambda x: -(2.74 + 0.25 * np.sqrt(x * 1e-6) + 1.56 * (x * 1e-9) - 4)])
    



def main():
    cs = ChannelSpec(type='cable')
    plt.plot(cs.f, cs.il_6Gbps)
    plt.ylabel("Magnitude Response (dB)")
    plt.xlabel("Frequency (GHz)")
    plt.xlim([0, cs.MAX_FREQ])
    plt.ylim([cs.MIN_MAG, 0])
    plt.title(f"MAXIMUM INSERTION LOSS")
    plt.grid()
    plt.show()


if __name__ == "__main__":
    main()