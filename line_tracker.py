import numpy as np
import cv2

video_capture = cv2.VideoCapture(0)
video_capture.set(3, 800)
video_capture.set(4, 400)

while(True):
    ret, frame = video_capture.read()
    crop_img = frame#[60:120, 0:160]
    gray = cv2.cvtColor(crop_img, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray,(5,5),0)
    ret,thresh = cv2.threshold(blur,60,150,cv2.THRESH_BINARY_INV)
    contours,hierarchy = cv2.findContours(thresh.copy(), 1, cv2.CHAIN_APPROX_NONE)

    if len(contours) > 0:
        c = max(contours, key=cv2.contourArea)
        M = cv2.moments(c)
        try:
            cx = int(M['m10']/M['m00'])
            cy = int(M['m01']/M['m00'])
        except:
            pass
        cv2.line(crop_img, (cx+40, cy+40), (cx-40, cy-40), (255,150,0),1)
        cv2.line(crop_img, (cx+40, cy-40), (cx-40, cy+40), (255,150,0),1)
       

        if cx >= 120:
            print("Turn Left")

        elif cx < 120 and cx > 50:
            print("On Track")

        elif cx <= 50:
            print("Turn Right")

        else:
            print("No line")

 

    #Display the resulting frame
    cv2.imshow('frame',crop_img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break