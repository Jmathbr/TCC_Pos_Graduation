import math
import cv2
import numpy as np
from sqlalchemy import true


vd = cv2.VideoCapture('Pictures/gl.mp4')
ok, frame = vd.read()

BlueLower = (80, 60, 40)
BlueUpper = (130, 255, 255)

while True:
    ok, frame = vd.read()
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    if not ok:
        break

    maskGreen = cv2.inRange(hsv, BlueLower, BlueUpper)
    maskGreen = cv2.erode(maskGreen, None, iterations=2)
    maskGreen = cv2.dilate(maskGreen, None, iterations=2)

    cv2.imshow("1",frame);
    cv2.imshow("2",hsv);
    cv2.imshow("3",maskGreen);

    if cv2.waitKey(1) & 0XFF == 27: # ESC
        break
