# -*- coding: utf-8 -*-
import imutils

def cambio_tam(imagen):
   """Toma la imagen y pasa su lado menor a 256 y el otro a un valor proporcional
   Entradas:
       imagen --> imagen a evaluar
   Salidas:
       m --> Imagen ya con el valor de 256 y valor proporcional
   """
   filas,columnas=imagen.shape#Se opbtienen las dimensiones de la imagen
   if filas<columnas:#Si las columnas son mayores que las filas
      m=imutils.resize(imagen, height=256)#filas son 256 y las columnas a un valor proporcional
   elif columnas==filas:#Caso especial donde la imagen es cuadrada
         m=imutils.resize(imagen, width=256,height=256)#Las dimensiones se pasan a 256x256
   else: #Si las filas son mayores que las columnas
      m=imutils.resize(imagen, width=256)#columna son 256 y filas a un valor proporcional
   return m#Se regresa la imagen con las dimensiones mencionadas