import numpy as np
import cv2
import movement as m

IMAGE_H = 600
IMAGE_W = 800

video_capture = cv2.VideoCapture(0)
video_capture.set(cv2.CAP_PROP_FRAME_WIDTH, IMAGE_W)
video_capture.set(cv2.CAP_PROP_FRAME_HEIGHT, IMAGE_H)
#video_capture.set(cv2.CAP_PROP_EXPOSURE, -4)
video_capture.set(cv2.CAP_PROP_EXPOSURE, -4)
video_capture.set(cv2.CAP_PROP_FPS, 10)

src = np.float32([[0, IMAGE_H], [IMAGE_W, IMAGE_H], [0, 0], [IMAGE_W, 0]])
dst = np.float32([[(IMAGE_W/2)-IMAGE_W/10, IMAGE_H], [(IMAGE_W/2)+IMAGE_W/10, IMAGE_H], [0, 0], [IMAGE_W, 0]])
M = cv2.getPerspectiveTransform(src, dst) # The transformation matrix
Minv = cv2.getPerspectiveTransform(dst, src) # Inverse transformation

theta = 0
center = 95
k = 2.5

while True:
    theta = 0
    ret,orig_frame = video_capture.read()
    
    frame = orig_frame[50:400,:]
    frame = 255 - frame
    frame = cv2.warpPerspective(frame, M, (IMAGE_W, IMAGE_H)) # Image warping
    frame = frame[200:-100 , 250:-180]
    frame = 255 - frame
    blur = cv2.GaussianBlur(frame, (9,9), 3)
    gray = cv2.cvtColor(blur, cv2.COLOR_BGR2GRAY)

    #adaptiveThreshold(src: Mat, maxValue: Any, adaptiveMethod: Any, thresholdType: Any, blockSize: Any, C: Any, dts: Mat = ...)
    #thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV,9,2)
    ret, thresh = cv2.threshold(gray, 90, 255, cv2.THRESH_BINARY_INV)
    #Canny(InputArray image, OutputArray edges, double threshold1, double threshold2, int apertureSize=3, bool L2gradient=false)
    #dst = cv2.Canny(thresh, 50, 255, None, 3)
    contours,hierarchy = cv2.findContours(thresh.copy(), 1, cv2.CHAIN_APPROX_NONE)
    

    r_contours = []
    angles = []
    centers = []
    if len(contours) > 0:
        
        for n,c in enumerate(contours): # Filter contours and analyze them
            
            if cv2.contourArea(c) < 600:
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
            
            rect = cv2.minAreaRect(c)
            center,(width,height),angle = rect
            
            box = cv2.boxPoints(rect)
            box = np.int0(box)
            cv2.drawContours(frame, [box], 0, (0,255,255), 2)
            r_contours.append(c)
            if width < height:
                angle = angle+90
            angles.append(angle)
            centers.append((cx, cy))
        try:
            theta = (sum(angles)/len(angles))-90
        except:
            theta = 0
        print(f"Angles = {angles}")
        print(f"Theta = {theta}")
        m.move_servo(95+float(theta))
        m.forward(15)
        


    #HoughLinesP(InputArray image, OutputArray lines, double rho, double theta, int threshold, double minLineLength=0, double maxLineGap=0)
    #linesP = cv2.HoughLinesP(dst, 1, np.pi / 180, 50, 20, 20, 20)
    
    #if linesP is not None:
    #    for i in range(0, len(linesP)):
    #        l = linesP[i][0]
    #        x1,y1,x2,y2 = l[0], l[1], l[2], l[3]
    #        cv2.line(frame, (x1, y1), (x2, y2), (0,0,255), 2, cv2.LINE_AA)
            
    #        theta=theta+np.arctan2((y2-y1),(x2-x1))
    
    #angle = center-theta*k
    #print(angle)
    #m.move_servo(angle)
    #output = thresh
    #cv2.imshow('original',orig_frame)
    #cv2.imshow('process',dst)
    cv2.imshow('output',frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        m.stop_moving()
        break
