import numpy as np
import imutils
import cv2
import json
from time import sleep


#Criar tratativa de erro para quando o centro do galao estiver em cima da linha
#Suguerir usar o tempo como parametro para o tempo de deteccao

largura_min = 80  # Largura minima do retangulo
altura_min = 80  # Altura minima do retangulo
offset = 6  # Erro permitido entre pixel
pos_linha = 400  # Posição da linha de contagem
delay = 60  # FPS do vídeo
detec = []
galoes = 0

def nothing(x):
    pass

def pega_centro(x, y, largura, altura):
    """
    :param x: x do objeto
    :param y: y do objeto
    :param largura: largura do objeto
    :param altura: altura do objeto
    :return: tupla que contém as coordenadas do centro de um objeto
    """
    x1 = largura // 2
    y1 = altura // 2
    cx = x + x1
    cy = y + y1
    return cx, cy

def set_info(detec):
    global galoes
    for (x, y) in detec:
        if (pos_linha + offset) > y > (pos_linha - offset):
            galoes += 1
            cv2.line(frame, (25, pos_linha), (575, pos_linha), (0, 127, 255), 3)
            detec.remove((x, y))
            print("Galoes detectados ate o momento: " + str(galoes))

def show_info(frame1, dilatada):
    text = f'Galoes: {galoes}'
    cv2.putText(frame1, text, (25, 70), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 5)
    cv2.imshow("Video Original", frame1)
    cv2.imshow("Detectar", dilatada)


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


subtracao = cv2.bgsegm.createBackgroundSubtractorMOG()

while True:
    ret, frame = cap.read()
    tempo = float(1 / delay)
    sleep(tempo)

    frame = imutils.resize(frame, width=600)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    blur = cv2.GaussianBlur(hsv, (3, 3), 5)
    img_sub = subtracao.apply(blur)
    dilat = cv2.dilate(img_sub, np.ones((5, 5)))

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

    contorno, img = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cv2.line(frame, (25, pos_linha), (575, pos_linha), (255, 127, 0), 3)
    for (i, c) in enumerate(contorno):
        (x, y, w, h) = cv2.boundingRect(c)
        validar_contorno = (w >= largura_min) and (h >= altura_min)
        if not validar_contorno:
            continue

        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        centro = pega_centro(x, y, w, h)
        detec.append(centro)
        cv2.circle(frame, centro, 4, (0, 0, 255), -1)

    set_info(detec)
    show_info(frame, mask)

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