# -*- coding: utf-8 -*-
#Bibliotecas y funciones ocupadas
import numpy as np
import cv2
from circulo_mano import circulo_mano
from cambio_tam import cambio_tam
from mascara_circular import mascara_circular

def cuadrado_mano_centrado(imagen_original):
    """Función que regresa la mano en tamaño de 256x256 en su respectivo circulo contenido.
    
    Se ingresa la imagen radiográfica con sus dimensiones originales, no importa cuales sean.
    Después se calcula el centroide y se obtiene una circunferencia donde se encuentra la mano,
    a partir de esta circunferencia se corta solamente dicha zona.
    Finalmente se regresa la mano con su circunferencia, en las dimensiones 256x256.
    
    Entradas:
        imagen_original-->Imagen a evaluar
    Salidas:
        imagen_final-->Imagen de la mano con dimensiones de 256x256
        cxc-->Valor del centroide en el eje x
        cyc-->Valor del centroide en el eje y
    """

    filas_o,columnas_o=imagen_original.shape#Se toman las dimensiones de la imagen original
    imagen = cambio_tam(imagen_original)#Toma el valor menor de las dimensiones y lo pasa a 256 y su lado mayor a un calor proporcional
    filas,columnas=imagen.shape#Obtiene las dimensiones de la imagen reducida
    cir_mano, radio_mano,cx,cy=circulo_mano(imagen)#Obtiene la mano en conjunto con su circulo contenida, el baricentro y el radio del círculo
    proporcion=round((columnas_o/columnas),1)#A partir de las filas y columnas de la imagen reducida, se obtiene un valor de proporción
    cx_p=cx*proporcion#Se obtiene el valor en x del centroide en la imagen original
    cy_p=cy*proporcion#Se obtiene el valor en y del centroide en la imagen original
    radio_p=round(radio_mano*proporcion)#Se obtiene el radio en la imagen original
    mascara=mascara_circular(filas_o,columnas_o,centro=[cx_p,cy_p],radio=radio_p)#Se obtiene la máscara circular en la imagen original
    zona=mascara*imagen_original#Se aplica la máscara circular en la imagen original
    cx_p=int(round(cx_p))#Se redondea el valor del centroide en el punto x
    cy_p=int(round(cy_p))#Se redondea el valor del centroide en el punto y
    radio_p=int(radio_p)#Se redondea el valor del radio
    dimy1=cy_p-radio_p#Valor mínimo en el eje y para realizar el recorte del circulo
    dimy2=cy_p+radio_p#Valor máximo en el eje y para realizar el recorte del circulo
    dimx1=cx_p-radio_p#Valor mínimo en el eje x para realizar el recorte del circulo
    dimx2=cx_p+radio_p#Valor máximo en el eje x para realizar el recorte del circulo
    if dimx1 <0:#En caso de que el valor sea un valor negativo en el eje x
       dimx1=0#Se obtiene el valor inicial de la imagen
    if dimy1<0:#En caso de que el valor sea un valor negativo en el eje y
       dimy1=0#Se obtiene el valor inicial de la imagen
    if dimx2 > columnas_o:#Si el valor es mayor al de las columnas
       dimx2=columnas_o#Se deja el valor de las columnas
    if dimy2 > filas_o:#Si el valor es mayor al de las filas
       dimy2=filas_o#Se deja el valor de las filas
    recorte=zona[dimy1:dimy2,dimx1:dimx2]#Recorte de la mano en conjunto con el circulo
    if recorte.shape[0]==recorte.shape[1]:#Si los recortes son cuadrados
       imagen_final=cv2.resize(recorte,dsize=(256, 256))#Se cambian las dimensiones del recorte a 256x256
       cxc=imagen_final.shape[0]//2#Se calcula el centroide del recorte en el eje x
       cyc=imagen_final.shape[0]//2#Se calcula el centroide del recorte en el eje y
    else:#En caso de que los recortes sean rectangulares
       if (cx_p-radio_p>0):#Si la resta entre el radio y el valor en x del centroide es mayor que 0
          diferencia1=cx_p-radio_p#Se guarda el valor de la resta en la variable diferencia1
       else:
          diferencia1=0#De otra manero se asigna a la variable el valor de 0
       cx_nuevo = cx_p-diferencia1#Nuevo valor para el valor del centroide en el eje x
       cy_nuevo=cy_p-dimy1#Nuevo valor para el centroide en el eje y
       final=np.zeros((radio_p*2,radio_p*2))#Se realiza una matriz del tamaño del radio
       aux1=radio_p-cx_nuevo#Variable en el eje x para recortar el rectangulo
       aux2=radio_p-cy_nuevo#Variable en el eje y para recortar el rectangulo
       final[aux2:aux2+recorte.shape[0] , aux1:aux1+recorte.shape[1]]=recorte#Se toma de la matriz final, una matriz del tamaño de recorte
       imagen_final=cv2.resize(final,dsize=(256, 256))#Se cambian las dimensiones de la matriz a 256x256
       cxc=imagen_final.shape[0]//2#Se calcula el centroide del recorte en el eje x
       cyc=imagen_final.shape[0]//2#Se calcula el centroide del recorte en el eje y
       
    return imagen_final,cxc,cyc#Se regresa la imagen de la mano de tamaño de 256x256 y su respectivo centroide