# -*- coding: utf-8 -*-

import cv2
import matplotlib.pyplot as plt

def centroide(imagen,grafica):
      """Localiza el centroide de una imagen y devuelve las coordenadas.
      Entradas:
      imagen --> Imagen a evaluar
      grafica --> si se elige grafica=1, se grafica el centroide con los bordes de canny
                  si grafica=2 se grafica el centroide con la imagen de entrada
      Salidas:
      cx --> coordenada x del baricentro
      cy --> coordenada y del baricentro
      """
      M2 = cv2.moments(imagen) #Función de opencv para obtener propiedas de la imagen
      if M2["m00"] != 0: #Condición para obtener el baricentro si es diferente de 0
           cx = int(M2['m10']/M2['m00']) #Fórmula para obtner la coordenada x
           cy = int(M2['m01']/M2['m00']) #Fórmula para obtner la coordenada y
      else: #Si m00 == 0 las dos coordenadas son 0
           cx, cy = 0, 0
      if grafica == 1: #Condición para graficar el centroide con bordes
         plt.plot(cx,cy,'ro')
         plt.imshow(imagen,cmap="gray")
         plt.show()
      elif grafica == 2: #Condición para graficar el centroide con la imagen de entrada
         plt.plot(cx,cy,'ro')
         plt.imshow(imagen,cmap="gray")
         plt.show()
      return cx,cy#Se regresa el baricentro
   
