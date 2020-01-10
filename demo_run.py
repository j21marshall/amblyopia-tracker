
# coding: utf-8

# In[ ]:

import numpy as np
#import serial
import binascii
from scipy import ndimage
import matplotlib.pyplot as plt
from time import sleep
from PIL import ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True

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

def new_pupil(im, justimage=False, saveto=''):
    #This function takes the original image, applies trans,
    #and, for justimage=False, returns the coordinates of the pupil;
    #for justimage=True, the function instead returns an image of the eye
    #with the pupil marked for demonstration
    
    trim10 = trans(im)
    co_x, co_y = [], []
    target = np.amin(trim10) #Generally close to 0
    prec = .45
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
            ax.add_patch(plt.Circle([np.median(co_x),np.median(co_y)],20,color='r'))
        plt.imshow(trim10,cmap='bone')
        if saveto == '':
            plt.show()
        else:
            plt.savefig(saveto)

def pupil_from_serial(file, saveat = ''):
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
    if saveat == '':
        for i in range(n_ims):
            exec('im'+str(i)+' = ndimage.imread(\'sr_'+str(i)+'.jpg\', flatten=True)')
            exec('new_pupil(im'+str(i)+', justimage=True)')
    else:
        for i in range(n_ims):
            exec('im'+str(i)+' = ndimage.imread(\'sr_'+str(i)+'.jpg\', flatten=True)')
            exec('new_pupil(im'+str(i)+', justimage=True, saveto=\'im'+str(i)+saveat+'.png\')')        
        
ts_1 = np.array([[ndimage.imread('images/Sarah/Sarah1right.jpg',flatten=True),
                  ndimage.imread('images/Sarah/Sarah4left.jpg',flatten=True)],
                  [ndimage.imread('images/Sarah/Sarah1right.jpg',flatten=True),
                  ndimage.imread('images/Sarah/Sarah4left.jpg',flatten=True)],
                  [ndimage.imread('images/Sarah/Sarah2right.jpg',flatten=True),
                  ndimage.imread('images/Sarah/Sarah2left.jpg',flatten=True)],
                  [ndimage.imread('images/Sarah/Sarah1right.jpg',flatten=True),
                  ndimage.imread('images/Sarah/Sarah4left.jpg',flatten=True)],
                  [ndimage.imread('images/Sarah/Sarah3right.jpg',flatten=True),
                  ndimage.imread('images/Sarah/Sarah4left.jpg',flatten=True)],
                  [ndimage.imread('images/Sarah/Sarah3right.jpg',flatten=True),
                  ndimage.imread('images/Sarah/Sarah2left.jpg',flatten=True)]])
ts_2 = np.array([[ndimage.imread('images/Jordan/jordan2right.jpg',flatten=True),
                  ndimage.imread('images/Jordan/jordan2left.jpg',flatten=True)],
                  [ndimage.imread('images/Jordan/jordan2right.jpg',flatten=True),
                  ndimage.imread('images/Jordan/jordan2left.jpg',flatten=True)],
                  [ndimage.imread('images/Jordan/jordan2right.jpg',flatten=True),
                  ndimage.imread('images/Jordan/jordan2left.jpg',flatten=True)],
                  [ndimage.imread('images/Jordan/jordan2right.jpg',flatten=True),
                  ndimage.imread('images/Jordan/jordan2left.jpg',flatten=True)],
                  [ndimage.imread('images/Jordan/jordan2right.jpg',flatten=True),
                  ndimage.imread('images/Jordan/jordan2left.jpg',flatten=True)],
                  [ndimage.imread('images/Jordan/jordan2right.jpg',flatten=True),
                  ndimage.imread('images/Jordan/jordan2left.jpg',flatten=True)]])
ts_3 = np.array([[ndimage.imread('images/Jordan/jordan2right.jpg',flatten=True),
                  ndimage.imread('images/Jordan/jordan2left.jpg',flatten=True)],
                  [ndimage.imread('images/Jordan/jordan2right.jpg',flatten=True),
                  ndimage.imread('images/Jordan/jordan3left.jpg',flatten=True)],
                  [ndimage.imread('images/Jordan/jordan2right.jpg',flatten=True),
                  ndimage.imread('images/Jordan/jordan2left.jpg',flatten=True)],
                  [ndimage.imread('images/Jordan/jordan2right.jpg',flatten=True),
                  ndimage.imread('images/Jordan/jordan3left.jpg',flatten=True)],
                  [ndimage.imread('images/Jordan/jordan2right.jpg',flatten=True),
                  ndimage.imread('images/Jordan/jordan2left.jpg',flatten=True)],
                  [ndimage.imread('images/Jordan/jordan2right.jpg',flatten=True),
                  ndimage.imread('images/Jordan/jordan3left.jpg',flatten=True)]]) 

#Guide: ts_1 is a simulated lazy eye with frames from the Sarah set
#ts_2 is a null case where there is no eye movement from the Jordan set
#ts_3 is a simulated twitch of the left eye from the Jordan set

ts = ts_1

print('Right eye frames')
for i, t in enumerate(ts[:,0]):
    sp = 'annotated_images/imr'+str(i)+'.png'
    new_pupil(t, justimage=True, saveto=sp)
    #new_pupil(t, justimage=True)
print('Left eye frames')
for i, t in enumerate(ts[:,1]):
    sp = 'annotated_images/iml'+str(i)+'.png'
    new_pupil(t, justimage=True, saveto=sp)
    #new_pupil(t, justimage=True)

ts_1_in = np.zeros([len(ts[:,0]),4])
for t in range(len(ts_1[:,0])):
    ts_1_in[t,0:2] = new_pupil(ts[t,0])
    ts_1_in[t,2:4] = new_pupil(ts[t,1])

print(ts_1_in)

#analysis
f = ts_1_in
#print(f)

#print(f[0,1])
n = len(f[:,1])

##df = np.zeros([n-1, 4])

diff = np.zeros([n-1, 2])
##for x in range(len(f[:,1])):
  ##  for y in range(len(f[1,:])):
   ##     df[x,y] = f[x,y+1]-f[x,y]

df =  f-np.roll(f,1,axis=0)

diff[:, 0] = abs(df[1:, 0]-df[1:, 2])
diff[:,1] = abs(df[1:, 1]-df[1:, 3])

threshold = 14

print('\n------------\nREPORT\n------------\n')

diffbin = np.copy(diff)
#diff = diff/np.amax(diff)
for x in range(len(diff[:,1])):
    for y in range(len(diff[1,:])):
        mag = np.amax(f[x:x+1,:])/50
        diffbin[x,y] = int(diff[x,y]/mag)
        if diffbin[x,y] >= 1:
            if y == 0:
                print('Horizontal desynchronized movement at tick '+str(x)+' has magnitude '+str(diffbin[x,y]))
            else:
                print('Vertical desynchronized movement at tick '+str(x)+' has magnitude '+str(diffbin[x,y]))

if np.mean(diffbin) <= 1 or np.median(diffbin) <= 1:
    print('\nNo serious desynchronization detected')
else:
    print('\nThere has been significant desynchronization of mean magnitude '+str(int(np.mean(diffbin))))

