"""

Logan Torres - updated 7/20/2017

Re-formats two text Spotlight-16 tracking files for front and back profile 
thresholds of droplet. Experiment variables are aquired from text file name
and scale factor is saved from text file.

Code assumes the frame rate and scale factor are applied before tracking (i.e.
the file contains time, drop_image_label, frame_number, x-position (mm), 
and y-position (mm)). 

csv file is exported to 'data' folder and exp parameters appended to 
'metedata.txt' file located in the 'data' folder. Data and variables are 
referenced by drop #.

"""
import numpy as np
import os, glob, math

wrkdir = os.path.dirname(os.path.realpath('file_generator_Spotlight.py'))
rawdir = os.path.join(wrkdir,'RAW_Spotlight')
datdir = os.path.join(wrkdir,'data')
#wrkdir = 'Y:\Projects\DropletJumpWedge\Repos_Data'
#rawdir = 'Y:\Projects\DropletJumpWedge\Repos_Data\RAW_Spotlight'
#datdir = 'Y:\Projects\DropletJumpWedge\Repos_Data\data'

def read_files():
    os.chdir(wrkdir)
    files = os.listdir(wrkdir)
    M = glob.glob(os.path.join(wrkdir,'*.txt'))
    (filepathb, filenameb) = os.path.split( [s for s in M if s.endswith('back.txt')][0] )  # Back file
    back = open(filenameb,'r')                      # open files to read
    b = back.readlines()                            # read back lines into b, each line is a string
    bdata = b[8:]                                   # take data excluding all header text
    back.close()                                    # close back spotlight file
    
    
    (filepathf, filenamef) = os.path.split( [s for s in M if s.endswith('front.txt')][0] )  # Front file
    front = open(filenamef,'r')                     # open files to read            
    f = front.readlines()                           # read front lines in f, each line is a string
    fdata = f[8:]                                   # take data excluding all header text        
    front.close()                                   # close front spotlight file
    
    filenameback= filenameb[:-9]
    filenamefront= filenamef[:-10]   
    append_to_metadata(bdata,b,fdata,f,filenameback,filenamefront)
    return files
    
def append_to_metadata(bdata,b,fdata,f,filenameback,filenamefront):
    
    # Calculate scale factors from spotlight files
    user = float(f[2].split()[5])
    image = float(f[2].split()[8])
    scale = str(round(user/image,3))

    
    # Pull variables from filename
    parameters_b = filenameback.split('_')
    parameters_f = filenamefront.split('_')
    vol = parameters_b[1][:-2].replace('o','.')
    angl = parameters_b[2][:-3].replace('o','.')
    ILb = parameters_b[3][:-2].replace('o','.')
    ILf = parameters_f[3][:-2].replace('o','.')
    
    l = open(os.path.join(datdir,'metadata.txt'),"a")
    metadata = filenameback[:5]+', '+angl+', '+vol+', '+ILf+', '+ILb+', '+scale+'\n'
    l.write(metadata) 
    l.close()
    
    ILb = float(ILb)
    ILf = float(ILf)
    angl = float(angl)
    convert_format(bdata,fdata,ILb,ILf,angl,filenameback)


def convert_format(bdata,fdata,ILb,ILf,angl,filenameback): 
    # Separate columns of data by space and convert from string to float
    n = np.size(bdata)
    for i in range(n):
        bdata[i] = bdata[i].split()             # splits each line by space
        for j in [0,3,4]:
            bdata[i][j] = float(bdata[i][j])    # converts data to float 
        bdata[i][2] = int(bdata[i][2])
          
    n = np.size(fdata)      
    for i in range(n):
        fdata[i] = fdata[i].split()             # splits each line by space
        for j in [0,2,3,4]:
            fdata[i][j] = float(fdata[i][j])    # converts data to float 
        fdata[i][2] = int(fdata[i][2])
    
    # Remove file names columns   
    for row in fdata:
        del row[1]  
    for row in bdata:
        del row[1]  
    
    # Swap time and frame number columns. Data organized as: 
    # Frame   Time    Xdata   Ydata
    for item in fdata:
        item[0], item[1] = item[1], item[0]   
    for item in bdata:
        item[0], item[1] = item[1], item[0]

    # Match starting and ending frames for front and back data
    [nf,mf] = np.shape(fdata)
    [nb,mb] = np.shape(bdata)   
    if(nf != nb):
        sf, sb = fdata[0][0], bdata[0][0] 
        ef, eb = fdata[nf-1][0], bdata[nb-1][0]
        if(sf>sb):
            bframes = [item[0] for item in bdata]
            start = bframes.index(sf)
            del bdata[:start]
        elif(sf<sb):
            fframes = [item[0] for item in fdata]
            start = fframes.index(sb)
            del fdata[:start]
        if(ef>eb):
            fframes = [item[0] for item in fdata]
            end = fframes.index(eb)
            del fdata[end+1:]
        elif(ef<eb):
            bframes = [item[0] for item in bdata]
            end = bframes.index(ef)  
            del bdata[end+1:]
    else:       # if frames match don't do anything
        bdata = bdata
        fdata = fdata
    process_data(bdata,fdata,ILb,ILf,angl,filenameback)
    
def process_data(bdata,fdata,ILb,ILf,angl,filenameback):
    time = [item[0]/59.94 for item in bdata]
    x_back = np.array([abs(item[2]-bdata[0][2]) for item in bdata])+ILb
    y_back = np.array([abs(item[3]-bdata[0][3]) for item in bdata])
    
    
    x_front = np.array([abs(item[2]-fdata[0][2]) for item in fdata])+ILf
    y_front = np.array([abs(item[3]-fdata[0][3]) for item in fdata])
    
    xave = (x_back+x_front)*0.5
    yave = (y_back+y_front)*0.5
    
    #s_b = ((abs(x_back[0]-x_back))**2. + (abs(y_back[0]-y_back))**2.)**(1./2)
    #s_f = ((abs(x_front[0]-x_front))**2. + (abs(y_front[0]-y_front))**2.)**(1./2)
    s = xave
    s_b = x_back
    s_f = x_front
    
    
    gen_csv_file(time,s,s_b,s_f,filenameback)

def gen_csv_file(time,s,s_b,s_f,filenameback): 
    data_file = os.path.join(wrkdir,filenameback[:5]+'.csv')   
#    data_file = wrkdir+'\\'+filenameback[:5]+'.csv' # filename for tracking data, desig. by drop #
    f = open(data_file,"w+")                    # creates new file in working folder, and close
    f.close()
    
    olddir = os.path.join(wrkdir,filenameback[:5]+'.csv')              # current file location
    newdir = os.path.join(wrkdir,'data',filenameback[:5]+'.csv')
#    newdir = wrkdir+'\\'+'data'+'\\'+filenameback[:5]+'.csv'  # new file location
    os.rename(olddir,newdir) # moves processed data folder to 'data' folder
         
    f = open(newdir,"w+")
    f.write("time,back,front,average\n")
    time = np.array(time)
    s = np.array(s)
    sb = np.array(s_b)
    sf = np.array(s_f)
    m = np.size(time)
    for i in range(m):
        t = str(time[i])
        x = str(s[i])
        xb = str(sb[i])
        xf = str(sf[i])
        line_data = t + "," + xb + "," + xf + "," + x + "\n"
        f.write(line_data)
    f.close()
    
    
def relocate_raw_files(files):
    # move spotlight files to RAW folder
    for j in files:
        if(j.endswith(".txt")):
            source = wrkdir+'\\'+j
            dest = rawdir+'\\'+j
            os.rename(source,dest)

files = read_files()
relocate_raw_files(files)

