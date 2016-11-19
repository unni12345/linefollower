
import cv2
import serial
import time

cap=cv2.VideoCapture(1)
if not(cap.isOpened()):
    cap.open()
ser=serial.Serial("COM9")
p='f'
lx=0
ly=0
rx=0
ry=0
bx=0
by=0
tx=0
ty=0
lx2=0
ly2=0
rx2=0
ry2=0
tx2=0
ty2=0
bx2=0
by2=0
cx=1
cy=1
p="s"
k=1

while(cap.isOpened()):
    ret, frame = cap.read()
    cv2.imshow("Webcam", frame)
    bkg=frame.copy()
    fundo = cv2.GaussianBlur(bkg,(3,3),0)
    
    bl,gl,rl=fundo[1,1]
    
    bc,gc,rc=fundo[220,240]
    kc= 0.299*rc+0.587*gc+0.114*bc
    kl=0.299*rl+0.587*gl+0.114*bl
    print "kc,kl",kc,kl
    
    
    
    if cv2.waitKey(1) == 27:
        cv2.destroyWindow("Webcam")
        break
while (cap.isOpened()):
    t=time.time()
    print t
    ret,img=cap.read()
    gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    if kc>kl:
        print " binary threshold"   
        ret,thresh1 = cv2.threshold(gray,kc-20,255,0)
    else :
        print " inverse binary threshold"
        ret,thresh1 = cv2.threshold(gray,kc+20,255,1)
        
    rows,cols,channels = img.shape
    roi=thresh1[400:430,0:cols]
    roit= thresh1[100:130,0:cols]
    roi[1,1]=1
    roit[1,1]=1
    
    
    cv2.imshow("roi",roi)
    
    image, contours, hierarchy = cv2.findContours(roi,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    cnt=contours[0]
    
    lx,ly = tuple(cnt[cnt[:,:,0].argmin()][0])
    rx,ry = tuple(cnt[cnt[:,:,0].argmax()][0])
    tx,ty = tuple(cnt[cnt[:,:,1].argmin()][0])
    bx,by = tuple(cnt[cnt[:,:,1].argmax()][0])
    print "lm",lx,ly
    print "rm",rx,ry
    print "tm",tx,ty
    print "bm",bx,by
    print "rx-lx",rx-lx
    print "by-ty",by-ty
    
    if rx>340 and lx >300:
        print "right"
        ser.write("t")
        p="t"
    elif  rx <300 and lx<340 :
        print "left"
        ser.write("e")
        p="e"
    
    elif tx==1 or  lx==1 :
        print "extreme left"
        ser.write("w")
        p="w"
    elif tx==638 or rx ==638:
        print "extrme right"
        ser.write("y")
        p="y"
    else:
        print "forward"
        ser.write("f")
        p='f'

    print "x-coordinate",(lx+bx+rx+tx)/4
    print "y-coordinate",(ly+by+ry+ty)/4
    cx=(lx+bx+rx+tx)/4
    cy=(ly+by+ry+ty)/4
    if cx==1 and cy==1:
        print "previous"
        ser.write(p)
        
        
    
    
        
   
    cv2.imshow("enthiru",thresh1)
    if cv2.waitKey(10) ==27:
       ser.write("s")
        
       cap.release()
       cv2.destroyAllWindows()
