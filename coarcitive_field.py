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


fig, ax = plt.subplots(1,figsize=(10,6), sharex=True) 
# fig.suptitle(f'Coercive field', fontsize=16)
# ax.axhline(0, linestyle = "--" , c="k") # horizontal line at energy = 1 
# ax.axvline(0.1, linestyle = "--" , c="k")
ax.set_ylabel('coercivity (Gauss)')
ax.set_xlabel('composition Co_1-X Tb_X')
ax.set_title("Coercive field as a function of composition")


# theoretical values:
# X = [0.10,0.12,0.15]
# real values: 
X= [1-0.122,1-0.145,1-0.1745]
Y = [1118.5, 3100,6945.750]
label = [4.1,4.2,4.3]

ax.plot(X,Y,'-*', label = "Series: 4" ,markersize=20)
ax.legend()
# ax.legend(frameon=False, loc='center left', bbox_to_anchor=(1, 0.5))
if save_plots:
    fig.savefig(f'Coercive field as a function of composition.png', bbox_inches = "tight" ,dpi=300)
fig.tight_layout()
plt.show()


# Put coordinates to every point