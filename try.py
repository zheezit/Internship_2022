from unittest import skip
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import csv
import os
import sys
import glob


p = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20]
print(p[-1::])

path = "150nm"
all_files = glob.glob(path + "*.dat")
print(all_files)

files = os.listdir(path)
print(len(files))
print(files)



save_plots = False

def get_raw(serie, paths):
    data = []
    criterias = []
    for path in paths:
        criterias.append(path)
        pmoke_files = os.listdir(f"moke/{serie}/{path}/pmoke") #load pmoke files in dir moke/{serie}/{path}/pmoke
        print(pmoke_files)
        lmoke_files = os.listdir(f"moke/{serie}/{path}/lmoke") #load lmoke files in dir moke/{serie}/{path}/lmoke
        pmoke = pd.read_table(f"moke/{serie}/{path}/pmoke/{pmoke_files[0]}", skiprows=4)[["Field","Channel A"]].to_numpy().T 
        lmoke = pd.read_table(f"moke/{serie}/{path}/lmoke/{lmoke_files[0]}", skiprows=4)[["Field","Channel A"]].to_numpy().T
        print(len(pmoke))
        data.append([pmoke, lmoke])
        print(len(data))
    return(data, criterias)


def plotfunction(data,criterias): #this function takes in a matrix and let you plot the differents array in the same plot. The criterias helps give name to the different functions. 
    #note that len(criterias) = len(data) + in same order
    fig, ax = plt.subplots(1, 2,figsize=(10,5), sharex=True) 
    fig.suptitle('Hysterisis of Magnetization as a function of magnetic field', fontsize=16)
    ax[0].axhline(0, linestyle = "--" , c="k") # horizontal line at energy = 1 
    ax[0].set_ylabel('Intensity')
    ax[0].set_xlabel('Magnetic field(Gauss)')

    ax[1].axhline(0, c="k") # horizontal line at enery = 1
    ax[1].set_xlabel('Magnetic field(Gauss)')

    for i in range(len(data)):
        ax[0].plot(
            data[i][0][0],scale_p(data[i][0][1]),'.',
            data[i][0][0],scale_p(data[i][0][1]),'-',
            color = colors[i],            
            )
        ax[1].plot(data[i][1][0],scale_l(data[i][1][1]),
            label = f"{criterias[i]}",
            color = colors[i],
            )
    ax[0].legend(frameon=False, loc='center left', bbox_to_anchor=(1, 0.5))
    ax[1].legend(frameon = False, loc='center left', bbox_to_anchor=(1, 0.5))
    # ax[1].set_ylim(-1,1)

    if save_plots:
        fig.savefig('fourth.png', bbox_inches = "tight" ,dpi=300)
    fig.tight_layout()
    plt.show()


def plotfunction_p(data,criterias): #this function takes in a matrix and let you plot the differents array in the same plot. The criterias helps give name to the different functions. 
    #note that len(criterias) = len(data) + in same order
    fig, ax = plt.subplots(1, 2,figsize=(10,5), sharex=True) 
    fig.suptitle('Hysterisis of Magnetization as a function of magnetic field', fontsize=16)
    ax[0].axhline(0, linestyle = "--" , c="k") # horizontal line at energy = 1 
    ax[0].set_ylabel('Intensity')
    ax[0].set_xlabel('Magnetic field(Gauss)')

    for i in range(len(data)):
        ax[0].plot(
            data[i][0][0],scale_p(data[i][0][1]),'.',
            label = f"{criterias[i]}",
            color = colors[i],            
            )
        ax[0].plot(data[i][0][0],scale_p(data[i][0][1]),'-',
            color = colors[i])
    ax[0].legend(frameon=False, loc='center left', bbox_to_anchor=(1, 0.5))

    if save_plots:
        fig.savefig('seccond.png', bbox_inches = "tight" ,dpi=300)
    fig.tight_layout()
    
    plt.show()

def scale(x): # takes in an array; set middle to be at 0 and scale it to go from -1 to 1. 
    min = abs(np.min(x))
    max = abs(np.max(x))
    q =(max-min)/2
    v = x-q
    new_max = abs(np.max(v))
    new_min = abs(np.min(v))
    k = v/new_max
    return(k)






def scale_p(x): # takes in an array; set middle to be at 0 and scale_p it to go from -1 to 1. 
    min = abs(np.min(x))
    max = abs(np.max(x))
    if np.argmax(x) > 4: 
        q =(max-min)/2
        v = x-q
    else: 
        q =(max-min)/2
        v = -(x-q)
    new_max = abs(np.max(v))
    new_min = abs(np.min(v))
    k = v/new_max
    return(k)





## plot only small data
rawdata_p = pd.read_table(r"moke\cv_45nm_p(co)90w_xbar\2,5microbar\pmoke\05_05_2022-72.dat",skiprows=4)
rawdata_l = pd.read_table(r"moke\cv_45nm_p(co)90w_xbar\2,5microbar\lmoke\05_05_2022-76.dat",skiprows=4)


min_p, max_p = rawdata_p["Channel A"].min(), rawdata_p["Channel A"].max()
min_l, max_l = rawdata_l["Channel A"].min(), rawdata_l["Channel A"].max()
# print(min_l,max_l)

data_p = rawdata_p[["Field","Channel A"]].to_numpy().T
data_l = rawdata_l[["Field","Channel A"]].to_numpy().T
# print(data_l)



# ## plot the pmoke
# fig, ax = plt.subplots(1, 2,figsize=(10,5), sharex=True)
# ax[0].plot(data_p[0],scale(data_p[1]))
# ax[0].set_title('Co88Tb12, layer = 150 nm'); 
# ax[0].set_ylabel('Intensity')
# ax[0].set_xlabel('Magnetic field(in??)')
# # ax[0].legend(frameon=False, loc='center left', bbox_to_anchor=(1, 0.5))

# ax[1].plot(data_l[0],scale_2(data_l[1]))

# plt.show()



## plot the lmoke
fig, ax = plt.subplots(1, 2,figsize=(10,5), sharex=True)
ax[0].plot(data_l[0],scale_l2(data_p[1]))
ax[0].set_title('Co88Tb12, layer = 150 nm'); 
ax[0].set_ylabel('Intensity')
ax[0].set_xlabel('Magnetic field(in??)')
# ax[0].legend(frameon=False, loc='center left', bbox_to_anchor=(1, 0.5))

ax[1].plot(data_l[0],scale_2(data_l[1]))

plt.show()


