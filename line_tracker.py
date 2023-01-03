import numpy as np
import cv2

video_capture = cv2.VideoCapture(0)
video_capture.set(3, 800)
video_capture.set(4, 600)
video_capture.set(cv2.CAP_PROP_FPS, 5)


while(True):
    ret, frame = video_capture.read()
    crop_img = frame#[350:-50, :]
    gray = cv2.cvtColor(crop_img, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray,(11,11),0)
    ret,thresh = cv2.threshold(blur,70,255,cv2.THRESH_BINARY_INV)
    contours,hierarchy = cv2.findContours(thresh.copy(), 1, cv2.CHAIN_APPROX_NONE)
    #crop_img = thresh
    if len(contours) > 0:
        
        #print(len(contours))
        for n,c in enumerate(contours):
#            c = max(contours, key=cv2.contourArea)
            if cv2.contourArea(c) < 400:
                continue

            M = cv2.moments(c)
            try:
                cx = int(M['m10']/M['m00'])
                cy = int(M['m01']/M['m00'])
            except:
                pass

            
            
            cv2.line(crop_img, (cx+40, cy+40), (cx-40, cy-40), (255,150,0),1)
            cv2.line(crop_img, (cx+40, cy-40), (cx-40, cy+40), (255,150,0),1)
            cv2.drawContours(crop_img, c, -1, (255,255,0))
            #x,y,w,h = cv2.boundingRect(c)
            #cv2.rectangle(crop_img, (x,y), (x+w, y+h), (0,0,255), 2)
            
            rect = cv2.minAreaRect(c)
            
            center,_,angle = rect
            
            box = cv2.boxPoints(rect) # cv2.boxPoints(rect) for OpenCV 3.x
            box = np.int0(box)
            cv2.drawContours(crop_img,[box],0,(0,255,255),2)
            print(f"Angle:  {angle}")

        

 

    #Display the resulting frame
    cv2.imshow('frame',crop_img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break