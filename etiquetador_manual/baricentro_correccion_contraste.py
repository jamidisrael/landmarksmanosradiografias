# -*- coding: utf-8 -*-
import cv2
from mascara_circular import mascara_circular
from centroide import centroide
from parche import parche
import numpy as np
from scipy.spatial import distance
from correccion_contraste_pormuestra import correccion_contraste_pormuestra

def baricentro_correccion_contraste(imagen):
   """Función para obtener el baricentro dentro de la mano.
   Entradas:
   imagen --> Imagen a evaluar
   Salidas:
   cx --> coordenada x de la imagen
   cy --> coordenada y de la imagen
   edges --> bordes de la imagen de la mano
   """
   radio_inicial =100 #Se inicia el radio con 100 pixeles
   filas,columnas=imagen.shape #Obtiene el valor de las dimensiones de la imagen
   edges = cv2.Canny(imagen,5,20) #Primera obtención de los bordes con valores umbrales mínimo de 5 y máximo de 20 
   cx,cy = centroide(edges,0)#Se localiza por primera vez el centroide
   parche_=parche(imagen,cx,cy,60)#Se toma una ventana de tamaño 60x60 pixeles a partir del baricentro
   correcion_cont = correccion_contraste_pormuestra(imagen,parche_,1.5,0)#Corrección de contraste con 1.5sigma
   edges = cv2.Canny(correcion_cont,70,100) #Segunda obtención de los bordes con valores umbrales mínimo de 70 y máximo de 100 
   cx,cy = centroide(edges,0) #Segunda localización del centroide
   centroide_anterior = np.array([cx,cy])#Variable para ir guardando el centroide previo
   condicion=True#Condición 
   cond2 = True #Condición
   
   #Inicio ciclo while
   while condicion == True or cond2 == True:#Se tienen dos condiocnes para el ciclo while
      mascara = mascara_circular(filas,columnas,centro=[cx,cy],radio=radio_inicial) #Se aplica la función de mascara_circular
      zona = (mascara*edges) #multiplica la mascara y la imagen para obtener la zona de interes
      cx,cy = centroide(zona,0) #Obtención del centroide
      centroide_actual=np.array([cx,cy])#Se guarda el centroide calculado
      distancia =  distance.euclidean(centroide_anterior, centroide_actual)#Calculo de la distancia euclideana del centroide anterior con el actual
      centroide_anterior = centroide_actual#Se asigna el centroide actual como anterior para continuar la búsqueda
      radio_inicial = radio_inicial - 10 #Va disminuyendo de 10 en 10 el radio
      #Condiciones para continuar o salir del bucle
      if distancia > 1:#Si la distancia del centroide aanterior y actual es mayor que 1
         cond2=False #cond2 es falso
      if distancia <= 1:#Si la distancia es menor o igual que 1
         condicion=False#condicion es falso
      else:#De otro modo
         condicion = True#Se continua en el bucle
      if radio_inicial<=30:#Si el radio inicial es menor o igual a 30
         condicion=False#condicion es falso
         cond2=False#cond2 es falso y se sale del bucle
   return cx,cy,edges#la función regresa las coordenadas del baricentro y los bordes de la imagen