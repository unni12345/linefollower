import cv2
import numpy as np
import time
import matplotlib.pyplot as plt
import serial as ser
import math
t=0

x=[]
y=[]
cap = cv2.VideoCapture(0)
lx2 =0
ly2=0
t2=0
t2=0


while(1):
   t1=time.time()
   
# Take each frame
  
   _, frame = cap.read()
   
   
# Convert BGR to HSV
   hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
   lg = np.array([58,50,50])
   ug= np.array([78,255,255])
# Threshold the HSV image to get only blue colors
   blur = cv2.GaussianBlur(hsv,(5,5),0)
   
   mask = cv2.inRange(blur, lg, ug)
   ret3,mask = cv2.threshold(mask,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
   kernel = np.ones((3,3),np.uint8)
   erosion = cv2.erode(mask,kernel,iterations = 1)
   dilation = cv2.dilate(erosion,kernel,iterations = 1)
   dilation[1,1]=1
   image, contours, hierarchy = cv2.findContours(dilation,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
# Bitwise-AND mask and original image
   res = cv2.bitwise_and(frame,frame, mask= mask)
   cnt=contours[0]
   
   l1,l2 = tuple(cnt[cnt[:,:,0].argmin()][0])
   r1,r2 = tuple(cnt[cnt[:,:,0].argmax()][0])
   t1,t2 = tuple(cnt[cnt[:,:,1].argmin()][0])
   b1,b2 = tuple(cnt[cnt[:,:,1].argmax()][0])
   cv2.imshow('frame',frame)
   cv2.imshow('mask',mask)
   cv2.imshow('res',res)
   cv2.imshow("dilation",dilation)
   lx=(l1+r1+t1+b1)/4
   ly=(l2+r2+t2+b2)/4
   print lx,ly
   x.append(lx)
   y.append(ly)
  
   
   print "present time", t1
   vel=math.sqrt((lx2-lx)*(lx2-lx)+(ly2-ly)*(ly2-ly))
   #find velocity
   print "velocity",vel
   lx2=lx
   ly2=ly
   t2=t1
   k = cv2.waitKey(5) & 0xFF
   if k == 27:
      break
 
for i in x:
    t=t+1
p=0
print "t", t    
for i in range (t):
    if x[i] != 1:
        if x[i+1]==1:
            x[i]=1
            y[i]=1
        elif x[i+2]==1:
            x[i]=1
            y[i]=1
        elif x[i+3]==1:
            x[i]=1
            y[i]=1
        elif x[i+4]==1:
            x[i]=1
            y[i]=1  
plt.plot( x, y)
plt.xlabel('x coordinate')
plt.ylabel('y coordinate')
plt.title('trajectory')
plt.show () 

cv2.destroyAllWindows()
