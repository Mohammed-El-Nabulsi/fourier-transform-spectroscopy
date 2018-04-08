import math
import unittest
import fourierExample 
import matplotlib.pyplot as plt
import numpy as np

class test(unittest.TestCase):
    def test_creates_signal_correctly(self):
       ex = fourierExample.FourierExample()

       signal = ex.generate_signal(0, 1) 

       plt.plot(signal)
       plt.xlabel('s')
       plt.show()

       self.assertTrue(False)

    def test_creates_functioning_fft(self):
       ex = fourierExample.FourierExample()

       signal = ex.generate_signal(50, 100) 

       axis = ex.generate_w_axis()
       _signal = ex.fourier_transform(signal)

       plt.plot(signal)
       plt.xlabel('s')
       plt.show()

       plt.plot(axis, _signal)
       plt.xlabel('Hz')
       plt.show()

       self.assertTrue(False)

if __name__ == '__main__':
    unittest.main()

