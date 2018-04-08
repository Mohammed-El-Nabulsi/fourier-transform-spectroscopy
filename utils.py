import numpy as np
import scipy

class Utils():
    # Multiplicator defines by how many datapoints should be interpolated
    def multiply_data_density(multiplicator, x, y):
        first_x = x[0]

        N = max(x)

        new_length = N * multiplicator
        new_x = np.linspace(first_x, N, new_length)
        
        # We use kind=cubic as it most easily can fit oszillations
        new_y = scipy.interpolate.interp1d(x, y, fill_value=[0], kind='cubic')(new_x)
      
        return new_x, new_y

    def interpolate(new_x, x, y):
        # We made sure that only a small number of data points at the beginning and end 
        # of the dataset is being extrapolated.
        # Extrapolation is mandatory here, because we are fitting the measured maximums
        # back to the original x axis. Because the measured maximums won't be exactly at
        # the boundries of the x axis, they will cover only a subset of it. Thus we have to
        # extrapolate the values -2000 and 2000 at the edge of the x axis.
        new_y = scipy.interpolate.interp1d(x, y, fill_value="extrapolate", kind='cubic')(new_x)
        return new_y


