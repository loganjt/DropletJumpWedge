import os, glob, numpy as np, csv
import matplotlib.pyplot as plt
from scipy import signal, fftpack

wrkdir = 'Y:\Projects\DropletJumpWedge\Repos_Data\data'
csv_files = wrkdir+'\\*.csv'
meta_files = wrkdir+'\\*.txt'
trackdata = glob.glob(csv_files)
metadata = glob.glob(meta_files)
n_files = np.size(trackdata)




def get_drop_vars(metadata):
    f = open(metadata[0],"r")
    drop_vars = list(csv.reader(f))
    f.close()
    
    
    drop_meta = {}
    for i in range(n_files):
        drop_meta[drop_vars[i+1][0]] = {}
        n_meta = np.size(drop_vars[0][1:])
        for n in range(n_meta):
            drop_meta[drop_vars[i+1][0]][drop_vars[0][n+1].split('_')[0]] = float(drop_vars[i+1][n+1])

    meta = drop_meta
    return meta



def gen_data_repos(wrkdir,csv_files,trackdata,n_files):
    
    total_drop_data = {}
    
    
    for i in range(n_files):
        (location, name) = os.path.split( trackdata[i] )
        
        f = open(trackdata[i],"r")
        drop_data = list(csv.reader(f))
        f.close()
        
        col_names = drop_data[0]
        n_col = np.size(drop_data[0])
        drop_data = np.asarray(drop_data[1:],dtype=float)
        total_drop_data[name[:-4]] = {}
        for j in range(n_col):
            total_drop_data[name[:-4]][col_names[j]] = drop_data[:,j]

    return total_drop_data
data = gen_data_repos(wrkdir,csv_files,trackdata,n_files)
meta = get_drop_vars(metadata)


class outlier_mask(object):
    def __init__(self,outlier=True):
        self.outlier = outlier
    

def plot_data(data,meta,volumes,location):
    fig = plt.figure(facecolor="white")
    plt.style.use('classic')
    font = {'family' : 'Times New Roman',
            'weight' : 'bold',
            'size'   : 16}
    plt.rc('font',**font)
    
    for key in sorted(data):
        drop_num = key
        if(meta[drop_num]['Volume'] in volumes ):
            if(meta[drop_num]['Volume'] == 0.5):
                color = 'r'
            elif(meta[drop_num]['Volume'] == 1.0):
                color = 'k'
            elif(meta[drop_num]['Volume'] == 2.0):
                color = 'b' 
                
            ax = fig.add_subplot(1,1,1)
            ax.plot(data[drop_num]['time'],data[drop_num][location],c=color,marker='.',linestyle='None',\
                    label=str(meta[drop_num]['Volume'])+'ml '+str( meta[drop_num]['ILback'])+'mm '+drop_num)
            
            ax.spines['right'].set_color('none')
            ax.spines['top'].set_color('none')
            ax.yaxis.set_ticks_position('left')
            ax.xaxis.set_ticks_position('bottom')
            ax.minorticks_on()
            
            ax.legend(bbox_to_anchor=(1, 1),loc='upper left',frameon=False,fontsize=12,facecolor="white")
            
            ax.set_xlabel('t (s)',fontsize=18)
            ax.set_ylabel('x (mm)',fontsize=18)
            
            ax.grid(b=True,which='major')
            ax.grid(b=True,which='minor')
    plt.show()
    



def filtering_data(data,meta,volumes,angles,location):
    fig1 = plt.figure(facecolor="white")
    fig2 = plt.figure(facecolor="white")
    plt.style.use('classic')
    font = {'family' : 'Times New Roman',
            'weight' : 'bold',
            'size'   : 16}
    plt.rc('font',**font)
    
    for key in sorted(meta, key = lambda x: meta[x]['ILback']):
        if(meta[key]['Volume'] in volumes and meta[key]['Angle'] in angles):
            if(meta[key]['Volume'] == 0.5):
                color = 'k'
                style = None
            elif(meta[key]['Volume'] == 1.0):
                color = 'c'
                style = None
            elif(meta[key]['Volume'] == 2.0):
                color = 'b'
                style = None
            
            dat = data[key][location][1:] 
            t = data[key]['time'][1:]
        
            slice_num = 5
            dat_sliced = dat[::slice_num]
            t_sliced = t[::slice_num]
            
            nn = int((np.ceil(np.size(dat_sliced)/2))*2-1)
            nn2 = nn-10
            nn3 = nn2-2
            

            poly_fit = 4
            x1 = signal.savgol_filter(dat_sliced,nn,poly_fit)
            x2 = signal.savgol_filter(x1,nn2,poly_fit)
            x3 = signal.savgol_filter(x2,nn3,poly_fit)
            xf = signal.savgol_filter(x3,slice_num+2,poly_fit)
            print('nn1='+str(nn)+' nn2='+str(nn2)+' nn3='+str(nn3))

            
            ax = fig1.add_subplot(1,1,1)
            ax.plot(t_sliced,dat_sliced,'o',label=key+' '+str(meta[key]['Volume'])+'ml '+str(meta[key]['Angle'])+'deg '+str( meta[key]['ILback'])+'mm ')
            ax.plot(t_sliced,xf,c=color,marker=style)

            ax.spines['right'].set_color('none')
            ax.spines['top'].set_color('none')
            ax.yaxis.set_ticks_position('left')
            ax.xaxis.set_ticks_position('bottom')
            ax.minorticks_on()

            legend1 = ax.legend(bbox_to_anchor=(1, 1),loc='upper left',frameon=False,fontsize=12)
            legend1.get_frame().set_facecolor('white')

            ax.set_xlabel('t (s)',fontsize=18)
            ax.set_ylabel('x (mm)',fontsize=18)
            
            ax.grid(b=True,which='major')
            ax.grid(b=True,which='minor')
            
            dxdt_savgol = np.zeros(np.size(dat_sliced)-2)
            for i in range(np.size(dat_sliced)-2):
                dxdt_savgol[i] = (xf[i+2]-xf[i])/(2*(t_sliced[i+1]-t_sliced[i]))
                
            
            dxdt_centraldiff = np.zeros(np.size(dat_sliced)-2)
            for i in range(np.size(dat_sliced)-2):
                dxdt_centraldiff[i] = (dat_sliced[i+2]-dat_sliced[i])/(2*(t_sliced[i+1]-t_sliced[i]))
                
                
            ax2 = fig2.add_subplot(1,1,1)
            ax2.plot(t_sliced[1:-1],dxdt_centraldiff,'.',marker='o',label=key+' '+str(meta[key]['Volume'])+'ml '\
                     +str(meta[key]['Angle'])+'deg '+str( meta[key]['ILback'])+'mm ')
            ax2.plot(t_sliced[1:-1],dxdt_savgol,c=color,marker=style,label=key+' '+str(meta[key]['Volume'])+'ml '+str(meta[key]['Angle'])+'deg '+str( meta[key]['ILback'])+'mm ')

            ax2.spines['right'].set_color('none')
            ax2.spines['top'].set_color('none')
            ax2.yaxis.set_ticks_position('left')
            ax2.xaxis.set_ticks_position('bottom')
            ax2.minorticks_on()
            
            legend2 = ax2.legend(bbox_to_anchor=(1, 1),loc='upper left',frameon=False,fontsize=12)
            legend2.get_frame().set_facecolor('white')

            ax2.set_xlabel('t (s)',fontsize=18)
            ax2.set_ylabel('v (mm/s)',fontsize=18)

            ax2.grid(b=True,which='major')
            ax2.grid(b=True,which='minor')
            ax2.set_xlim([0,2.1])
#            ax2.set_ylim([0,150])
            
            fig1.savefig('Figures/positions.png',dpi=100,bbox_extra_artists=(legend1,), bbox_inches='tight')
            fig2.savefig('Figures/velocities.png',dpi=100,bbox_extra_artists=(legend2,), bbox_inches='tight')
            
def noise_fft(data,meta):
    y = data['07241']['back']
    t = data['07241']['time']
    
    dxdt_centraldiff = np.zeros(np.size(y)-2)
    for i in range(np.size(y)-2):
        dxdt_centraldiff[i] = (y[i+2]-y[i])/(2*(t[i+1]-t[i]))
        
    p = np.polyfit(t,y,3)
    y_osci = y - np.polyval(p,t)
    
    n = len(y_osci)
    k = np.arange(n)
    T = n/59.94
    frq = k/T
    frq = frq[range(int(n/2))]
    
    Y = np.fft.fft(y_osci)/n
    Y = Y[range(int(n/2))]
    
    fig3 = plt.figure(1,1,1)
    ax3 = fig3.add_subplot(1,1,1)
#    plt.plot(t,y_osci,'-*')
#    plt.plot(frq,abs(Y),'r')
#    ax[0].plot(t,y)
#    ax3.plot(t[1:-1],dxdt_centraldiff,'*')


location = 'back'
volumes = [0.5]
angles= [2.0,3.5]
data = gen_data_repos(wrkdir,csv_files,trackdata,n_files)
meta = get_drop_vars(metadata)
#plot_data(data,meta,volumes,location)
filtering_data(data,meta,volumes,angles,location)
noise_fft(data,meta)

