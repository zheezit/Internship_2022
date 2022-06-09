# -*- coding: utf-8 -*-
"""
Created on Fri May  6 14:50:48 2022

@author: Emmanuelle JAL

To plot MOKE data from the LCPMR set up

"""

import numpy as np
import matplotlib.pyplot as plt

def MOKE_UPMC(file_name,MOKE_type,fig):
    """
    Parameters
    ----------
    file_name : string in ''
    MOKE_type = 'raw', 'norm', 'nodrift' depending on what you want
    fig = if you want to plot figure or not 'fig' or 'nofig'

    Returns
    -------
    field in G, MOKE normalized

    """
    # import data
    path = "C:/Users/macho/Documents/2015-2017 UPMC-ATER/Recherche/MOKE UPMC/2021-04 FeA2 mesure Kath et Cathy/"
    #file_name = "28_04_2021-2271.dat"
    
        
    data = np.loadtxt(path+file_name, skiprows = 5) # import array with 10 columns
    # Field (G), Intensity (A), Channel A, Channel B, Agilent, 0 , RF out, Monitor +, Monitor -, Time
    # We generally use the column Field and Channel A. Can use the intensity and new calibration function if needed
    
    # extract usefull column
    field_H = data[:,0]
    field_I = data[:,1]
    MOKE_raw = data[:,2]
    
    # # plot raw data
    # plt.figure()
    # plt.plot(field_H,MOKE_raw,'-o')
    # plt.xlabel('H (G)')
    # plt.ylabel('MOKE signal')
    # plt.title('raw MOKE for scan'+file_name)
    
    # Calculate max and min in order to plot the normalized signal ##calculate max and min index. 
    i_min = 2 # sometime the first point is not good because the field is not set yet
    i_max = int(len(MOKE_raw)/2 )
    nb_pt = 20 # nb of points for averaging on for max and min value
    
    min_MOKE = MOKE_raw[i_max-nb_pt:i_max].mean(0) ## the min value is a mean over a range
    max_MOKE = MOKE_raw[i_min:i_min+nb_pt].mean(0)
    
    # create the different MOKE signal
    MOKE_signOK = np.zeros(len(MOKE_raw))
    MOKE_norm = np.zeros(len(MOKE_raw))
    drift = np.zeros(len(MOKE_raw))
    MOKE_nodrift = np.zeros(len(MOKE_raw))
    
    # Reverse curve if needed and center it to 0
    if max_MOKE > min_MOKE:
        MOKE_signOK = MOKE_raw-(max_MOKE+min_MOKE)/2
    else:
        MOKE_signOK = -MOKE_raw+(max_MOKE+min_MOKE)/2
        
    # plt.figure()
    # plt.plot(field_H,MOKE_signOK,'-o')
    # plt.xlabel('H (G)')
    # plt.ylabel('MOKE signal')
    # plt.title('raw MOKE for scan'+file_name)
        
    
    # Normalize signal from -1 to 1
    if max_MOKE > min_MOKE:
        MOKE_norm = (MOKE_raw-max_MOKE+(max_MOKE-min_MOKE)/2)/(max_MOKE-min_MOKE)*2
    else:
        MOKE_norm = -(MOKE_raw-min_MOKE+(min_MOKE-max_MOKE)/2)/(min_MOKE-max_MOKE)*2
        
    # plt.figure()
    # plt.plot(field_H,MOKE_norm,'-o',label='MOKE norm')
    # plt.xlabel('H (G)')
    # plt.ylabel('MOKE signal')
    # plt.title('MOKE normalized for scan'+file_name)
    
    # If there is a drift, correct it
    max_end = MOKE_raw[len(MOKE_raw)-nb_pt::].mean(0)
    
    for n in range(len(MOKE_raw)):
        drift[n] =1-n*(1-max_end)/len(MOKE_raw)
    
    MOKE_nodrift = MOKE_norm/drift
    # plt.plot(field_H,MOKE_nodrift,'-o',label='MOKE drift corrected')
    # plt.legend()
    

    # Calculate field in mT, be sure it is the good curve calibration
    field_mT = 33.8+166.2 * field_I-0.603* field_I* field_I-0.96 *field_I* field_I* field_I
    
    if MOKE_type=='raw':
        MOKE = MOKE_signOK
    elif MOKE_type=='norm':
        MOKE = MOKE_norm
    elif MOKE_type=='nodrift':
        MOKE = MOKE_nodrift
        
    if fig=='fig':
        plt.figure()
        plt.plot(field_H,MOKE,'-o',label=MOKE_type)
        plt.xlabel('H (G)')
        plt.ylabel('MOKE signal')
        plt.title('MOKE for scan'+file_name)
        plt.legend()
    
    return[field_H,MOKE]
        
# %%If several files and want to do the mean and std
# determine all the files you want to average
filenames = ["28_04_2021-2267.dat","28_04_2021-2269.dat","28_04_2021-2270.dat","28_04_2021-2271.dat"]
MOKE_type = 'nodrift'

data0 = MOKE_UPMC(str(filenames[0]),MOKE_type,'nofig')

data=np.zeros([len(filenames),np.shape(data0)[1]])

for j in range(len(filenames)):
    MOKE = MOKE_UPMC(str(filenames[j]),MOKE_type,'nofig')
    data[j,:]=MOKE[1]

MOKE_mean = data.mean(0)
MOKE_std = data.std(0)

plt.figure()
plt.errorbar(data0[0],MOKE_mean,yerr=MOKE_std,fmt='-o')
plt.xlabel('H (G)')
plt.ylabel('MOKE signal')


      

    
    
    
    




