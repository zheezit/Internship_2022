# -*- coding: utf-8 -*-
"""
Created on Fri May  6 14:50:48 2022

@author: Emmanuelle JAL

To plot MOKE data from the LCPMR set up

"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
data = pd.read_table(r"moke\ap_(co88tb12)X_p(co)90W\75nm\27_04_2022-2904.dat", skiprows=4).to_numpy().T
field_H = data[:,0]
field_I = data[:,1]
MOKE_raw = data[:,2]
print(MOKE_raw[2::])
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
# Normalize signal from -1 to 1
if max_MOKE > min_MOKE:
    MOKE_norm = (MOKE_raw-max_MOKE+(max_MOKE-min_MOKE)/2)/(max_MOKE-min_MOKE)*2
else:
    MOKE_norm = -(MOKE_raw-min_MOKE+(min_MOKE-max_MOKE)/2)/(min_MOKE-max_MOKE)*2
# If there is a drift, correct it

max_end = MOKE_raw[len(MOKE_raw)-nb_pt::].mean(0) #here you take the mean of the end. 
for n in range(len(MOKE_raw)): #take every value of the end 
    drift[n] =1-n*(1-max_end)/len(MOKE_raw)
MOKE_nodrift = MOKE_norm/drift
plt.plot(field_H,MOKE_nodrift,'-o',label='MOKE drift corrected')
plt.legend()
plt.show()




# Calculate field in mT, be sure it is the good curve calibration
field_mT = 33.8+166.2 * field_I-0.603* field_I* field_I-0.96 *field_I* field_I* field_I

# if MOKE_type=='raw':
#     MOKE = MOKE_signOK
# elif MOKE_type=='norm':
#     MOKE = MOKE_norm
# elif MOKE_type=='nodrift':
#     MOKE = MOKE_nodrift
    

# plt.figure()
# # plt.plot(field_H,MOKE,'-o',label=MOKE_type)

# plt.xlabel('H (G)')
# plt.ylabel('MOKE signal')
# plt.title('MOKE for scan')
# plt.legend()

# plt.show()

# # return[field_H,MOKE]
    
# # # %%If several files and want to do the mean and std
# # # determine all the files you want to average
# # filenames = ["28_04_2021-2267.dat","28_04_2021-2269.dat","28_04_2021-2270.dat","28_04_2021-2271.dat"]
# # MOKE_type = 'nodrift'

# data0 = MOKE_UPMC(str(filenames[0]),MOKE_type,'nofig')

# # data=np.zeros([len(filenames),np.shape(data0)[1]])

# # for j in range(len(filenames)):
# # MOKE = MOKE_UPMC(str(filenames[j]),MOKE_type,'nofig')
# # data[j,:]=MOKE[1]

# MOKE_mean = data.mean(0)
# MOKE_std = data.std(0)

# plt.figure()
# plt.errorbar(data0[0],MOKE_mean,yerr=MOKE_std,fmt='-o')
# plt.xlabel('H (G)')
# plt.ylabel('MOKE signal')


    









