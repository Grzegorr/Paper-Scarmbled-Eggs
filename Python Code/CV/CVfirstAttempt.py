import cv2
import matplotlib.pyplot as plt
import numpy as np

img1 = cv2.imread('Manual_Tests_Data/BeforeMixing.jpg',1)
cv2.imshow("Before Mixing", img1)
#cv2.waitKey(0)

img2 = cv2.imread('Manual_Tests_Data/BeforeMixingButter.jpg',1)
cv2.imshow("BeforeMixingButter", img2)
#cv2.waitKey(0)

img3 = cv2.imread('Manual_Tests_Data/Mixed.jpg',1)
cv2.imshow("Mixed", img3)
#cv2.waitKey(0)

img4 = cv2.imread('Manual_Tests_Data/HalfScrambled.jpg',1)
cv2.imshow("HalfScrambled", img4)
#cv2.waitKey(0)

img5 = cv2.imread('Manual_Tests_Data/FullScrambled.jpg',1)
cv2.imshow("FullScrambled", img5)
#cv2.waitKey(0)

cv2.destroyAllWindows()

#cv2.imwrite('Manual_Tests_Data/WriteTest.jpg',img1)

img_hsv = cv2.cvtColor(img1,cv2.COLOR_BGR2HSV)
hue = img_hsv[:,:,0]
flat_hue = np.array(hue).flatten()
plt.hist(flat_hue, bins = 180)
plt.show()

img_hsv = cv2.cvtColor(img2,cv2.COLOR_BGR2HSV)
hue = img_hsv[:,:,0]
flat_hue = np.array(hue).flatten()
plt.hist(flat_hue, bins = 180)
plt.show()

img_hsv = cv2.cvtColor(img3,cv2.COLOR_BGR2HSV)
hue = img_hsv[:,:,0]
flat_hue = np.array(hue).flatten()
plt.hist(flat_hue, bins = 180)
plt.show()

img_hsv = cv2.cvtColor(img4,cv2.COLOR_BGR2HSV)
hue = img_hsv[:,:,0]
flat_hue = np.array(hue).flatten()
plt.hist(flat_hue, bins = 180)
plt.show()

img_hsv = cv2.cvtColor(img5,cv2.COLOR_BGR2HSV)
hue = img_hsv[:,:,0]
flat_hue = np.array(hue).flatten()
plt.hist(flat_hue, bins = 180)
plt.show()