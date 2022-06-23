#import opencv and numpy
import cv2  
import numpy as np

#trackbar callback fucntion to update HSV value
def callback(x):
    global H_low,H_high,S_low,S_high,V_low,V_high

    H_low = cv2.getTrackbarPos('L-H','controls')
    H_high = cv2.getTrackbarPos('H-H','controls')
    S_low = cv2.getTrackbarPos('L-S','controls')
    S_high = cv2.getTrackbarPos('H-S','controls')
    V_low = cv2.getTrackbarPos('L-V','controls')
    V_high = cv2.getTrackbarPos('H-V','controls')


#create a seperate window named 'controls' for trackbar
cv2.namedWindow('controls',2)
cv2.resizeWindow("controls", 300,5);


#global variable
H_low = 0
H_high = 179
S_low= 0
S_high = 255
V_low= 0
V_high = 255

#create trackbars for high,L-H,S,V 
cv2.createTrackbar('L-H','controls',0,179,callback)
cv2.createTrackbar('L-S','controls',0,255,callback)
cv2.createTrackbar('L-V','controls',0,255,callback)

cv2.createTrackbar('H-H','controls',179,179,callback)
cv2.createTrackbar('H-S','controls',255,255,callback)
cv2.createTrackbar('H-V','controls',255,255,callback)


while(1):
    #read source image
    img=cv2.imread("Pictures/cristal.png")
    #convert sourece image to HSC color mode
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)  
    #
    hsv_low = np.array([H_low, S_low, V_low], np.uint8)
    hsv_high = np.array([H_high, S_high, V_high], np.uint8)


    mask = cv2.inRange(hsv, hsv_low, hsv_high)
    print (hsv_low)
    #masking HSV value selected color becomes black
    res = cv2.bitwise_and(img, img, mask=mask)

    #show image
    cv2.imshow('mask',mask)
    cv2.imshow('res',res)

    #waitfor the user to press escape and break the while loop 
    k = cv2.waitKey(1) & 0xFF
    if k == 27:
        break

cv2.destroyAllWindows()