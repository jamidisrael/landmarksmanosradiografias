# -*- coding: utf-8 -*-

#Bibliotecas y funciones utilizadas
import numpy as np

def mascara_circular(filas, columnas, centro=None, radio=None):
    """Función para aplicar una máscara circular sobre una imagen.
    
    Ésta función aplica una máscara circular sobre una imagen, donde lo que esta dentro del círculo
    es de valor 1 y lo demás es de valor 0. Para esto se deben ingresar las filas, columnas de la imagen,
    el centro del circulo y el radio al que se quiere.
    
    Entradas:
        filas --> Valor de las filas de la imagen
        columnas --> Valor de las columnas de la imagen
        centro --> Centro del círculo (Si no se escribe el centro, se toma el centro de la imagen)
        radio --> Radio del circulo (Si no se especifica el radio se toma el tamaño de la imagen)
    Salidas:
        mascara --> Máscara sobre la imagen
    """
    
    if centro is None:#Se toma la mitad de la imagen
        centro = [int(columnas/2), int(filas/2)]#El centro se toma de acuerdo a los valores dados
    if radio is None: #Se usa la distancia a las filas y columnas para el radio, si no se especifica
        radio = min(centro[0], centro[1], columnas-centro[0], filas-centro[1])#Se toma el radio que se especifica
    Y, X = np.ogrid[:filas, :columnas] #Crea una matriz del tamaño especificado
    dist_from_center = np.sqrt((X - centro[0])**2 + (Y-centro[1])**2)#Se calcula la distancia al centro
    #Se convierte a binaria la imagen
    mask = dist_from_center <= radio#Toma los valores que estan dentro del radio
    mascara = np.zeros((filas,columnas))#Crea una matriz del tamaño de las filas y columnas
    mascara[mask==False] = 0#Si los valores en la variable mask son False, se asigna a todos ellos el valor de 0
    mascara[mask==True] = 1#Si los valores en la variable mask son True, se asigna a todos ellos el valor de 1
    return mascara.astype('uint8')#Se regresa la variable mascara con valores uin8