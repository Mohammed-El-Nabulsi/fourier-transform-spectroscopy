from utils import Utils

import matplotlib.pyplot as plt
import numpy as np

import re, scipy

class DataProcessor():
    def __init__(self, laser_path, data_path, plot_cb = None):
        self.laser_path = laser_path
        self.data_path = data_path
        self.plot_cb = plot_cb

    def read_files(self):
        laser_file = open(self.laser_path, "r")
        data_file = open(self.data_path, "r")
        return laser_file.readlines(), data_file.readlines()

    def process_file(self, lines):
        x = []
        y = []

        for line in lines:
            str_values = re.split(r'\t+', line)

            values = [float(i) for i in str_values]

            x.append(values[0])
            y.append(np.mean(values[1:]))

        print("orig" + str(len(x)))
        return x, y

    def get_data(self, multiplicator = 2):
        laser_lines, data_lines = self.read_files()
  
        laser_x, laser_y = self.process_file(laser_lines)
        x, y = self.process_file(data_lines)

        if (self.plot_cb):
            self.plot_cb("original-data", x, y, "engine steps", "I")
            self.plot_cb("original-laser-data", laser_x, laser_y, "engine steps", "I")

        x, y = Utils.multiply_data_density(multiplicator, x, y)
        laser_x, laser_y = Utils.multiply_data_density(multiplicator, laser_x, laser_y)

        print("interp")
        print(len(x))
 
        if (self.plot_cb):
            self.plot_cb("interpolated-data", x, y, "engine steps", "I")
            self.plot_cb("interpolated-laser-data", laser_x, laser_y, "engine steps", "I")

        return x, list(reversed(y)), laser_x, list(reversed(laser_y))
