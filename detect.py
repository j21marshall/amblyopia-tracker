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
    return [np.mean(co_x)+ylow,np.mean(co_y)+xlow]
    #return [np.mean(co_x)+xlow,np.mean(co_y)+ylow]

#print(pupil_coords(im_t, 200, 1000, 200, 1000))

def trans(im):
    #imnew = -np.exp(-im/np.mean(im))
    #imnew = np.arctan((imnew-np.amin(imnew))/(np.amax(imnew)-np.amin(imnew)))
    imnew = np.arctan((im-np.amin(im))/(np.amax(im)-np.amin(im)))
    imnew = np.exp(-(imnew-np.mean(imnew))/np.mean(imnew))
    imnew = -imnew/np.amax(imnew)
    #imnew = np.exp(-imnew/np.mean(imnew))
    return imnew

def new_pupil(im):
    trim10 = trans(im)
    fig,ax = plt.subplots(1)
    co_x, co_y = [], []
    newmin = 0
    target = np.amin(trim10)
    prec = .3
    slide = 50
    xhigh, xlow, yhigh, ylow = len(trim10[:,0])-slide, 0+slide, len(trim10[0,:])-slide, 0+slide
    for i in np.arange(0,int((xhigh-xlow)/20))*20:
        for k in np.arange(0,int((yhigh-ylow)/20))*20:
            valhere = np.mean(trim10[i:i+20,k:k+20])
            if valhere < target+prec:
                co = [int(k+10),int(i+10)]
                co_x.append(co[0]); co_y.append(co[1])
                circ = plt.Circle(co,10,color='c')
                ax.add_patch(circ)
    if co_x == []:
        plt.text(int(xhigh/2),int(yhigh/2),'This is a blink')
    else:
        ax.add_patch(plt.Circle([np.mean(co_x),np.mean(co_y)],20,color='r'))
    plt.imshow(trim10,cmap='bone')
    plt.show()

#print('images9.jpg')
im9 = ndimage.imread('images/9.jpeg', flatten=True)
im10 = ndimage.imread('images/10.jpeg', flatten=True)
im12 = ndimage.imread('images/12.jpeg', flatten=True)
im13 = ndimage.imread('images/13.jpeg', flatten=True)

new_pupil(im10)
new_pupil(im12)
new_pupil(im9)
new_pupil(im13)