import pandas as pd
import numpy as np 
import matplotlib.pyplot as plt 
import random 
import sys
import os, subprocess
from pdf2image import convert_from_path
import math
from icecream import ic
import shutil
from PIL import Image, ImageDraw, ImageFont

from fitting import phi_Fitter
from utils import file_maker

def passto_phifit(x,ranges,plot_dir):

    phi_vals = x

    xmin = str(ranges[0])
    xmax = str(ranges[1])
    q2min = str(ranges[2])
    q2max = str(ranges[3])
    tmax = str(ranges[4])
    tmin = str(ranges[5])
    
    plot_title = 'phi-fit-xb-{}-{}-q2-{}-{}-t-{}-{}'.format(xmin,xmax,q2min,q2max,tmin,tmax)

    return phi_Fitter.getPhiFit(phi_vals,plot_title,plot_dir)
    

datadir = "pickled_data/"
datafile = "skims-168.pkl"
data = pd.read_pickle(datadir+datafile)
ic(data.shape)


#Official splits
xb_ranges = [0.1,0.15,0.2,0.25,0.3,0.35,0.4,0.45,0.5,0.55,0.6,0.7,0.85,1]
q2_ranges = [1.0,1.5,2.0,2.5,3.0,3.5,4.0,4.5,5.0,5.5,6.0,7.0,8.0,9.0,12.0]
t_ranges = [0.09,0.15,0.2,0.3,0.4,0.6,1,1.5,2,3,4.5,6]

#save_folder = "phi_pics/"
save_folder = "fitted_phi_plots/"
file_maker.make_dir(save_folder)
  
#Making individual phi plots
t_vals = []
for q2_ind in range(1,len(q2_ranges)):
    print("----- On Q2 {} out of {} -------".format(q2_ind,len(q2_ranges)-1))
    q2_min = q2_ranges[q2_ind-1]
    q2_max = q2_ranges[q2_ind]
    for xb_ind in range(1,len(xb_ranges)):
        print("On xB {} out of {}".format(xb_ind,len(xb_ranges)))
        xb_min = xb_ranges[xb_ind-1]
        xb_max = xb_ranges[xb_ind]
        for t_ind in range(1,len(t_ranges)):
            t_min = t_ranges[t_ind-1]
            t_max = t_ranges[t_ind]
            #print(xb_min,xb_max,q2_min,q2_max,t_min,t_max)
            ranges = [xb_min,xb_max,q2_min,q2_max,t_min,t_max]
            data_xb = data[(data['xB']>xb_min) & (data['xB']<=xb_max) & (data['Q2']>q2_min) & (data['Q2']<=q2_max)& (data['t']>t_min) & (data['t']<=t_max)]

            #just_phi_plotter(data_xb["Phi"],ranges,save_folder)
            fit_params = passto_phifit(data_xb["Phi"],ranges,save_folder)
            print(fit_params)
            t_vals.append([q2_min,q2_max,xb_min,xb_max,t_min,t_max,fit_params[0],fit_params[1],fit_params[2]])
            #print(t_vals)
    df = pd.DataFrame(t_vals, columns=['Q2min', 'Q2max', 'xBmin','xBmax','tmin','tmax','A','B','C'])
    print("DF IS ----------")
    print(df)
    df.to_pickle("pickled_data/phi_fit_vals.pkl")


