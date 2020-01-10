import numpy as np
import scipy as si
from scipy import ndimage
import matplotlib.pyplot as plt

def pupil_coords(im, xlow, xhigh, ylow, yhigh, prec=.1):
    co = [0,0]
    imnew = im[int(xlow):int(xhigh),int(ylow):int(yhigh)]
    co_x, co_y = [], []

    target = np.amin(imnew)
    #fig,ax = plt.subplots(1)
    for i in np.arange(0,int((xhigh-xlow)/20))*20:
        for k in np.arange(0,int((yhigh-ylow)/20))*20:
            if np.mean(imnew[i:i+20,k:k+20]) < target+prec:
                co = [int(k+10),int(i+10)]
                co_x.append(co[0]); co_y.append(co[1])
                #circ = plt.Circle(co,20,color='c')
                #ax.add_patch(circ)
    #ax.add_patch(plt.Circle([np.mean(co_x),np.mean(co_y)],40,color='r'))
    #plt.imshow(imnew, cmap='bone', origin='lower')
    #plt.show()
    #return [np.mean(co_x),np.mean(co_y)]
    return [np.mean(co_x)+xlow,np.mean(co_y)+ylow]

#print(pupil_coords(im_t, 200, 1000, 200, 1000))

def trans(im):
    #imnew = -np.exp(-im/np.mean(im))
    #imnew = np.arctan((imnew-np.amin(imnew))/(np.amax(imnew)-np.amin(imnew)))
    imnew = np.arctan((im-np.amin(im))/(np.amax(im)-np.amin(im)))
    imnew = np.exp(-(imnew-np.mean(imnew))/np.mean(imnew))
    imnew = -imnew/np.amax(imnew)
    #imnew = np.exp(-imnew/np.mean(imnew))
    return imnew