import numpy as np
import scipy as si
from skimage import data, color
from skimage.transform import hough_circle
#, hough_circle_peaks
#from skimage.feature import canny
#from skimage.draw import circle_perimeter
from skimage.util import img_as_ubyte

frame = si.ndimage.imread('/home/pi/frames/2.jpg', flatten=True)
#frame = img_as_ubyte('/home/pi/frames/test.jpg')
#frame_t = hough_circle(frame, radius=100)
#si.misc.imsave('/home/pi/frames/test_transform.jpg', frame)
#sx = si.ndimage.sobel(frame, axis=0, mode='constant')
#sy = si.ndimage.sobel(frame, axis=1, mode='constant')
#sob = np.hypot(sx,sy)
sob = si.ndimage.sobel(frame, 0)
threshparam = 1e6
low_vals = sob < np.amax(sob)/threshparam
high_vals = sob >= np.amax(sob)/threshparam
sob[low_vals] = 1
sob[high_vals] = 0
frame_t = hough_circle(frame, radius=np.array(range(100,101)))
si.misc.imsave('/home/pi/frames/2_edges.jpg', sob)
