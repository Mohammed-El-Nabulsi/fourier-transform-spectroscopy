import math
import numpy as np

norm = 1;
N = 2;
dt = 0.0005
t = np.arange(0, N, dt)

class FourierExample:
    def generate_random_signal(self):
        return np.sin(2 * np.pi * np.random.rand(len(t))) * (0.4 * norm);

    def generate_signal(self, f1, f2):
        return np.sin(2 * np.pi * f1 * t) + np.sin(2 * np.pi * f2 * t) + self.generate_random_signal()

    def generate_w_axis(self):
        return np.linspace(-1/(2*dt), 1/(2*dt), len(t))

    def fourier_transform(self, func):
        _func =  np.fft.fft(func) * dt
        return abs(np.fft.fftshift(_func))
