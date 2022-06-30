import numpy as np
import imutils
import cv2
import json

#trackbar callback fucntion to update HSV value
# optional argument for trackbars
def nothing(x):
    pass

barsWindow = 'Bars'
hl = 'H Low'
hh = 'H High'
sl = 'S Low'
sh = 'S High'
vl = 'V Low'
vh = 'V High'

try:
    arquivo = open('SaveHSV.json', 'r+')
except FileNotFoundError:
    arquivo = open('SaveHSV.json', 'w+')
    arquivo.writelines("{HSVLOWER:[0,0,0],HSVHIGH:[255,255,255]}")
    arquivo.close()

with open("SaveHSV.json", encoding='utf-8') as meu_json:
    dados = json.load(meu_json)

cap = cv2.VideoCapture(0)

cv2.namedWindow(barsWindow, flags = cv2.WINDOW_AUTOSIZE)

cv2.createTrackbar(hl, barsWindow, 0, 179, nothing)
cv2.createTrackbar(hh, barsWindow, 0, 179, nothing)
cv2.createTrackbar(sl, barsWindow, 0, 255, nothing)
cv2.createTrackbar(sh, barsWindow, 0, 255, nothing)
cv2.createTrackbar(vl, barsWindow, 0, 255, nothing)
cv2.createTrackbar(vh, barsWindow, 0, 255, nothing)

cv2.setTrackbarPos(hl, barsWindow, dados['HSVLOWER'][0])
cv2.setTrackbarPos(hh, barsWindow, dados['HSVHIGH'][0])
cv2.setTrackbarPos(sl, barsWindow, dados['HSVLOWER'][1])
cv2.setTrackbarPos(sh, barsWindow, dados['HSVHIGH'][1])
cv2.setTrackbarPos(vl, barsWindow, dados['HSVLOWER'][2])
cv2.setTrackbarPos(vh, barsWindow, dados['HSVHIGH'][2])



while True:
    ret, frame = cap.read()
    frame = imutils.resize(frame, width=600)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    hul = cv2.getTrackbarPos(hl, barsWindow)
    huh = cv2.getTrackbarPos(hh, barsWindow)
    sal = cv2.getTrackbarPos(sl, barsWindow)
    sah = cv2.getTrackbarPos(sh, barsWindow)
    val = cv2.getTrackbarPos(vl, barsWindow)
    vah = cv2.getTrackbarPos(vh, barsWindow)

    HSVLOW = np.array([hul, sal, val])
    HSVHIGH = np.array([huh, sah, vah])

    kernel = np.ones((9, 9), np.uint8)

    mask = cv2.inRange(hsv, HSVLOW, HSVHIGH)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
                                cv2.CHAIN_APPROX_SIMPLE)[-2]
    center = None

    if len(cnts) > 0:
        c = max(cnts, key=cv2.contourArea)
        ((x, y), radius) = cv2.minEnclosingCircle(c)
        M = cv2.moments(c)
        center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

        if radius > 10:
            cv2.circle(frame, (int(x), int(y)), int(radius),
                       (0, 255, 255), 2)
            cv2.circle(frame, center, 5, (0, 0, 255), -1)

            cv2.putText(frame, "Contagem: {}".format(str(len(cnts))), (5, 50),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (250, 0, 1), 2)
    
    cv2.imshow("Frame", frame)
    cv2.imshow("Mask", mask)

    if cv2.waitKey(1) & 0XFF == ord('s'):

        arquivo = open('SaveHSV.json', 'w+')
        arquivo.writelines('{\"HSVLOWER\":[' + str(HSVLOW[0]) + ',' + str(HSVLOW[1]) + ',' +
        str(HSVLOW[2]) + '],\"HSVHIGH\":[' + str(HSVHIGH[0]) + ',' + str(HSVHIGH[1]) + ',' + 
        str(HSVHIGH[2]) + ']}')
        arquivo.close()

        break

    if cv2.waitKey(1) & 0XFF == 27:
        break


cap.release()
cv2.destroyAllWindows()