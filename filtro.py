import math
import cv2
import numpy as np
from sqlalchemy import true

#frame = cv2.VideoCapture("C:/Users/joaom/Documents/Cristalina/ReconBottle/Pictures/gl.mp4")
frame = cv2.imread("Pictures/cristal.png")

BlueLower = (97, 100, 117)
BlueUpper = (110, 255, 255)

hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
maskGreen = cv2.inRange(hsv, BlueLower, BlueUpper)
maskGreen = cv2.erode(maskGreen, None, iterations=2)
maskGreen = cv2.dilate(maskGreen, None, iterations=2)

cv2.imshow("1",frame);
cv2.imshow("2",hsv);
cv2.imshow("3",maskGreen);
cv2.waitKey(0)
cv2.destroyAllWindows();