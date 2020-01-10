import numpy as np
import scipy as si
from scipy import ndimage
import matplotlib.pyplot as plt

im2 = np.log(ndimage.imread('2.jpg', flatten=True))
plt.imshow(im2, cmap='bone', origin='lower')
plt.show()
plt.imshow(np.exp(im2), cmap='bone', origin='lower')
plt.show()
plt.imshow(np.log(im2), cmap='bone', origin='lower')
plt.show()
plt.imshow(np.arctan(im2), cmap='bone', origin='lower')
plt.show()

test = np.arctan(im2)[200:1000,100:1200]
test = abs(test-np.amax(test))

pupil_test = ndimage.center_of_mass(test)
fig,ax = plt.subplots(1)
ax.set_aspect('equal')
circ = plt.Circle(pupil_test,50, color = 'c')
ax.add_patch(circ)
plt.imshow(test, cmap='bone', origin='lower')
plt.show()

pupil_new = pupil_test[0]+200,pupil_test[1]+100
fig,ax = plt.subplots(1)
circ = plt.Circle(pupil_test,100, color = 'c')
ax.add_patch(circ)
plt.imshow(im2, cmap='bone', origin='lower')
plt.show()
print(pupil_test)
print(pupil_new)