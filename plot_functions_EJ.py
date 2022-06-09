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
colors = plt.cm.Set3(np.linspace(0.3, 1, 12)) #color map, Set3 = hvilken colormap du bruger, der er også Reds
# field_mT = 33.8+166.2 * field_I-0.603* field_I* field_I-0.96 *field_I* field_I* field_I


def get_raw(serie, paths): #file1 is the pMOKE and file2 is the LMOKE
    data = []
    criterias = []
    for path in paths:
        criterias.append(path)
        pmoke_files = os.listdir(f"moke/{serie}/{path}/pmoke")
        lmoke_files = os.listdir(f"moke/{serie}/{path}/lmoke")
        pmoke = pd.read_table(f"moke/{serie}/{path}/pmoke/{pmoke_files[0]}", skiprows=4)[["Field","Channel A"]].to_numpy().T
        lmoke = pd.read_table(f"moke/{serie}/{path}/lmoke/{lmoke_files[0]}", skiprows=4)[["Field","Channel A"]].to_numpy().T
        # print(pmoke)
        data.append([pmoke, lmoke])
        # print(pmoke)
    return(data, criterias)

#this code corrigates the drift and make it normalized between -1 and 1. 
def scale_l(x): #normalize and make drift disapear:  
    nb = 10
    drift= np.zeros(len(x))
    len_data = len(x)
    # max_end = np.mean(x[-1::]) #here you take the mean of the end
    mean_last_nb = np.mean(x[-nb::]) # take the mean of the last 10 values
    mean_first_nb = np.mean(x[:nb]) # take the mean of the first 10 values
    max_end = mean_last_nb-mean_first_nb  # this is the difference between the 2 means
    for i in range(len_data): 
        drift[i] =(i*(max_end))/len_data # every index has a drift which is linear
    no_drift = x - drift # the final drift is the initial values minus the drift
    
    # everything is fine until here
    
    
    # Normalization process not good
    #no_drift -=np.mean(no_drift, axis = 0) 
    # you can not take the mean you need to substract the middle value 
    # between no_drif_max and no_drift_min 

    # I do not understand what is below.
    
    # list = no_drift
    # max = abs(np.max(list))
    # min = abs(np.min(list))
    # if max > min: 
    #     k = list/max
    # else:
    #     k = list/min
    
    # to normalize from 1 to -1 you need to divide by the total amplitude/2
    # Normally we should not take the max and min but an average over several points
    i_min = 2 # sometime the first point is not good because the field is not set yet
    i_max = int(len_data/2) 
    
    min_MOKE = no_drift[i_max-nb:i_max].mean()
    max_MOKE = no_drift[i_min:i_min+nb].mean()
    
    if max_MOKE > min_MOKE:
        k = (no_drift-max_MOKE+(max_MOKE-min_MOKE)/2)/(max_MOKE-min_MOKE)*2
    else:
        k = -(no_drift-min_MOKE+(min_MOKE-max_MOKE)/2)/(min_MOKE-max_MOKE)*2
     
    return(k)


#This code finds the standard deviation
def std_pmoke(serie, paths): #file1 is the pMOKE and file2 is the LMOKE
    data = []
    std = []
    criterias = []
    for path in paths:
        criterias.append(path) #make a list of names so the distinguishment of the different plots are easy
        pmoke_files = os.listdir(f"moke/{serie}/{path}/pmoke") #load the pmokefiles 
        lmoke_files = os.listdir(f"moke/{serie}/{path}/lmoke") #load the lmokefiles
        len_field = np.shape(pd.read_table(f"moke/{serie}/{path}/pmoke/{pmoke_files[0]}", skiprows=4)["Field"].to_numpy().T)[0]
        len_p_moke = len(pmoke_files)
        data_pmoke = np.zeros([len_p_moke,len_field]) #makes an numpy matrix which has dim (number of pmokes and number of measurements )
        for i in range(len_p_moke):
            pmoke = pd.read_table(f"moke/{serie}/{path}/pmoke/{pmoke_files[i]}", skiprows=4)[["Field","Channel A"]].to_numpy().T
            data_pmoke[i,:] = pmoke[1]
        mean_pmoke = data_pmoke.mean(0)
        std_pmoke = data_pmoke.std(0)
        lmoke = pd.read_table(f"moke/{serie}/{path}/lmoke/{lmoke_files[0]}", skiprows=4)[["Field","Channel A"]].to_numpy().T
        data.append([np.array([pmoke[0],mean_pmoke]),lmoke])
        # print(std_pmoke)
        std.append(std_pmoke)
    return(data, criterias,std)


## Given a set of datapoints (MOKE and field as well as a description "criterias")
def plotfunction(serie, paths): #this function takes in a matrix and let you plot the differents array in the same plot. The criterias helps give name to the different functions. 
    #note that len(criterias) = len(data) + in same order
    data, criterias, std = std_pmoke(serie, paths)
    # --------------------------------------------------------------------------------------------------------------------------------------------
    fig, ax = plt.subplots(1, 2,figsize=(10,5), sharex=True) 
    fig.suptitle(f'Hysterisis of Magnetization as a function of magnetic field {serie}', fontsize=16)
    ax[0].axhline(0, linestyle = "--" , c="k") # horizontal line at energy = 1 
    ax[0].set_ylabel('Intensity')
    ax[0].set_xlabel('Magnetic field(Gauss)')

    ax[1].axhline(0, c="k") # horizontal line at enery = 1
    ax[1].set_xlabel('Magnetic field(Gauss)')

    for i in range(len(data)):
        ax[0].plot(
            data[i][0][0],scale_l(data[i][0][1]),'.',
            color = colors[i],            
            )
        ax[0].errorbar(data[i][0][0], scale_l(data[i][0][1]),yerr=std[i],fmt='--.', color = colors[i])
        # ax[0].errorbar(x, y, yerr=[yerr, 2*yerr], xerr=[xerr, 2*xerr], fmt='--o')
        ax[1].plot(data[i][1][0],scale_l(data[i][1][1]),
            '.',
            label = f"{criterias[i]}",
            color = colors[i],
            )
    ax[0].legend(frameon=False, loc='center left', bbox_to_anchor=(1, 0.5))
    ax[1].legend(frameon = False, loc='center left', bbox_to_anchor=(1, 0.5))
    if save_plots:
        fig.savefig(f'{serie}.png', bbox_inches = "tight" ,dpi=300)
    fig.tight_layout()
    plt.show()

# (co88tb12)_X changing the thickness made by CV
# list = ["65nm"]
list = ["25nm","35nm","45nm","55nm","65nm","75nm"]
serie = "cv_(co88tb12)X_p(co)"
plotfunction(serie,list)


# ----------------------------------------------------DATA with errorbars - plotfunction -----------------------------------------------------


# # co = 90 W - changing the pressure made by CV: 
# list = ["2,5microbar", "4,5microbar","6,3microbar", "8,7microbar", "10,3microbar", "12,4microbar", "21,3microbar"]
# serie = "cv_45nm_p(co)90w_xbar"
# plotfunction(serie,list)

# # co = 150 W - changing the pressure made by CV: 
# list = ["2,5microbar", "4,5microbar","6,5microbar", "8,5microbar", "10,4microbar", "12,5microbar", "21,6microbar"]
# serie = "cv_45nm_p(co)150w_xbar"
# plotfunction(serie,list)

# # (co88tb12)_X changing the thickness made by CV
# list = ["25nm","35nm","45nm","55nm","65nm","75nm"]
# serie = "cv_(co88tb12)X_p(co)"
# plotfunction(serie,list)

