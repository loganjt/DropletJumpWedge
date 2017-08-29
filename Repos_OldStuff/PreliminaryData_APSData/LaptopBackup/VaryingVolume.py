import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.ticker as ticker
import numpy as np

data1 = pd.read_csv('Experimental Results/VaryingVolume.csv')

# Numerical time arrays
t = np.array(data1["time"])
# Experimental time arrays
Twoml = np.array(data1["2ml"])/10
Fourml = np.array(data1["4ml"])/10
Sixml = np.array(data1["6ml"])/10

fig = plt.figure(1)
plt.rc('font',family='Times New Roman')
ax = plt.subplot(111)
ax.plot(t, Twoml,'rD', label='3mL', markeredgewidth=0.0)
ax.plot(t, Fourml,'bs', label='4', markeredgewidth=0.0)
ax.plot(t, Sixml,'ko', label='6', markeredgewidth=0.0)


plt.xlabel(r'$t$ (s)', fontsize=22)
plt.ylabel(r'$x$ (cm)', fontsize=22)
plt.xticks(np.arange(0,2.1,0.5))
plt.yticks(np.arange(0,25,5))
#plt.axis([0,2.1,0,20])
plt.legend( loc='upper left', numpoints = 1, fontsize=14, framealpha=0)
plt.text(-0.5,20,'a)',fontsize=22, family='Times New Roman')
ax.tick_params(labelsize=20)
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
ax.yaxis.set_ticks_position('left')
ax.xaxis.set_ticks_position('bottom')
ax.yaxis.set_major_formatter(ticker.FormatStrFormatter('%0.1f'))

plt.show()
fig.savefig('C:/Users/logan/Documents/1 Portland State Graduate School/Capillary Fluidics/DropletJumpInWedge/Paper/Figures/VaryingVolume.pdf',transparent=True,dpi=600,bbox_inches='tight')
fig.savefig('C:/Users/logan/Documents/1 Portland State Graduate School/Capillary Fluidics/DropletJumpInWedge/Paper/Figures/VaryingVolume.png',transparent=True,dpi=600,bbox_inches='tight')
