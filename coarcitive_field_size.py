from unittest import skip
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import csv
import os
import sys
import glob
from matplotlib.colors import LinearSegmentedColormap
plt.rcParams.update({'font.size': 20})

save_plots = True
colors = plt.cm.Set3(np.linspace(0.2, 1.1, 12)) #color map, Set3 = hvilken colormap du bruger, der er også Reds


fig, ax = plt.subplots(1,figsize=(12,6), sharex=True) 
# fig.suptitle(f'Coercive field', fontsize=16)
# ax.axhline(0, linestyle = "--" , c="k") # horizontal line at energy = 1 
# ax.axvline(0.1, linestyle = "--" , c="k")
ax.set_ylabel('Coercivity (Gauss)')
ax.set_xlabel('Thickness of CoTb layer')
ax.set_title("Coercive field as a function of size")


##Changing thickness 20220531_APEJX	Ta3/(Co90Tb10)Xnm/Pt3 - Initial = 8*10^-7	Mks = 2*10^-3	CG1= 3*10^-3	P(Co)= 60	2sccm	Acetone
X = [20,50,75,100,150,200]
Y = [511.5,403.5,424.5,568,368,175]

ax.plot(X,Y,'-o',label = "serie 5: Co90Tb10",markersize=15)


## Changing thickness	Ta3/(Co88Tb12)X/Pt3				Initial = 2,4*10^-7	Mks = 4,4-5,1*10^-3	CG1= 4.5*10^-3	P(Co)= 30	3sccm	ethanol
X = [20,50,75,100,150,200]
Y = [1570.5,2716,3078.5,3162,5771,3938.5]

ax.plot(X,Y,'-o',label = "serie 3: Co88Tb12",markersize=15)






ax.legend()
# ax.legend(frameon=False, loc='center left', bbox_to_anchor=(1, 0.5))
if save_plots:
    fig.savefig(f'Coercive field as a function of size.png', bbox_inches = "tight" ,dpi=300)
fig.tight_layout()
plt.show()


