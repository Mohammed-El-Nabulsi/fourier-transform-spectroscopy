from fourier import FourierTransformer
from data import DataProcessor
from calibrator import Calibrator 
from utils import Utils

import matplotlib.pyplot as plt
import numpy as np

import os, sys, argparse

LASER_WAVELENGTH = 532 # nm

def main(argv):
   parser = argparse.ArgumentParser()
   parser.add_argument("dataid", help="Chooses data to process. Either 'Iod' or 'Filter'. Required.")
   parser.add_argument("-m", "--multiplier", help="Factor by which the number of datapoints is increased when interpolating. Defaults to 2.", type=int, default=2)
   parser.add_argument("-s", "--save", help="If set saves all plots to ./plots/<data type>/.", action="store_true")
   parser.add_argument("-d", "--display", help="If set displays all plots at runtime.", action="store_true")
   parser.add_argument("-ft", "--ftonly", help="If set with -d or -s  displays/saves only the resulting plots after fourier transformation at runtime.", action="store_true")
   parser.add_argument("-i", "--ignorecalib", help="If set skips calibration.", action="store_true")

   args = parser.parse_args()

   if not check_args_valid(args):
       sys.exit(2)

   if args.dataid == "Filter":
       plot_fkt = plot_fkt_factory("filter", args.save, args.display)

       correction_factor = get_correction_factor("./data/Notch Filter/Data Channel 2.dat", args)

       processor = DataProcessor(
               "./data/Notch Filter/Data Channel 2.dat",
               "./data/Notch Filter/Data Channel 0.dat",
               None if args.ftonly else plot_fkt)
                
       l, spectrum = calculate(
               processor,
               args.multiplier,
               args.ignorecalib,
               None if args.ftonly else plot_fkt,
               correction_factor)

       plot_fkt("spectrum-notch-filter", l, spectrum, "wavelength [nm]", "I")
 
   elif args.dataid == "Iod":
       iod_plot_fkt = plot_fkt_factory("iod", args.save, args.display)
       ref_plot_fkt = plot_fkt_factory("iod-ref", args.save, args.display)

       correction_factor = get_correction_factor("./data/Iod/Data Channel 2.dat", args)
       ref_correction_factor = get_correction_factor("./data/Referenz fuer Iod/Data Channel 2.dat", args)

       processor = DataProcessor(
               "./data/Iod/Data Channel 2.dat",
               "./data/Iod/Data Channel 0.dat",
               None if args.ftonly else iod_plot_fkt)

       ref_processor = DataProcessor(
               "./data/Referenz fuer Iod/Data Channel 2.dat",
               "./data/Referenz fuer Iod/Data Channel 0.dat",
               None if args.ftonly else ref_plot_fkt)


       ref_l, ref_spectrum = calculate(
               ref_processor,
               args.multiplier,
               args.ignorecalib,
               None if args.ftonly else ref_plot_fkt,
               ref_correction_factor)

       l, spectrum = calculate(
               processor,
               args.multiplier,
               args.ignorecalib,
               None if args.ftonly else iod_plot_fkt,
               correction_factor)
       
       # Bring the ref and iod to the same x axis
       y = Utils.interpolate(ref_l, l, spectrum)

       od = np.log(y / ref_spectrum)

       ref_plot_fkt("spectrum-iod-reference", ref_l, ref_spectrum, "wavelength [nm]", "I")
       iod_plot_fkt("spectrum-iod", ref_l, spectrum, "wavelength [nm]", "I")
       iod_plot_fkt("OD", ref_l, od, "wavelength [nm]", "")


# Orchestrates the entire process of data retrieval, interpolation
# calibration and fourier transformation. Returns the resulting
# spectrum over wavelength
def calculate(processor, interp_multiplier, ignore_calib, plot_fkt, correction_factor = 1):
   x, y, laser_x, laser_y = processor.get_data(interp_multiplier)

   calibrator = Calibrator(laser_x, laser_y, interp_multiplier, plot_fkt)
   delta, dt_max = calibrator.get_calibration(x)

   print(len(x))
   if not ignore_calib:
       _x = x + delta

       x = np.linspace(_x[0], _x[-1], len(_x)) 
       y = Utils.interpolate(x, _x, y)

       x = x * correction_factor

   # t in seconds
   t = x * dt_max
   dt = t[1] - t[0]

   t_max = len(t)

   print(len(t))
   print(1/t_max)

   l, y_trans = FourierTransformer().transform(y, dt, t_max)

# /   y_trans = list(reversed(y_trans))

   return l, y_trans

# Calculates the positional error of the laser peak and returns
# the factor needed to correct the wavelenth axis of the laser back to 
# 532nm. This factor is used to correcft every spectrum after calibration
def get_correction_factor(laser_path, args):
   laser_processor = DataProcessor(
           laser_path,
           laser_path,
           None)

   laser_l, laser_spectrum = calculate(
           laser_processor,
           args.multiplier,
           args.ignorecalib,
           None)

   max_wavelength_idx = np.array(laser_spectrum).argmax()
   correction_factor = LASER_WAVELENGTH / laser_l[max_wavelength_idx]
  
   return correction_factor


# This function generates callbacks that saves plots into
# different directories
def plot_fkt_factory(directory, save_plots, show_plots):
   def plot_fkt(name, x, y, xlabel, ylabel):
       if not save_plots and not show_plots:
           return

       if not os.path.exists("plots"):
           os.makedirs("plots")

       if not os.path.exists("plots/" + directory):
           os.makedirs("plots/" + directory)
           
       plt.plot(x, y)
       plt.title(directory + "-" + name)
       plt.xlabel(xlabel)
       plt.ylabel(ylabel)

       if save_plots:
           path = "plots/" + directory + "/" + name + ".png"
           print("Saving file: " + path)
           plt.savefig(path)
       
       if show_plots:
           plt.show()

       plt.clf()

   return plot_fkt


def check_args_valid(args):
   if args.multiplier <= 0:
       print("Multiplier must be an integer greater than 0")
       return False;

   if args.dataid not in ( "Iod", "Filter" ):
       print("Data id must be set to either 'Iod' or 'Filter'!") 
       return False;
   
   return True;


if __name__ == "__main__":
   main(sys.argv[1:])
