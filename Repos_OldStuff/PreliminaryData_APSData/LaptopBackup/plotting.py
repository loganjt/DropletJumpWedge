import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.ticker as ticker
import numpy as np

data1 = pd.read_csv('3ml Results.csv')
data2 = pd.read_csv('4ml Results.csv')
# Numerical time arrays
time1_n = np.array(data1["time_n"])
time2_n = np.array(data2["time_n"])
# Experimental time arrays
time1_e = np.array(data1["time_e"])
time2_e = np.array(data2["time_e"])
# Numerical centroid tracking
cent1_n = np.array(data1['cent_xn'])
cent2_n = np.array(data2['cent_xn'])
# Numerical average tracking
ave1_n = np.array(data1["ave_xn"])
ave2_n = np.array(data2["ave_xn"])
# Experimental average tracking
ave1_e = np.array(data1["ave_xe"])
ave2_e = np.array(data2["ave_xe"])

center_ave_error1 = np.multiply(abs(ave1_n-cent1_n),1/cent1_n)*100
center_ave_error1_average = np.mean(center_ave_error1[100::])

fig = plt.figure(1)
plt.rc('font',family='Times New Roman')
ax = plt.subplot(111)
ax.plot(data1["time_n"], data1["cent_xn"],'k-', label='numerical 3mL 1.2$^{\circ}$')
ax.plot(data2["time_n"], data2["cent_xn"],'r-', label='numerical 4mL 3.8$^{\circ}$')
ax.plot(data1["time_e"], data1["ave_xe"],'ko', label='experimental 3mL 1.2$^{\circ}$', fillstyle='none')
ax.plot(data2["time_e"], data2["ave_xe"],'r^', label='experimental 4mL 3.8$^{\circ}$', fillstyle='none')

plt.xlabel(r'$t$ (s)', fontsize=18)
plt.ylabel(r'$x$ (cm)', fontsize=18)
plt.axis([0.0,2.0,0.0,12])
plt.legend( loc='upper left', numpoints = 1, fontsize=12, framealpha=0)

ax.tick_params(labelsize=14)
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
ax.yaxis.set_ticks_position('left')
ax.xaxis.set_ticks_position('bottom')
ax.yaxis.set_major_formatter(ticker.FormatStrFormatter('%0.1f'))

plt.show()
fig.savefig('Figures/comparison.pdf',transparent=True,dpi=600,bbox_inches='tight')
fig.savefig('Figures/comparison.png',transparent=True,dpi=600,bbox_inches='tight')

fig = plt.figure(2)
plt.rc('font',family='Times New Roman')
ax = plt.subplot(111)
ax.plot(data1["time_n"], data1["cent_xn"],'k-', label='centroid 3mL 1.2$^{\circ}$')
ax.plot(data2["time_n"], data2["cent_xn"],'r-', label='centroid 4mL 3.8$^{\circ}$')
ax.plot(time1_n[1::30], ave1_n[1::30],'ko', label='average 3mL 1.2$^{\circ}$', fillstyle='none')
ax.plot(time2_n[1::30], ave2_n[1::30],'ro', label='average 4mL 3.8$^{\circ}$', fillstyle='none')

plt.xlabel(r'$t$ (s)', fontsize=18)
plt.ylabel(r'$x$ (cm)', fontsize=18)
plt.axis([0.0,2.0,0.0,6.5])
plt.legend( loc='upper left', numpoints = 1, fontsize=12, framealpha=0)

ax.tick_params(labelsize=14)
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
ax.yaxis.set_ticks_position('left')
ax.xaxis.set_ticks_position('bottom')
ax.yaxis.set_major_formatter(ticker.FormatStrFormatter('%0.1f'))


plt.show()

fig = plt.figure(2)
plt.rc('font',family='Times New Roman')
ax = plt.subplot(111)
ax.plot(time1_n,center_ave_error1,'k*')
plt.xlabel(r'$t$ (s)', fontsize=18)
plt.ylabel(r'$error$ (%)', fontsize=18)
plt.axis([0.0,2.1,0.0,6])
plt.legend( loc='upper left', numpoints = 1, fontsize=12, framealpha=0)

ax.tick_params(labelsize=14)
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
ax.yaxis.set_ticks_position('left')
ax.xaxis.set_ticks_position('bottom')
ax.yaxis.set_major_formatter(ticker.FormatStrFormatter('%0.1f'))
plt.show()

print center_ave_error1_average

fig.savefig('Figures/centroidaverage.pdf',transparent=True,dpi=600,bbox_inches='tight')
fig.savefig('Figures/centroidaverage.png',transparent=True,dpi=600,bbox_inches='tight')