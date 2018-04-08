from scipy.constants import codata
import numpy as np
import math

c = codata.value("speed of light in vacuum") * 10e9 # in nm per s

class FourierTransformer:
    def get_axis(self, dt, t_max):
        df = 1 / dt
        dl = c / df

        return (np.linspace(-0.5 * dl, 0.5 * dl, t_max))

    def transform(self, func, dt, t_max):
        _func =  np.fft.fft(func) * dt

        y = abs(np.fft.fftshift(_func))
        x = self.get_axis(dt, t_max)
         
        lower_boundry = int(round(len(x)*0.5)) + 5
        upper_boundry = int(round(len(x) * 0.8))
      
        return x[lower_boundry:upper_boundry], y[lower_boundry:upper_boundry]
