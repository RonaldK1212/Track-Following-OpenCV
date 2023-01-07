import numpy as np
import cv2
try: import movement as m
except: pass
import time

IMAGE_W = 640
IMAGE_H = 480
FPS = 60

video_capture = cv2.VideoCapture(1)

video_capture.set(cv2.CAP_PROP_FRAME_WIDTH, IMAGE_W)
video_capture.set(cv2.CAP_PROP_FRAME_HEIGHT, IMAGE_H)
#video_capture.set(cv2.CAP_PROP_EXPOSURE, -4)
video_capture.set(cv2.CAP_PROP_EXPOSURE, -5)
video_capture.set(cv2.CAP_PROP_FPS, FPS)




#USED TO CREATE A TRACKBAR FOR TESTING VALUES
def nothing(_):
    pass
cv2.namedWindow('trackbar')
cv2.createTrackbar('region_left', 'trackbar', 180, IMAGE_W, nothing)
cv2.createTrackbar('region_right', 'trackbar', 460, IMAGE_W, nothing)




#Bottom Left - Bottom Right - Top Left - Top Right
src = np.float32([[0, IMAGE_H], [IMAGE_W, IMAGE_H], [0, 0], [IMAGE_W, 0]])
dst = np.float32([[(IMAGE_W/2)-80, IMAGE_H], [(IMAGE_W/2)+80, IMAGE_H], [0, 0], [IMAGE_W, 0]])
M = cv2.getPerspectiveTransform(src, dst) # The transformation matrix
Minv = cv2.getPerspectiveTransform(dst, src) # Inverse transformation

theta = 0
center = 95
k = 2.5

region_threshold = 0





while True:
    
    theta = 0
    ret,orig_frame = video_capture.read()
    cv2.imshow('original',orig_frame)
    

    frame = orig_frame#[-65:-90,:]
    frame = 255 - frame
    frame = cv2.warpPerspective(frame, M, (IMAGE_W, IMAGE_H)) # Image warping
    frame = frame[-220:-120 , :]
    frame = 255 - frame
    blur = cv2.GaussianBlur(frame, (5,5), 3)
    gray = cv2.cvtColor(blur, cv2.COLOR_BGR2GRAY)

    #adaptiveThreshold(src: Mat, maxValue: Any, adaptiveMethod: Any, thresholdType: Any, blockSize: Any, C: Any, dts: Mat = ...)
    #thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV,9,2)
    ret, thresh = cv2.threshold(gray, 120, 255, cv2.THRESH_BINARY_INV)
    #Canny(InputArray image, OutputArray edges, double threshold1, double threshold2, int apertureSize=3, bool L2gradient=false)
    #dst = cv2.Canny(thresh, 50, 255, None, 3)
    contours,hierarchy = cv2.findContours(thresh.copy(), 1, cv2.CHAIN_APPROX_NONE)
    

    r_contours = []
    angles = []
    centers = []
    error = 0

    region_left = cv2.getTrackbarPos('region_left','trackbar')
    region_right = cv2.getTrackbarPos('region_right','trackbar')
    if len(contours) > 0:
        
        for n,c in enumerate(contours): # Filter contours and analyze them
            
            if cv2.contourArea(c) < 200:
                continue
            Mo = cv2.moments(c)
            try:
                cx = int(Mo['m10']/Mo['m00'])
                cy = int(Mo['m01']/Mo['m00'])
            except:
                pass
            
            cv2.line(frame, (cx+40, cy+40), (cx-40, cy-40), (255, 150, 0),1)
            cv2.line(frame, (cx+40, cy-40), (cx-40, cy+40), (255, 150, 0),1)
            cv2.drawContours(frame, c, -1, (255, 255, 0))
            cv2.line(frame, (region_left, 0), (region_left, IMAGE_H), (0,0,255), 2)
            cv2.line(frame, (region_right, 0), (region_right, IMAGE_H), (0,0,255), 2)
            
            rect = cv2.minAreaRect(c)
            center,(width,height),angle = rect
            
            box = cv2.boxPoints(rect)
            box = np.int0(box)
            cv2.drawContours(frame, [box], 0, (0,255,255), 2)
            r_contours.append(c)
            if width < height:
                angle = angle+90
            angles.append(angle)
            centers.append(cx)
        try:
            theta = (sum(angles)/len(angles))-90
        except:
            theta = 0
        
        centers.sort()

        for i,center in enumerate(centers):
            print(f"Center x{i+1}:", center, end="\t")

        

        if len(centers) == 1:
            if centers[0] < IMAGE_W/2:
                error = region_left - centers[0]
            else:
                error = region_right - centers[0]

        if len(centers) >= 2:
            error = IMAGE_W/2 - np.mean(centers)

        #error = -error

        print("Error: ", error)
        

        m.move_servo(95-error)
        #m.forward(15)
        


    
    cv2.imshow('process',thresh)
    cv2.imshow('output',frame)
    #time.sleep(1/FPS)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        #m.stop_moving()
        break
