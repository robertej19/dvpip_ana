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

#This project
from src.utils import data_getter
from src.utils import query_maker
from src.utils import file_maker


data_dir = "data/5_pickled_pandas/lund_pickles/"
data_list = os.listdir(data_dir)
ic.disable()

def vec_subtract(vec1,vec2):
    res = tuple(map(lambda i, j: i - j, vec1, vec2)) 
    return res

def vec_add(vec1,vec2):
    res = tuple(map(lambda i, j: i + j, vec1, vec2)) 
    return res

def calc_inv_mass_squared(four_vector):
    fv = four_vector
    inv_mass2 = fv[0]**2-fv[1]**2-fv[2]**2-fv[3]**2
    return inv_mass2

def calculate_kinematics(event_df):
    ele = event_df.query("particleID == 11")
    pro = event_df.query("particleID == 2212")
    ic(ele)
    ic(pro)
    photons = event_df.query("particleID == 22")
    photon1 = photons.head(n=1)#This will only work for two photons!
    photon2 = photons.tail(n=1)#This will only work for two photons!
    ic(photons)
    ic(photon1)
    

    e_mass = 0.000511
    pro_mass = 0.938
    Ebeam_4mom = (10.6,0,0,10.6)
    e_4mom = (ele["E_GeV"].values[0],ele["mom_x"].values[0],ele["mom_y"].values[0],ele["mom_z"].values[0])
    #e_energy = np.sqrt(e_mass**2+np.sum(np.square(e_mom)))
    pro_4mom = (pro["E_GeV"].values[0],pro["mom_x"].values[0],pro["mom_y"].values[0],pro["mom_z"].values[0])
    target_4mom = (pro_mass,0,0,0)
    pho1_4mom = (photon1["E_GeV"].values[0],photon1["mom_x"].values[0],photon1["mom_y"].values[0],photon1["mom_z"].values[0])
    pho2_4mom = (photon2["E_GeV"].values[0],photon2["mom_x"].values[0],photon2["mom_y"].values[0],photon2["mom_z"].values[0])


    ic(e_4mom)
    ic(Ebeam_4mom)
    ic(pro_4mom)
    Eprime = e_4mom[0]
    ic(Eprime)

    virtual_gamma = vec_subtract(Ebeam_4mom,e_4mom)
    ic(virtual_gamma)
    
    #Calculate kinematic quantities of interest
    Q2 = -1*calc_inv_mass_squared(virtual_gamma)
    nu = virtual_gamma[0]
    xB = Q2/(2*pro_mass*nu)

    pion_4mom = vec_add(pho1_4mom,pho2_4mom)
    ic(pion_4mom)

    #Calculate t
    #t = (P - P')^2
    #t[i] = 2*0.938*(p4_proton[i].E() - 0.938);
    t = -1*calc_inv_mass_squared(vec_subtract(target_4mom,pro_4mom)) 
    #Could also calculate this using (target+e_beam-e'-pion)

    #Calculate phi (trento angle)

    e3 = e_4mom[1:]
    ic(e3)
    v_lepton = np.cross(Ebeam_4mom[1:],e_4mom[1:])
    v_hadron = np.cross(pro_4mom[1:],virtual_gamma[1:])
    v_hadron2 = np.cross(pro_4mom[1:],pion_4mom[1:])

    phi = np.dot(v_lepton,v_hadron)*180/np.pi
  

    ic(v_hadron,v_hadron2)

    

    return Q2, xB, t,phi,Eprime


    
def process_lunds_into_events(df):
    events_list = []
    num_events = df["event_num"].max()
    ic(num_events)
    for ind in range(0,num_events+1):
        if ind % 1000 ==0:
            ic.enable()
            ic(ind)
            ic.disable()
        event_dataframe = df.query("event_num == {}".format(ind))
        
        run_num = 0
        event_num = ind
        lumi = 0
        heli = 0
        Ebeam = 10.6
        
        q2,xb,t,phi,Eprime = calculate_kinematics(event_dataframe)

        events_list.append([run_num,event_num,lumi,heli,
            Ebeam,Eprime,q2,xb,t,phi])
    
    return events_list



out_labels = ["run","event","luminosity","helicity","Ebeam","Eprime","q2","xb","t","phi"]


for lund_pickle in data_list:
    ic(lund_pickle)
    df = data_getter.get_dataframe("lund_pickles/"+lund_pickle)

    ic.disable()
    events_list = process_lunds_into_events(df)
    ic.enable()
    df_out = pd.DataFrame(events_list, columns=out_labels)
    ic(df_out)
    df_out.to_pickle("lund_processed_pickles/"+lund_pickle)
    