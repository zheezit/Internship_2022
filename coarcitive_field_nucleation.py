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
# fig.suptitle(f'Nucleation', fontsize=16)
# ax.axhline(0, linestyle = "--" , c="k") # horizontal line at energy = 1 
# ax.axvline(0.1, linestyle = "--" , c="k")
ax.set_ylabel('Nucleation (Gauss)')
ax.set_xlabel('Thickness of CoTb layer')
ax.set_title("Nucleation as a function of thickness")

##Changing thickness 20220531_APEJX	Ta3/(Co90Tb10)Xnm/Pt3 - Initial = 8*10^-7	Mks = 2*10^-3	CG1= 3*10^-3	P(Co)= 60	2sccm	Acetone
X = [20,50,75,100,150,200]
Y = [445,126,126,447,-39,-842]
ax.plot(X,Y,'-*',label = "serie 5: Co90Tb10",markersize=20)

ax.legend()
# ax.legend(frameon=False, loc='center left', bbox_to_anchor=(1, 0.5))
if save_plots:
    fig.savefig(f'Nucleation as a function of thickness.png', bbox_inches = "tight" ,dpi=300)
fig.tight_layout()
plt.show()


