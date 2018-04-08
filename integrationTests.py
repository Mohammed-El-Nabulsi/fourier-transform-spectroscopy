from fourier import FourierTransformer
from calibrator import Calibrator 
import math
import unittest
import data 
import matplotlib.pyplot as plt
import numpy as np

class test(unittest.TestCase):
    def xtest_compare_calibrator_with_multiple_interpolations(self):
        # 2: Light
        # 1: Laser
        processor = preProcessData.DataProcessor("./data/Notch Filter/Data Channel 1.dat", "./data/Notch Filter/Data Channel 2.dat")

        x, y, laser_x, laser_y = processor.get_data(8)

        transformer1 = FourierTransformer(laser_x[1] - laser_x[0], max(laser_x))
        transformer2 = FourierTransformer(x[1] - x[0], max(x))

        fx, fy = transformer1.transform(laser_y)
        print(fy)
        plt.plot(fy)
        plt.show()

        fx, fy = transformer2.transform(y)
        print(fy)
        plt.plot(fy)
        

        plt.xlabel('peak index')
        plt.ylabel('delta')
        plt.show()

    def xtest_compare_calibrator_with_multiple_interpolations(self):
        # 2: Light
        # 1: Laser
        processor = preProcessData.DataProcessor("./data/Notch Filter/Data Channel 1.dat", "./data/Notch Filter/Data Channel 2.dat")

        x, y, laser_x, laser_y = processor.get_data(1)
        calibrator = Calibrator(laser_x, laser_y)
        x, y = calibrator.calculate_calibration();
        plt.plot(x, y)

        x, y, laser_x, laser_y = processor.get_data(2)
        calibrator = Calibrator(laser_x, laser_y)
        x, y = calibrator.calculate_calibration(2);
        plt.plot(x, y)

        x, y, laser_x, laser_y = processor.get_data(8)
        calibrator = Calibrator(laser_x, laser_y)
        x, y = calibrator.calculate_calibration(8);
        plt.plot(x, y)

        plt.xlabel('peak index')
        plt.ylabel('delta')
        plt.show()



    def test_data_looks_good(self):
        def print_plot(name, x, y):
            print(name)
            
        #    plt.plot(x, y)
        #    plt.show()

        # 0: Light
        # 2: Laser
        processor = preProcessData.DataProcessor("./data/Iod/Data Channel 2.dat", "./data/Iod/Data Channel 0.dat", print_plot)


        t, y, dt = processor.get_data(4)

        print("dt: " + str(dt))

        fourierTransformer = FourierTransformer()

        w, y_trans = fourierTransformer.transform(y, dt, len(t))
        print(w)
        print(y_trans)
        dw = abs(w[1] - w[0])
        w_max = len(w)

        print("dw: " + str(dw))
        print("w_max: " + str(w_max))

        plt.plot(w, y_trans)
        plt.xlabel('s')
        plt.show()

if __name__ == '__main__':
    unittest.main()
