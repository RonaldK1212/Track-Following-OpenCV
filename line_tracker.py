import numpy as np
import cv2
try: import movement as m
except: pass

video_capture = cv2.VideoCapture(0)
video_capture.set(3, 800)
video_capture.set(4, 600)
video_capture.set(cv2.CAP_PROP_EXPOSURE, -4)

video_capture.set(cv2.CAP_PROP_FPS, 5)


def checkCoords(x1, x2):
    error = 400+95 - ((x1+x2)/2)
    distance = 45
    servo_middle = 95
    theta = np.arctan(error*75/(distance*800))
    theta = servo_middle - theta*180/np.pi
    print((x1+x2)/2)
    #m.move_servo(theta)
    

while(True):
    ret, frame = video_capture.read()
    crop_img = frame[50:200, :]
    gray = cv2.cvtColor(crop_img, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5,5),0)
    #ret, thresh = cv2.threshold(blur, 90, 255, cv2.THRESH_BINARY_INV)
    
    kernel = np.ones((7,7),np.uint8)
    
    erosion = cv2.erode(blur, kernel, iterations=1)
    dilation = cv2.dilate(erosion, kernel, iterations=1)
    
    
    
    #crop_img = dilation
    
    
    thresh = cv2.adaptiveThreshold(dilation, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV,15,4)
    contours,hierarchy = cv2.findContours(thresh.copy(), 1, cv2.CHAIN_APPROX_NONE)
    crop_img = thresh
    
    r_contours = []
    angles = []
    centers = []
    if len(contours) > 0:
        
        for n,c in enumerate(contours): # Filter contours and analyze them
            
            if cv2.contourArea(c) < 800:
                continue
            M = cv2.moments(c)
            try:
                cx = int(M['m10']/M['m00'])
                cy = int(M['m01']/M['m00'])
            except:
                pass
            
            cv2.line(crop_img, (cx+40, cy+40), (cx-40, cy-40), (255, 150, 0),1)
            cv2.line(crop_img, (cx+40, cy-40), (cx-40, cy+40), (255, 150, 0),1)
            cv2.drawContours(crop_img, c, -1, (255, 255, 0))
            
            rect = cv2.minAreaRect(c)
            center,_,angle = rect
            
            box = cv2.boxPoints(rect)
            box = np.int0(box)
            cv2.drawContours(crop_img, [box], 0, (0,255,255), 2)
            r_contours.append(c)
            angles.append(angle)
            centers.append((cx, cy))
        
    
                
        print("\n")
        r_contours.sort(key=cv2.contourArea)
        try:
            checkCoords(centers[0][0], centers[0][1])
        except:
            pass
        
        
    cv2.imshow('frame',crop_img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
            
