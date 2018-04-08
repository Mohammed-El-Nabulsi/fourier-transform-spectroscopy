from utils import Utils

import numpy as np

from scipy.signal import argrelextrema    
from scipy.constants import codata

# constants
c = codata.value("speed of light in vacuum") * 10e9 # in nm per s

LASER_WAVELENGTH = 532 # nm

class Calibrator():
    def __init__(self, laser_x, laser_y, scaling, plot_cb = None):
        self.laser_x = laser_x
        self.laser_y = laser_y
        self.scaling = scaling
        self.plot_cb = plot_cb

    def get_calibration(self, x):
        delta, dt_max = self.calculate_calibration()
        return delta, dt_max

    def calculate_calibration(self):
        measured_pos = argrelextrema(np.array(self.laser_y), np.greater)[0]
        measured_pos_idx = np.arange(measured_pos.size)

        # argrelexrema only returns the indecies within the 
        # dataset that contain the maximums. Here we extract them.
        measured_pos_x = []
        measured_pos_y = []
        for i in measured_pos_idx:
            measured_pos_x.append(self.laser_x[measured_pos[i]])
            measured_pos_y.append(self.laser_y[measured_pos[i]])

        measured_pos = measured_pos / self.scaling

        m, b = np.polyfit(measured_pos_idx, measured_pos, 1)

        desired_pos = m * measured_pos_idx + b; 
        delta = desired_pos - measured_pos # -> delta must be added to x

        # Extend the delta function to span the entire measured space
        delta_y = Utils.interpolate(self.laser_x, measured_pos_x, delta)

        # Every step between maximums is 532 nm wide. Use this to 
        # calculate the actual distances for the x axis dx. Then 
        # as the wave moves with c calculate t with dx / c  = dt
        steps_between_max = desired_pos[1] - desired_pos[0]

        # With every engine step the mirror moves one step dx further away from the light.
        # This lengthens the path of the light by a factor of 2, as it has to move the
        # dx to the mirror and back away from the mirror.
        # That means if n steps of the engine led from max to max the path differnce 
        # was actually double that number. Thus:
        dx_max = LASER_WAVELENGTH / (steps_between_max * 2)
        dt_max = dx_max / c # dt_max in seconds
 
        if (self.plot_cb):
            self.plot_cb("laser-maximums", measured_pos_x, measured_pos_y, "engine pos", "I")
            self.plot_cb("measured-maximums", measured_pos_idx, measured_pos, "i", "max")
            self.plot_cb("desired-maximums", measured_pos_idx, desired_pos, "i", "max")
            self.plot_cb("calibration-function", self.laser_x, delta_y, "i", "delta")

        return delta_y, dt_max
        
