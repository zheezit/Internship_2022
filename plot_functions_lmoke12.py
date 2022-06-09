from unittest import skip
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import csv
import os
import sys
import glob
from matplotlib.colors import LinearSegmentedColormap

save_plots = True
colors = plt.cm.Set3(np.linspace(0.3, 1, 10)) #color map, Set3 = hvilken colormap du bruger, der er også Reds
# field_mT = 33.8+166.2 * field_I-0.603* field_I* field_I-0.96 *field_I* field_I* field_I
DeltaH = 50

#This code loads the data and finds the standard deviation and the mean of sampels
def std_pmoke(series, list): 
    data = []
    criterias = []
    for i in range(len(series)):
        for path in list[i]:
            criterias.append(path) #make a list of names so the distinguishment of the different plots are easy
            lmoke1_files = os.listdir(f"moke/{series[i]}/{path}/lmoke1") #load the lmokefiles
            lmoke2_files = os.listdir(f"moke/{series[i]}/{path}/lmoke2") #load the lmokefiles

            lmoke1 = pd.read_table(f"moke/{series[i]}/{path}/lmoke1/{lmoke1_files[0]}", skiprows=4)[["Field","Channel A"]].to_numpy().T
            lmoke2 = pd.read_table(f"moke/{series[i]}/{path}/lmoke2/{lmoke2_files[0]}", skiprows=4)[["Field","Channel A"]].to_numpy().T
            data.append([lmoke1,lmoke2])
    return(data, criterias)

#this code corrigates the drift and make it normalized between -1 and 1. 
def scale_l(x):
    nb = 4
    drift= np.zeros(len(x))
    len_data = len(x)
    # max_end = np.mean(x[-1::]) #here you take the mean of the end
    mean_last_nb = np.mean(x[-nb::]) # take the mean of the last 10 values
    mean_first_nb = np.mean(x[:nb]) # take the mean of the first 10 values
    max_end = mean_last_nb-mean_first_nb  # this is the difference between the 2 means
    for i in range(len_data): 
        drift[i] =(i*(max_end))/len_data # every index has a drift which is linear
    no_drift = x - drift # the final drift is the initial values minus the drift
    i_min = 2 #this code flips the graph if it has the wrong sign
    i_max = int(len_data/2)
    min_MOKE = no_drift[i_max-nb:i_max+nb].mean() 
    max_MOKE = no_drift[i_min:i_min + nb].mean()
    if max_MOKE > min_MOKE: 
        k = (no_drift-max_MOKE + (max_MOKE-min_MOKE)/2)/(max_MOKE-min_MOKE)*2
    else:
        k = -(no_drift-min_MOKE+(min_MOKE-max_MOKE)/2)/(min_MOKE-max_MOKE)*2
    return(k)


## Given a set of datapoints (MOKE and field as well as a description "criterias")
def plotfunction(serie, list): #this function takes in a matrix and let you plot the differents array in the same plot. The criterias helps give name to the different functions. 
    #note that len(criterias) = len(data) + in same order
    data, criterias = std_pmoke(serie, list) # this part finds the std and the mean of the measurements
    # --------------------------------------------------------------------------------------------------------------------------------------------
    fig, ax = plt.subplots(1, 2,figsize=(12,6), sharex=True) 
    fig.suptitle(f'Hysterisis of Magnetization as a function of magnetic field {serie}', fontsize=16)
    ax[0].axhline(0, linestyle = "--" , c="k") # horizontal line at energy = 1 
    ax[0].axhline(0, linestyle = "--" , c="k") # horizontal line at energy = 1 
    ax[0].axvline(0, linestyle = "--" , c="k")
    ax[0].set_ylabel('Intensity')
    ax[0].set_xlabel('Magnetic field(Gauss)')
    ax[0].set_title("lmoke1")

    ax[1].axhline(0, c="k") # horizontal line at enery = 1
    ax[1].set_xlabel('Magnetic field(Gauss)')
    ax[1].set_title("lmoke2")

    for i in range(len(data)):
        field_pmoke = data[i][0][0] + DeltaH
        scaled_pmoke = scale_l(data[i][0][1])
        field_lmoke = data[i][1][0] + DeltaH
        scaled_lmoke = scale_l(data[i][1][1])

        ax[0].plot(
            field_pmoke,scaled_pmoke,'.',
            color = colors[5],)

        ax[1].plot(field_lmoke,scaled_lmoke,'.',
            label = f"{criterias[i]}",
            color = colors[5],)
    # ax[0].legend(frameon=False, loc='center left', bbox_to_anchor=(1, 0.5))
    ax[1].legend(frameon = False, loc='center left', bbox_to_anchor=(1, 0.5))
    if save_plots:
        fig.savefig(f'moke/{serie}.png', bbox_inches = "tight" ,dpi=300)
    fig.tight_layout()
    plt.show()


# ----------------------------------------------------DATA with errorbars - plotfunction -----------------------------------------------------

# # Ta3/(co88tb12)_X/Pt3 changing the thickness made by AP pressure of argon MKS= 1.5 microbar
# list = [["50nm","63nm","75nm","88nm","100nm","150nm"]]
# # list = [["75nm","100nm","150nm"]]
# serie =[ "ap_Ta3(Co88Tb12)XPt3_P(Co)90W_p(Ar)1,5microbar"]
# plotfunction(serie,list)


# Pt3/(co88tb12)_X/Pt3 changing the thickness made by CV
# list = [["25nm","35nm","45nm","55nm","65nm","75nm"]]
# list = [["25nm"]]
list = [["75nm"]]
# list = [["55nm"]]
serie = ["cv_Pt3(Co88Tb12)XnmPt3_P(Co)W_p(ar)1,6microbar"]
plotfunction(serie,list)
