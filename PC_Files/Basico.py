import cv2
import numpy as np

cap = cv2.VideoCapture(0)


print "Resolucao padrao: ( " + str(cap.get(3)) + " x " + str(cap.get(4)) + " )"

cap.set(3, 320)
cap.set(4, 240)

print "Resolucao ajustada para: ( " + str(cap.get(3)) + " x " + str(cap.get(4)) + " )"
print "\nAperte 'Esc' para encerrar o programa."



while(1):
    _,frame = cap.read()

    #Escrever um texto em uma imagem na coordenada (xy)
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(frame, 'OpenCV',(80,220),font,0.5,(255,255,255),1,cv2.LINE_AA)

    # converter o frame para o padrao de cores HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Conjunto de cores basicas
    lower_blue = np.array([110,100,100])
    upper_blue = np.array([130,255,255])

    lower_red = np.array([0,50,50])
    upper_red = np.array([10,255,255])

    lower_yellow = np.array([20,20,20])
    upper_yellow = np.array([35,255,255])

    lower_green = np.array([24,40,40])
    upper_green = np.array([60,255,255])
    ###

    ##brincadeira
    #Criar um Circulo no centro da tela
    scr_x = int(cap.get(3))/2 # meio da tela do Eixo X
    scr_y = int(cap.get(4))/2 # meio da tela do Eixo Y
                
    cv2.circle(frame,(scr_x,scr_y),5,(0,255,0),-1)
    ##

    # marcar e/ou apenas a imagem do intervalo de cor selecionado
    mask = cv2.inRange(hsv, lower_blue, upper_blue)

    # buscar estruturas na imagem
    element = cv2.getStructuringElement(cv2.MORPH_RECT,(3,3))
    mask = cv2.erode(mask,element, iterations=2)
    mask = cv2.dilate(mask,element, iterations=2)
    mask = cv2.erode(mask,element)

    #buscar melhor objeto para encontrar contornos
    frame2,contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)


    maximumArea = 0
    bestContour = None
    for contour in contours:
        currentArea = cv2.contourArea(contour)
        if currentArea > maximumArea:
            bestContour = contour
            maximumArea = currentArea

    if bestContour is not None:
        # desenhar retangulo em volta do objeto (nesse caso, azul)
        x,y,w,h = cv2.boundingRect(bestContour)
        cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0), 3)

        ##Brincadeira
        # escrever na tela as coordenadas das bordas X e Y do retangulo
        # texto fica flutuando ao lado do retangulo
        msg = 'X: ' +str(x) + ' Y: ' +str(y) 
        cv2.putText(frame, msg,(x,y+(-10)),font,0.3,(255,0,0),1,cv2.LINE_AA)
        ##


        ##Brincadeira
        # criar um ponto central no moment contornado (neste caso azul (centroid))
        M = cv2.moments(bestContour)
        cx,cy = int(M['m10']/M['m00']), int(M['m01']/M['m00'])
        cv2.circle(frame,(cx,cy),10,(0,0,255),-1)
        ##

        ##Brincadeira
        # escrever na tela as coordenadas CX e CY do centro do moment 
        # coordenadas do centroid
        msg2 = 'CX: ' + str(cx) + ' CY: ' + str(cy)
        cv2.putText(frame, msg2,(cx +10,cy),font,0.5,(0,0,255),1,cv2.LINE_AA)
        ##


        ## brincadeira
        # criar uma linha do cento da tela ate o centro do moment
        cv2.line(frame, (160,120), (cx,cy),(255,255,255),5)
        ##

        ## brincadeira
        #desenhar contorno no moment (neste caso, objeto azul)
        cv2.drawContours(frame,[bestContour],-1,(255,0,0),2)
        ##

        ##Brincadeira
        # escrever no console se o objeto detectado esta em
        # Superior Direito/Esquerdo, Inferior Direito/Esquerdo, Superior, inferior ou centro da tela
        # Tome nota, a imagem eh invertida
        if cx > scr_x:
            if cy < scr_y:
                print ' Superior Esquerdo '

            elif cy > scr_y:
                print ' Inferior Esquerdo '

            else:
                print ' Lado Esquerdo '

        elif cx < scr_x:
            if cy < scr_y:
                print ' Superior Direito '

            elif cy > scr_y:
                print ' Inferior Direito '

            else:
                print ' Lado Direito '

        elif cx == scr_x:
            if cy < scr_y:
                print' cima '

            else:
                print ' baixo '


        else:
            print ' meio '
        ##

    # exibir a imagem
    cv2.imshow('frame', frame)
    #cv2.imshow('mask', mask)
    #cv2.imshow('hsv', hsv)

    # caso a tecla 'Esc' for pressionada, sair do loop
    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break

#fechar todas as janelas e encerrar a camera.
print "\nEncerrando programa..."
cv2.destroyAllWindows()
cap.release()

