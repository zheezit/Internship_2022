import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os


colors = plt.cm.Set3(np.linspace(0.3, 1, 11)) #color map, Set3 = hvilken colormap du bruger, der er også Reds

def plotfunction(serie, list):
    data = []
    lmoke_files = os.listdir(f"moke/raw_data/{serie[0]}/{list[0][0]}/lmoke") 
    for file in lmoke_files: 
        lmoke = pd.read_table(f"moke/raw_data/{serie[0]}/{list[0][0]}/lmoke/{file}", skiprows=4)[["Field","Channel A"]].to_numpy().T
        data.append([lmoke])
    # --------------------------------------------------------------------------------------------------------------------------------------------
    fig, ax = plt.subplots(1, 2,figsize=(12,6), sharex=True) 
    fig.suptitle(f'{serie}{list}', fontsize=16)
    ax[0].axhline(0, linestyle = "--" , c="k") # horizontal line at energy = 1 
    ax[0].axvline(0, linestyle = "--" , c="k")
    ax[0].set_ylabel('Intensity')
    ax[0].set_xlabel('Magnetic field(Gauss)')
    ax[0].set_title("find best lmoke")
    for i in range(len(data)):
        ax[0].plot(
            data[i][0][0],data[i][0][1],'.',
            label = f"{lmoke_files[i]}",
            color = colors[i],)
    ax[0].legend(frameon = False, loc='center left', bbox_to_anchor=(1, 0.5))
    fig.tight_layout()
    plt.show()

# ----------------------------------------------------DATA with errorbars - plotfunction -----------------------------------------------------

# moke\ap_Pt3(Co88Tb12)XPt3_P(Co)90W_p(Ar)1,5microbar_3

# serie = ["ap_Pt3(Co88Tb12)XPt3_P(Co)90W_p(Ar)1,5microbar_3"]
# list = [["75nm"]]
# plotfunction(serie,list)
# list = [["100nm"]]
# plotfunction(serie,list)
# list = [["150nm"]]
# plotfunction(serie,list)


# # # ap_Pt3orTa3(Co88Tb12)XPt3_P(Co)90W_p(Ar)1,56microbar changing the thickness made by AP pressure of argon MKS= 1.5 microbar
# serie = ["ap_Pt3orTa3(Co88Tb12)XPt3_P(Co)90W_p(Ar)1,56microbar"]
# list = [["Ta_50nm"]]
# plotfunction(serie,list)

# # # ap_Pt3orTa3(Co88Tb12)XPt3_P(Co)90W_p(Ar)1,56microbar changing the thickness made by AP pressure of argon MKS= 1.5 microbar
# serie = ["ap_Pt3orTa3(Co88Tb12)XPt3_P(Co)90W_p(Ar)1,56microbar"]
# list = [["Pt_50nm"]]
# plotfunction(serie,list)

# # # ap_Pt3orTa3(Co88Tb12)XPt3_P(Co)90W_p(Ar)1,56microbar changing the thickness made by AP pressure of argon MKS= 1.5 microbar
# serie = ["ap_Pt3orTa3(Co88Tb12)XPt3_P(Co)90W_p(Ar)1,56microbar"]
# list = [[ "Ta_75nm"]]
# plotfunction(serie,list)

# # # ap_Pt3orTa3(Co88Tb12)XPt3_P(Co)90W_p(Ar)1,56microbar changing the thickness made by AP pressure of argon MKS= 1.5 microbar
# serie = ["ap_Pt3orTa3(Co88Tb12)XPt3_P(Co)90W_p(Ar)1,56microbar"]
# list = [["Pt_75nm"]]
# plotfunction(serie,list)

# # # ap_Pt3orTa3(Co88Tb12)XPt3_P(Co)90W_p(Ar)1,56microbar changing the thickness made by AP pressure of argon MKS= 1.5 microbar
# serie = ["ap_Pt3orTa3(Co88Tb12)XPt3_P(Co)90W_p(Ar)1,56microbar"]
# list = [[ "Ta_100nm"]]
# plotfunction(serie,list)

# # # ap_Pt3orTa3(Co88Tb12)XPt3_P(Co)90W_p(Ar)1,56microbar changing the thickness made by AP pressure of argon MKS= 1.5 microbar
# serie = ["ap_Pt3orTa3(Co88Tb12)XPt3_P(Co)90W_p(Ar)1,56microbar"]
# list = [[ "Pt_100nm"]]
# plotfunction(serie,list)


# # # ap_Pt3orTa3(Co88Tb12)XPt3_P(Co)90W_p(Ar)1,56microbar changing the thickness made by AP pressure of argon MKS= 1.5 microbar
# serie = ["ap_Pt3orTa3(Co88Tb12)XPt3_P(Co)90W_p(Ar)1,56microbar"]
# list = [[ "Ta_150nm"]]
# plotfunction(serie,list)

# # ap_Pt3orTa3(Co88Tb12)XPt3_P(Co)90W_p(Ar)1,56microbar changing the thickness made by AP pressure of argon MKS= 1.5 microbar
serie = ["ap_Pt3orTa3(Co88Tb12)XPt3_P(Co)90W_p(Ar)1,56microbar"]
list = [[ "Pt_150nm"]]
plotfunction(serie,list)

