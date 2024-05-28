import numpy as np
import cv2
from collections import deque


def setValues(x):#for trackbar function
    print("")

#creating trackbar for marker color;
cv2.namedWindow("Color detectors")
cv2.createTrackbar("Upper Hue","Color detectors",153,180,setValues)
cv2.createTrackbar("Upper Saturation","Color detectors",255,255,setValues)
cv2.createTrackbar("Upper Value","Color detectors",255,255,setValues)
cv2.createTrackbar("Lower Hue","Color detectors",64,180,setValues)
cv2.createTrackbar("Lower Saturation","Color detectors",72,255,setValues)
cv2.createTrackbar("Lower Value","Color detectors",49,255,setValues)


bpoints=[deque(maxlen=1024)]
gpoints=[deque(maxlen=1024)]
rpoints=[deque(maxlen=1024)]
ypoints=[deque(maxlen=1024)]

blue_index=0
green_index=0
red_index=0
yellow_index=0

kernel=np.ones((5,5),np.uint8)

color=[[255,0,0],[0,255,0],[0,0,255],[0,255,255]]
color_index=0

paintwindow=np.zeros((471,636,3))+255
paintwindow=cv2.rectangle(paintwindow,(40,1),(140,65),(0,0,0),2)#It seems like you're using OpenCV (cv2) to draw a rectangle on an image. This line of code draws a rectangle on the image paintwindow with the specified parameters:

# (40, 1) is the coordinate of the top-left corner of the rectangle.
# (140, 65) is the coordinate of the bottom-right corner of the rectangle.
# (0, 0, 0) represents the color of the rectangle in BGR format (black in this case).
# 2 is the thickness of the rectangle border.

paintwindow=cv2.rectangle(paintwindow,(160,1),(255,65),color[0],1)
paintwindow=cv2.rectangle(paintwindow,(275,1),(370,65),color[1],1)
paintwindow=cv2.rectangle(paintwindow,(390,1),(485,65),color[2],1)
paintwindow=cv2.rectangle(paintwindow,(505,1),(600,65),color[3],1)

cv2.putText(paintwindow,"CLEAR",(49,33),cv2.FONT_HERSHEY_SIMPLEX,0.5,(0,0,0),2,cv2.LINE_AA)
# "CLEAR" is the text to be displayed.
# (49, 33) specifies the coordinates of the bottom-left corner of the text.
# cv2.FONT_HERSHEY_SIMPLEX is the font type.
# 0.5 is the font scale factor.
# (0, 0, 0) is the color of the text in BGR format (black in this case).
# 2 is the thickness of the text stroke.
# cv2.LINE_AA is the line type.
# This code will draw the text "CLEAR" on paintwindow with the specified parameters. 
cv2.putText(paintwindow,"BLUE",(185,33),cv2.FONT_HERSHEY_SIMPLEX,0.5,(255,255,255),2,cv2.LINE_AA)
cv2.putText(paintwindow,"GREEN",(298,33),cv2.FONT_HERSHEY_SIMPLEX,0.5,(255,255,255),2,cv2.LINE_AA)
cv2.putText(paintwindow,"RED",(420,33),cv2.FONT_HERSHEY_SIMPLEX,0.5,(255,255,255),2,cv2.LINE_AA)
cv2.putText(paintwindow,"YELLOW",(520,33),cv2.FONT_HERSHEY_SIMPLEX,0.5,(150,150,150),2,cv2.LINE_AA)

cv2.namedWindow('Paint',cv2.WINDOW_AUTOSIZE)


cap=cv2.VideoCapture(0)

while True:
    ret,frame=cap.read()
    frame=cv2.flip(frame,1)

    hsv=cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
    u_hue=cv2.getTrackbarPos("Upper Hue","Color detectors")
    u_saturation=cv2.getTrackbarPos("Upper Saturation","Color detectors")
    u_value=cv2.getTrackbarPos("Upper Value","Color detectors")
    l_hue=cv2.getTrackbarPos("Lower Hue","Color detectors")
    l_saturation=cv2.getTrackbarPos("Lower Saturation","Color detectors")
    l_value=cv2.getTrackbarPos("Lower Value","Color detectors")

    upper_hsv=np.array([u_hue,u_saturation,u_value])
    lower_hsv=np.array([l_hue,l_saturation,l_value])

#ye live frmae ke rectangle ke liye hai
    frame=cv2.rectangle(frame,(40,1),(140,65),(122,122,122),-1)
    frame=cv2.rectangle(frame,(160,1),(255,65),color[0],-1)
    frame=cv2.rectangle(frame,(275,1),(370,65),color[1],-1)
    frame=cv2.rectangle(frame,(390,1),(485,65),color[2],-1)
    frame=cv2.rectangle(frame,(505,1),(600,65),color[3],-1)
    cv2.putText(frame,"CLEAR",(49,33),cv2.FONT_HERSHEY_SIMPLEX,0.5,(255,255,255),2,cv2.LINE_AA)
    cv2.putText(frame,"BLUE",(185,33),cv2.FONT_HERSHEY_SIMPLEX,0.5,(255,255,255),2,cv2.LINE_AA)
    cv2.putText(frame,"GREEN",(298,33),cv2.FONT_HERSHEY_SIMPLEX,0.5,(255,255,255),2,cv2.LINE_AA)
    cv2.putText(frame,"RED",(420,33),cv2.FONT_HERSHEY_SIMPLEX,0.5,(255,255,255),2,cv2.LINE_AA)
    cv2.putText(frame,"YELLOW",(520,33),cv2.FONT_HERSHEY_SIMPLEX,0.5,(150,150,150),2,cv2.LINE_AA)

    #for creating mask and bid

    mask=cv2.inRange(hsv,lower_hsv,upper_hsv)
    mask=cv2.erode(mask,kernel,iterations=1)
    mask=cv2.morphologyEx(mask,cv2.MORPH_OPEN,kernel)
    mask=cv2.dilate(mask,kernel,iterations=1)

    #find countour of all pointer after identifing it

    cnts,_=cv2.findContours(mask.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    center=None

    if len(cnts)>0:
        #sort the contours
        cnt=sorted(cnts,key=cv2.contourArea,reverse=True)[0]
        ((x,y),radious)=cv2.minEnclosingCircle(cnt)
        #draw the circle
        cv2.circle(frame,(int(x),int(y)),int(radious),(0,255,255),2)
        #calculate the center of detected countour
        M=cv2.moments(cnt)
        center=(int(M['m10'] / M['m00']),int(M['m01']/M['m00']))

        if center[1]<=65:
            if 40<=center[0]<=140:#clear button
                bpoints=[deque(maxlen=512)]
                gpoints=[deque(maxlen=512)]
                rpoints=[deque(maxlen=512)]
                ypoints=[deque(maxlen=512)]

                blue_index=0
                green_index=0
                red_index=0
                yellow_index=0

                paintwindow[67:,:,:]=255
            elif 160<=center[0]<=255:
                color_index=0 #blue
            elif 275 <=center[0]<=370:
                color_index=1
            elif 390<=center[0]<=485:
                color_index=2
            elif 505 <=center[0]<=600:
                color_index=3


        else:
            if color_index==0:
                bpoints[blue_index].appendleft(center)
            elif color_index==1:
                gpoints[green_index].appendleft(center)
            elif color_index==2:
                rpoints[red_index].appendleft(center)
            elif color_index==3:
                ypoints[yellow_index].appendleft(center)
    
    else:
        bpoints.append(deque(maxlen=512))
        blue_index+=1
        gpoints.append(deque(maxlen=512))
        green_index+=1
        rpoints.append(deque(maxlen=512))
        red_index+=1
        ypoints.append(deque(maxlen=512))
        yellow_index+=1

    #draw lines of all colours
    points = [bpoints, gpoints, rpoints, ypoints]
    for i in range(len(points)):
        for j in range(len(points[i])):
            for k in range(1, len(points[i][j])):
                if points[i][j][k - 1] is None or points[i][j][k] is None:
                    continue
                # print("Point 1:", points[i][j][k - 1])
                # print("Point 2:", points[i][j][k])
                cv2.line(frame, points[i][j][k - 1], points[i][j][k], color[i], 2)
                cv2.line(paintwindow, points[i][j][k - 1], points[i][j][k], color[i], 2)
            
    
    cv2.imshow("Tracking",frame)
    cv2.imshow("paint",paintwindow)
    cv2.imshow("mask",mask)

    if(cv2.waitKey(1)& 0xFF==ord("q")):
        break

cap.release()
cv2.destroyAllWindows()




        


   

