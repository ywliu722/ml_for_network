import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


for i in range(2):
    input = f'fps-00{i+1}.txt'
    output = f'fps0{i+1}.png'
    fig11=pd.read_csv(input, sep=" ", header=None)

    fig,ax = plt.subplots(figsize=(15,5),dpi=100,linewidth = 2)
    ax.plot(fig11.index,fig11[0],color = 'r', label="VR Device")
    ax.set_ylabel("fps",color="red",fontsize=14)
    ax.set_ylim(0,50)

    plt.savefig(output)
