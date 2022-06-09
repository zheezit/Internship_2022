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
colors = plt.cm.Set3(np.linspace(0.2, 1.1, 12)) #color map, Set3 = hvilken colormap du bruger, der er også Reds
# field_mT = 33.8+166.2 * field_I-0.603* field_I* field_I-0.96 *field_I* field_I* field_I
# colors = plt.cm.RdGy(np.linspace(0.2, 1.1, 7))
DeltaH = 250

#This code loads the data and finds the standard deviation and the mean of sampels
def std_pmoke(series, list): 
    data = []
    std = []
    criterias = []
    for i in range(len(series)):
        for path in list[i]:
            criterias.append(path) #make a list of names so the distinguishment of the different plots are easy
            pmoke_files = os.listdir(f"moke/{series[i]}/{path}/pmoke") #load the pmokefiles 
            len_field = np.shape(pd.read_table(f"moke/{series[i]}/{path}/pmoke/{pmoke_files[0]}", skiprows=4)["Field"].to_numpy().T)[0]
            len_p_moke = len(pmoke_files)
            data_pmoke = np.zeros([len_p_moke,len_field]) #makes an numpy matrix which has dim (number of pmokes and number of measurements )
            for j in range(len_p_moke):
                pmoke = pd.read_table(f"moke/{series[i]}/{path}/pmoke/{pmoke_files[j]}", skiprows=4)[["Field","Channel A"]].to_numpy().T
                data_pmoke[j,:] = pmoke[1]
            mean_pmoke = data_pmoke.mean(0)
            std_pmoke = data_pmoke.std(0)
            data.append([np.array([pmoke[0],mean_pmoke])])
            # print(std_pmoke)
            std.append(std_pmoke)
            # with open(f'{path}{pmoke}.csv', newline='') as file_name: 
            #     csv.writer(file_name).writerows(pmoke[0] + mean_moke)
    return(data, criterias,std)

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
    data, criterias, std = std_pmoke(serie, list) # this part finds the std and the mean of the measurements
    # --------------------------------------------------------------------------------------------------------------------------------------------
    fig, ax = plt.subplots(1,figsize=(12,6), sharex=True) 
    fig.suptitle(f'Hysterisis of Magnetization as a function of magnetic field {serie}', fontsize=16)
    ax.axhline(0, linestyle = "--" , c="k") # horizontal line at energy = 1 
    ax.axhline(0, linestyle = "--" , c="k") # horizontal line at energy = 1 
    ax.axvline(0, linestyle = "--" , c="k")
    ax.set_ylabel('Intensity')
    ax.set_xlabel('Magnetic field(Gauss)')
    ax.set_title("pmoke")

    for i in range(len(data)):
        field_pmoke = data[i][0][0] + DeltaH
        scaled_pmoke = scale_l(data[i][0][1])
        ax.plot(
            field_pmoke,scaled_pmoke,'.',
            color = colors[i],
            label = f"{criterias[i]}",)

        ax.errorbar(field_pmoke, scaled_pmoke ,yerr=std[i],fmt='--.', 
            color = colors[i],)
    ax.legend(frameon=False, loc='center left', bbox_to_anchor=(1, 0.5))
    if save_plots:
        fig.savefig(f'moke\{serie[0]}\{serie[0]}.png', bbox_inches = "tight" ,dpi=300)
    fig.tight_layout()
    plt.show()

#--------------------------------------------------------Comparing DATA - ---------------------------------------------------

# # Comparing different parts of sampel 
# serie = ["comparing MOKE measurements on different parts of sampel 20220426_APRD1"]
# list = [["75nm_A","75nm_E", "75nm_E2", "75nm_E3","75nm_R"]]
# plotfunction(serie,list)

# # # comparing 75 nm 
# serie = ["comparing MOKE measurements on different parts of sampel 20220426_APRD1","ap_Ta3(Co90Tb10)XPt3_P(Co)60W_p(Ar)0.2microbar","ap_Ta3(Co1-XTbX)75nmPt3_P(Co)60W_p(Ar)0,22microbar" ]
# list = [["75nm_R"],["75nm-20220531_APEJ3"],["X=10-20220525_APEJ3"]]
# plotfunction(serie,list)


# # comparing 150 nm
# serie = ["ap_Pt3(Co88Tb12)XPt3_P(Co)90W_p(Ar)1,5microbar_1","ap_Ta3(Co90Tb10)XPt3_P(Co)60W_p(Ar)0.2microbar","ap_Pt3orTa3(Co88Tb12)XPt3_P(Co)90W_p(Ar)1,56microbar" ]
# list = [["150nm-20220426_APRD3"],["150nm-20220531_APEJ5"],["Ta_150nm-20220518_APEJ8"]]
# plotfunction(serie,list)

# ----------------------------------------------------- DATA -----------------------------------


# # # ap_Ta3(Co90Tb10)XPt3_P(Co)60W_p(Ar)0.2microbar changing the thickness. 
# serie = ["ap_Ta3(Co90Tb10)XPt3_P(Co)60W_p(Ar)0.2microbar"]
# list = [["20nm-20220531_APEJ1", "50nm-20220531_APEJ2", "75nm-20220531_APEJ3", "100nm-20220531_APEJ4","150nm-20220531_APEJ5","200nm-20220531_APEJ6",]]
# plotfunction(serie,list)



# # Pt3/(co88tb12)_X/Pt3 changing the thickness made by APRD pressure of argon MKS= 1.5 microbar
# serie =[ "ap_Pt3(Co88Tb12)XPt3_P(Co)90W_p(Ar)1,5microbar_1"]
# list = [["75nm-20220426_APRD1","100nm-20220426_APRD2","150nm-20220426_APRD3"]]
# plotfunction(serie,list)


# # # moke\ap_Pt3(Co88Tb12)XPt3_P(Co)90W_p(Ar)1,5microbar_3 changing the thickness made by AP pressure of argon MKS = 1.56 microbar
# serie = ["ap_Pt3(Co88Tb12)XPt3_P(Co)90W_p(Ar)1,5microbar_3"]
# list = [["75nm-20220426_APRD1","100nm-20220426_APRD2","150nm-20220426_APRD3"]]
# plotfunction(serie,list)


# # ap_Pt3orTa3(Co88Tb12)XPt3_P(Co)90W_p(Ar)1,56microbar -  changing the thickness made by AP pressure of argon MKS= 1.5 microbar
# serie = ["ap_Pt3orTa3(Co88Tb12)XPt3_P(Co)90W_p(Ar)1,56microbar"]
# # list = [["Pt_50nm-20220518_APEJ4","Pt_75nm-20220518_APEJ1","Pt_100nm-20220518_APEJ2","Pt_150nm-20220518_APEJ3","Ta_50nm-20220518_APEJ5","Ta_75nm-20220518_APEJ6","Ta_100nm-20220518_APEJ7","Ta_150nm-20220518_APEJ8"]]
# # plotfunction(serie,list)
# list = [["Ta_50nm-20220518_APEJ5","Ta_75nm-20220518_APEJ6","Ta_100nm-20220518_APEJ7","Ta_150nm-20220518_APEJ8"]]
# plotfunction(serie,list)
# list = [["Pt_50nm-20220518_APEJ4","Ta_50nm-20220518_APEJ5"]]
# plotfunction(serie,list)
# list = [["Pt_75nm-20220518_APEJ1","Ta_75nm-20220518_APEJ6"]]
# plotfunction(serie,list)
# list = [["Pt_100nm-20220518_APEJ2","Ta_100nm-20220518_APEJ7"]]
# plotfunction(serie,list)
# list = [["Pt_150nm-20220518_APEJ3","Ta_150nm-20220518_APEJ8"]]
# plotfunction(serie,list)


# # ap_Ta3(Co88Tb12)XPt3_P(Co)90W_p(Ar)1,5microbar - changing the thickness made by AP pressure of argon MKS= 1.5 microbar
# list = [["50nm-20220511_APEJ1","63nm-20220511_APEJ2","75nm-20220511_APEJ3","88nm-20220511_APEJ4","100nm-20220511_APEJ5","150nm-20220511_APEJ6"]]
# serie =[ "ap_Ta3(Co88Tb12)XPt3_P(Co)90W_p(Ar)1,5microbar"]
# plotfunction(serie,list)


# cv_Pt3(Co88Tb12)45nmPt3_P(co)90W_p(ar)xbar - Changing the pressure made by CV: 
# serie = ["cv_Pt3(Co88Tb12)45nmPt3_P(co)90W_p(ar)xbar"]
# list = [["2,5microbar-20210514_CVMH1", "4,6microbar-202105014_CVMH2","6,3microbar-20210519_CVEJ2","8,7microbar-20210519_CVEJ3","10,3microbar-20210519_CVEJ4","12,4microbaR-20210531_CVMH1","21,3microbar-20210519_CVEJ6"]]
# plotfunction(serie,list)


# # cv_Pt3(Co88Tb12)45nmPt3_P(co)150W_p(ar)xbar - changing the pressure made by CV: 
# serie = ["cv_Pt3(Co88Tb12)45nmPt3_P(co)150W_p(ar)xbar"]
# list = [["2,5microbar-20210526_CVEJ1", "4,5microbar-20210526_CVEJ2", "6,5microbar-20210526_CVEJ3", "8,5microbar-20210526_CVEJ4", "10,4microbar-20210526_CVEJ5", "12,5microbar-20210526_CVEJ6", "21,6microbar-20210526_CVEJ7"]]
# plotfunction(serie,list)


# # cv_Pt3(Co88Tb12)XnmPt3_P(Co)W_p(ar)1,6microbar - Pt3/(co88tb12)_X/Pt3 changing the thickness made by CV
# serie = ["cv_Pt3(Co88Tb12)XnmPt3_P(Co)W_p(ar)1,6microbar"]
# list = [["25nm-20210602_CVMH1","35nm-20210602_CVMH2","45nm-20210602_CVMH3","55nm-20210602_CVMH4","65nm-20210602_CVMH5","75nm-20210602_CVMH6"]]
# plotfunction(serie,list)


##only pmoke

# ap_Ta3(Co1-XTbX)75nmPt3_P(Co)60W_p(Ar)0,22microbar changing the composition
# serie = ["ap_Ta3(Co1-XTbX)75nmPt3_P(Co)60W_p(Ar)0,22microbar"]
# list = [["X=10-20220525_APEJ3", "X=12-20220525_APEJ1", "X=12-20220525_APEJ1-Ethanol", "X=15-20220525_APEJ2"]]
# plotfunction(serie,list)
# list = [["X=12-20220525_APEJ1", "X=12-20220525_APEJ1-Ethanol"]]
# plotfunction(serie,list)

# # Pt3/(co88tb12)_X/Pt3 changing the thickness made by AP pressure of argon MKS= 1.5 microbar Done it again with Marcel- ONLY PMOKE
# serie =[ "ap_Pt3(Co88Tb12)XPt3_P(Co)90W_p(Ar)1,5microbar_2"]
# list = [["75nm-20220426_APRD1","100nm-20220426_APRD2","150nm-20220426_APRD3"]]
# plotfunction(serie,list)

# # Changing the thickness.
# serie = ["comparing MOKE measurements from last year changing thicknessP(Co)W_p(Ar)1,6microbar"]
# list = [["25nm-20210602_CVMH1","25nm-20210602_CVMH1-CV", "35nm-20210602_CVMH2", "35nm-20210602_CVMH2-CV", "45nm-20210602_CVMH3","45nm-20210602_CVMH3-CV","55nm-20210602_CVMH4","55nm-20210602_CVMH4-CV"]]
# plotfunction(serie,list)
# list = [["25nm-20210602_CVMH1","25nm-20210602_CVMH1-CV"]]
# plotfunction(serie,list)
# list = [["35nm-20210602_CVMH2", "35nm-20210602_CVMH2-CV"]]
# plotfunction(serie,list)
# list = [["45nm-20210602_CVMH3","45nm-20210602_CVMH3-CV"]]
# plotfunction(serie,list)
# list = [["55nm-20210602_CVMH4","55nm-20210602_CVMH4-CV"]]
# plotfunction(serie,list)
# list =[["25nm-20210602_CVMH1", "35nm-20210602_CVMH2","45nm-20210602_CVMH3", "55nm-20210602_CVMH4"]] 
# plotfunction(serie,list)
# list = [["25nm-20210602_CVMH1-CV", "35nm-20210602_CVMH2-CV","45nm-20210602_CVMH3-CV", "55nm-20210602_CVMH4-CV"]]
# plotfunction(serie,list)

# serie = ["comparing MOKE measurements from last year P(co)150W_p(Ar)xbar"]
# # list = [["2,5microbar-20210526_CVEJ1", "2,5microbar-20210526_CVEJ1-CV", "4,5microbar-20210526_CVEJ2", "4,5microbar-20210526_CVEJ2-CV", "6,5microbar-20210526_CVEJ3", "6,5microbar-20210526_CVEJ3-CV", "8,5microbar-20210526_CVEJ4", "8,5microbar-20210526_CVEJ4-CV", "10,4microbar-20210526_CVEJ5", "10,4microbar-20210526_CVEJ5-CV","12,5microbar-20210526_CVEJ6","12,5microbar-20210526_CVEJ6-CV"]]
# # plotfunction(serie,list)
# list = [["2,5microbar-20210526_CVEJ1", "2,5microbar-20210526_CVEJ1-CV"]]
# plotfunction(serie,list)
# list = [["4,5microbar-20210526_CVEJ2", "4,5microbar-20210526_CVEJ2-CV"]]
# plotfunction(serie,list)
# list = [["6,5microbar-20210526_CVEJ3", "6,5microbar-20210526_CVEJ3-CV"]]
# plotfunction(serie,list)
# list = [["8,5microbar-20210526_CVEJ4", "8,5microbar-20210526_CVEJ4-CV"]]
# plotfunction(serie,list)
# list = [["10,4microbar-20210526_CVEJ5", "10,4microbar-20210526_CVEJ5-CV"]]
# plotfunction(serie,list)
# list = [["12,5microbar-20210526_CVEJ6","12,5microbar-20210526_CVEJ6-CV"]]
# plotfunction(serie,list)

# # # ap_Ta3(Co88Tb12)XPt3_P(Co)30W_p(Ar)0,41-0,51microbar - Changing the thickness
# serie = ["ap_Ta3(Co88Tb12)XPt3_P(Co)30W_p(Ar)0,41-0,51microbar"]
# list = [["20nm-20220523_APEJ1","50nm-20220523_APEJ2","75nm-20220523_APEJ3","100nm-20220523_APEJ4","150nm-20220523_APEJ5","200nm-20220523_APEJ6"]] 
# plotfunction(serie,list)


# serie = ["comparing MOKE measurements on differents parts of sample 20220518_APEJ6"]
# list = [["75nm_A", "75nm_E", "75nm_E2", "75nm_E3"]]
# # list  = [["75nm_A", "75nm_E"]]
# plotfunction(serie,list)


# serie = ["comparing MOKE measuremtns on different parts of sample 20220518_APEJ1"]
# list = [["75nm_A", "75nm_E", "75nm_E2", "75nm_E3"]]
# # list  = [["75nm_A", "75nm_E"]]
# plotfunction(serie,list)






