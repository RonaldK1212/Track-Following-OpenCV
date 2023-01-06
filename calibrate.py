import numpy as np
import cv2
import matplotlib.pyplot as plt


#video_capture = cv2.VideoCapture(1)
#video_capture.set(cv2.CAP_PROP_FRAME_WIDTH, 800)
#video_capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 600)
#video_capture.set(cv2.CAP_PROP_EXPOSURE, -4)



IMAGE_H = 1080
IMAGE_W = 1920

src = np.float32([[0, IMAGE_H], [IMAGE_W, IMAGE_H], [0, 0], [IMAGE_W, 0]])
dst = np.float32([[600, IMAGE_H], [1300, IMAGE_H], [0, 0], [IMAGE_W, 0]])
M = cv2.getPerspectiveTransform(src, dst) # The transformation matrix
Minv = cv2.getPerspectiveTransform(dst, src) # Inverse transformation

img = cv2.imread('test.jpg') # Read the test img
img = img[450:(450+IMAGE_H), 0:IMAGE_W] # Apply np slicing for ROI crop
warped_img = cv2.warpPerspective(img, M, (IMAGE_W, IMAGE_H)) # Image warping
plt.imshow(cv2.cvtColor(warped_img, cv2.COLOR_BGR2RGB)) # Show results
plt.show()
