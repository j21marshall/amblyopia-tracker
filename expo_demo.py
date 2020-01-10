import numpy as np
import serial
import binascii
from scipy import ndimage
import matplotlib.pyplot as plt
from time import sleep
from PIL import ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True

#ser1 = serial.Serial('/dev/ttyACM0',baudrate=38400)
ser1 = serial.Serial('/dev/ttyUSB0',baudrate=38400,timeout=10)
#ser2 = serial.Serial('/dev/ttyACM1',baudrate=38400,timeout=10)
ser2 = serial.Serial('/dev/ttyUSB1',baudrate=38400,timeout=10)

print('\n------------\nBEGINNING CAPTURE\n------------\n')

s_old = 'n'
s_old1 = 'n'
q_old = 'n'
q_old1 = 'n'
im = ''
imr = ''
re = open('sread2.txt','w')
rer = open('sreadr2.txt','w')
#for t in range(30000):
while 1:
    s = ser1.read(1)
    q = ser2.read(1)
    if s:
        im += str(s)
    else:
        break
    if q:
        imr += str(q)
    else:
        break
    #if str(q_old1)+str(q_old)+str(q) == 'End':
    #if str(s_old1)+str(s_old)+str(s) == 'pic':
    #    break
    #print(s,q)
    
    s_old1 = s_old
    s_old = s
    q_old1 = q_old
    q_old = q
#print(imr)
re.write(im)
re.close()
rer.write(imr)
rer.close()
ser1.close()
ser2.close()

print('\n------------\nCAPTURE COMPLETE\n------------\n')

###Pupil detection functions

def trans(im):
    #This function maps the brightness values to a scale that
    #makes features slightly brighter than the pupil in the original image
    #instead significantly brighter. The image elements are normalized so
    #that the precision (prec) parameter in new_pupil can be used
    
    imnew = np.arctan((im-np.amin(im))/(np.amax(im)-np.amin(im)))
    imnew = np.exp(-(imnew-np.mean(imnew))/np.mean(imnew))
    imnew = -imnew/np.amax(imnew) #Normalization
    return imnew

def new_pupil(im, justimage=False):
    #This function takes the original image, applies trans,
    #and, for justimage=False, returns the coordinates of the pupil;
    #for justimage=True, the function instead returns an image of the eye
    #with the pupil marked for demonstration
    
    trim10 = trans(im)
    co_x, co_y = [], []
    target = np.amin(trim10) #Generally close to -1
    prec = .35
    slide = 30
    step = 20
    xhigh, xlow, yhigh, ylow = len(trim10[:,0])-slide, 60, 250, 60
    for i in np.arange(0,int((xhigh-xlow)/step))*step:
        for k in np.arange(int(ylow/step),int(yhigh/step))*step:
            valhere = np.median(trim10[i:i+step,k:k+step])
            if valhere < target+prec:
                co = [int(k+step/2),int(i+step/2)]
                co_x.append(co[0]); co_y.append(co[1])
    if justimage == False:
        if co_x == []: #Blink case; returns a coordinate
            #large enough that the magnitude of the difference
            #in coordinate change between eyes is so small
            #relative to each difference that the analysis
            #will not recognize either this or the next frame
            #as desynchronized
            return [10000,10000]
        else:
            return [np.mean(co_x),np.mean(co_y)]
    else:
        fig,ax = plt.subplots(1)
        if co_x == []:
            plt.text(int(xhigh/2),int(yhigh/2),'This is a blink')
        else:
            ax.add_patch(plt.Circle([np.mean(co_x),np.mean(co_y)],20,color='r'))
        plt.imshow(trim10,cmap='bone')
        plt.show()

def pupil_from_serial(file):
    #This function takes the serial port output,
    #converts out of hexadecimal, fills out frames
    #that did not complete, creates jpg frames,
    #and runs new_pupil pupil detection for each frame
    
    ###Hexadecimal string to jpg
    txtim = open(file,'r').read()+'\n'
    k_s, p_s, q_s = [], [], []
    for i in range(len(txtim)):
        if txtim[i] == '\n': k_s.append(i)
    for i in range(1,len(k_s)):
        if k_s[i]-k_s[i-1] > 100:
            p_s.append(k_s[i-1])
            q_s.append(k_s[i])
    ims = []
    n_ims = len(p_s)
    for i in range(n_ims):
        ims.append(txtim[p_s[i]+6:q_s[i]-4])
    jpgnames = []
    for i in range(n_ims):
        if str(ims[i][-3])+str(ims[i][-2])+str(ims[i][-1]) == 'FD9':
            print('Complete frame')
        else:
            print('Incomplete frame, extrapolating')
            ims[i] += ims[0][len(ims[i]):]
        exec('jpg_'+str(i)+' = open(\'sr_'+str(i)+'.jpg\',\'wb\'); jpgnames.append(jpg_'+str(i)+')')
        exec('jpg_'+str(i)+'.write(binascii.unhexlify(ims['+str(i)+']))')
        exec('jpg_'+str(i)+'.close')
    ###Pupil detection
    new = []
    for i in range(n_ims):
        exec('im'+str(i)+' = ndimage.imread(\'sr_'+str(i)+'.jpg\', flatten=True)')
        exec('new.append(new_pupil(im'+str(i)+', justimage=False))')
        print(new)
    return np.array(new)

print('\n------------\nANALYSIS\n------------\n')

oneeye = pupil_from_serial('sread2.txt')
twoeye = pupil_from_serial('sreadr2.txt')

ts_1_in = np.zeros([len(oneeye[:,0]),4])
ts_1_in[:,:2] = oneeye
ts_1_in[:,2:] = twoeye

#analysis
f = ts_1_in
n = len(f[:,1])

diff = np.zeros([n-1, 2])

df =  f-np.roll(f,1,axis=0)

diff[:, 0] = abs(df[1:, 0]-df[1:, 2])
diff[:,1] = abs(df[1:, 1]-df[1:, 3])

threshold = 14

print('\n------------\nREPORT\n------------\n')

diffbin = np.copy(diff)
#diff = diff/np.amax(diff)
for x in range(len(diff[:,1])):
    for y in range(len(diff[1,:])):
        mag = np.amax(f[x:x+1,:])/10
        diffbin[x,y] = int(diff[x,y]/mag)
        if diffbin[x,y] >= 1:
            if y == 0:
                print('Horizontal desynchronized movement at tick '+str(x)+' has relative magnitude '+str(diffbin[x,y]))
            else:
                print('Vertical desynchronized movement at tick '+str(x)+' has relative magnitude '+str(diffbin[x,y]))
#print(diffbin)
history = open('history.txt','r').read()

allruns = []
for run in range(int(len(history)/10)):
    new = int(history[int(run*10):int(run*10+10)])
    allruns.append(new)

plt.plot(allruns)
plt.title('History of desynchronization')
plt.ylabel('Average desynchronization')
plt.xlabel('Session')
plt.ylim([0,900])

hist = open('history.txt','w')
if np.mean(diffbin) <= 1 or np.median(diffbin) <= 1:
    print('\nNo serious desynchronization detected')
else:
    print('\nThere has been significant desynchronization of mean magnitude '+str(np.mean(diff)))
newval = str(int(np.mean(diffbin)*100))
for i in range(int(10-len(newval))):
    newval = '0'+newval
history = history+newval
hist.write(history)
hist.close()

plt.show()
