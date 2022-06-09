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

X = [0,1,2,3]
Y = [6,2,3,6]

fig, ax = plt.subplots(1,figsize=(12,6), sharex=True) 
fig.suptitle(f'Coarcitive field', fontsize=16)
ax.axhline(0, linestyle = "--" , c="k") # horizontal line at energy = 1 
ax.axvline(1.6, linestyle = "--" , c="k")
ax.set_ylabel('Coarcitive field')
ax.set_xlabel('composition Co_1-X Tb_X')
ax.set_title("Coarcitive field")


ax.plot(X,Y,'.')

ax.legend(frameon=False, loc='center left', bbox_to_anchor=(1, 0.5))
if save_plots:
    fig.savefig(f'somename.png', bbox_inches = "tight" ,dpi=300)
fig.tight_layout()
plt.show()


