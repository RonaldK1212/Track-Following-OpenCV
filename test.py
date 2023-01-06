import numpy as np
import cv2

IMAGE_H = 600
IMAGE_W = 800

video_capture = cv2.VideoCapture(1)
video_capture.set(cv2.CAP_PROP_FRAME_WIDTH, IMAGE_W)
video_capture.set(cv2.CAP_PROP_FRAME_HEIGHT, IMAGE_H)
#video_capture.set(cv2.CAP_PROP_EXPOSURE, -4)
video_capture.set(cv2.CAP_PROP_AUTO_EXPOSURE, 1)
#video_capture.set(cv2.CAP_PROP_FPS, 30)

src = np.float32([[0, IMAGE_H], [IMAGE_W, IMAGE_H], [0, 0], [IMAGE_W, 0]])
dst = np.float32([[(IMAGE_W/2)-IMAGE_W/10, IMAGE_H], [(IMAGE_W/2)+IMAGE_W/10, IMAGE_H], [0, 0], [IMAGE_W, 0]])
M = cv2.getPerspectiveTransform(src, dst) # The transformation matrix
Minv = cv2.getPerspectiveTransform(dst, src) # Inverse transformation

theta = 0

while True:
    ret,orig_frame = video_capture.read()
    
    frame = orig_frame[50:400,:]
    
    frame = cv2.warpPerspective(frame, M, (IMAGE_W, IMAGE_H)) # Image warping
    frame = frame[:-80 , 250:-220]

    blur = cv2.GaussianBlur(frame, (5,5), 3)
    gray = cv2.cvtColor(blur, cv2.COLOR_BGR2GRAY)

    #adaptiveThreshold(src: Mat, maxValue: Any, adaptiveMethod: Any, thresholdType: Any, blockSize: Any, C: Any, dts: Mat = ...)
    thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV,9,5)

    #Canny(InputArray image, OutputArray edges, double threshold1, double threshold2, int apertureSize=3, bool L2gradient=false)
    dst = cv2.Canny(gray, 50, 255, None, 3)

    #HoughLinesP(InputArray image, OutputArray lines, double rho, double theta, int threshold, double minLineLength=0, double maxLineGap=0)
    linesP = cv2.HoughLinesP(dst, 1, np.pi / 180, 50, 20, 20, 20)
    
    if linesP is not None:
        for i in range(0, len(linesP)):
            l = linesP[i][0]
            cv2.line(frame, (l[0], l[1]), (l[2], l[3]), (0,0,255), 2, cv2.LINE_AA)


    output = frame
    cv2.imshow('original',orig_frame)
    cv2.imshow('process',dst)
    cv2.imshow('output',output)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
