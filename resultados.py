# -*- coding: utf-8 -*-
"""
Created on Mon Sep 28 21:20:55 2020

@author: israe
"""
#Bibliotecas y funciones utilizadas
from sklearn.metrics import mean_absolute_error
from sklearn.metrics import mean_squared_error
import csv
import logging
# from error_mae import error_mae
# from error_rmse import error_rmse
# from archivo_log import archivo_log

def error_mae(coordenadas_manuales, coordenadas_automaticas):
    """Función que calcula el error medio absoluto de landmarks.
    
    Realiza el cálculo del error mae de las landmarks en pixeles.Para esto se debe ingresar 
    los archivos .mat en conjunto con su ubicación.
    La función realiza el cálculo del error medio absoluto de acuerdo a la siguiente fórmula:

                                                N
                                               ___
                                    MAE = 1    \
                                          -    /   |Yi - Y*i|
                                          N    ___
                                               i=1
    
    Donde:
    N                       : El total de puntos marcados
    Yi                      : Los puntos marcados manualmente
    Y*i                     : Los puntos marcados automáticamente
    
    Parámetros de entrada de la función:
    
    coordenadas_manuales    : Es el archivo .mat con los puntos marcados manualmente.
                              Se debe especificar la ruta donde esta el archivo .mat.
                              Por ejemplo: ./ruta/archivo/mat_manual.mat
    coordenadas_automaticas : Es el archivo .mat con los puntos marcados automáticamente
                              Se debe especificar la ruta donde esta el archivo .mat.
                              Por ejemplo: ./ruta/archivo/mat_automatico.mat
                              
    Parámetros de salida de la función:
    
    error_final             : Es el error en pixeles de las landmarks
    """
    manual_sx = []#Lista vacia para guardar la landmark superior manual en el eje x
    automa_sx = []#Lista vacia para guardar la landmark superior automática en el eje x
    manual_ix = []#Lista vacia para guardar la landmark inferior manual en el eje x
    automa_ix = []#Lista vacia para guardar la landmark inferior automática en el eje x
    manual_sy = []#Lista vacia para guardar la landmark superior manual en el eje y
    automa_sy = []#Lista vacia para guardar la landmark superior automática en el eje y
    manual_iy = []#Lista vacia para guardar la landmark inferior manual en el eje y
    automa_iy = []#Lista vacia para guardar la landmark inferior automática en el eje y
    
    ###############################Lectura de los archivos csv################################
    # archivo_manual = 'Manual_landmarks.csv'#Se leé el csv con las landmarks manual
    with open(coordenadas_manuales) as f:#Se guarda en el objeto f
        reader=csv.reader(f)#Se pasa la información a la variable reader
        header_row=next(reader)#Se va leyendo las filas del archivo
        lista_manual=[]#Se crea una lista donde se irá guardando los datos leídos
        for row in reader:#Ciclo para guardar los datos
            lista_manual.append(row)#Se va agregando los datos a las listas
    
    # archivo_automa = 'E:/Maestria/una_imagen/ipilab/Alignded_Images/Landmarks.csv'#Se leé el csv con las landmarks automáticas
    with open(coordenadas_automaticas) as f2:#Se guarda en el objeto f
        reader2=csv.reader(f2)#Se pasa la información a la variable reader
        header_row2=next(reader2)#Se va leyendo las filas del archivo
        lista_automa=[]#Se crea una lista donde se irá guardando los datos leídos
        for row2 in reader2:#Ciclo para guardar los datos
            lista_automa.append(row2)#Se va agregando los datos a las listas
    #####################################################################################
    for i in range(0,len(lista_manual)):#Ciclo para crear las lsitas donde se obtendrá el error
        nombrem,xsm,ysm,xim,yim=lista_manual[i]#Lista con los datos manuales
        nombrea,xsa,ysa,xia,yia=lista_automa[i]#Lista con los datos automáticos
        if nombrem==nombrea:#Si los nombres de la imagen automática y manual coinciden
            manual_sx.append(float(xsm))#Se agrega la lista correspondiente
            automa_sx.append(float(xsa))#Se agrega la lista correspondiente
            manual_sy.append(float(ysm))#Se agrega la lista correspondiente
            automa_sy.append(float(ysa))#Se agrega la lista correspondiente
            manual_ix.append(float(xim))#Se agrega la lista correspondiente
            automa_ix.append(float(xia))#Se agrega la lista correspondiente
            manual_iy.append(float(yim))#Se agrega la lista correspondiente
            automa_iy.append(float(yia))#Se agrega la lista correspondiente
    manual_x=manual_sx+manual_ix#Se guarda el punto manual x en la variable
    automa_x=automa_sx+automa_ix#Se guarda el punto automático x en la variable
    manual_y=manual_sy+manual_iy#Se guarda el punto manual y en la variable
    automa_y=automa_sy+automa_iy#Se guarda el punto automático y en la variable
    
    error_x = mean_absolute_error(manual_x, automa_x)#Se calcula el mae para el eje x
    error_y = mean_absolute_error(manual_y, automa_y)#Se calcula el mae para el eje y
    error_final = (error_x + error_y) / 2#Se obtiene el mae al promediar el eje x y el eje y
    return error_final

def error_rmse(coordenadas_manuales, coordenadas_automaticas):
    """Función que calcula la raiz del error cuadrático medio de landmarks.
    
    Realiza el cálculo del error mae de las landmarks en pixeles.Para esto se debe ingresar 
    los archivos .mat en conjunto con su ubicación.
    La función realiza el cálculo de la raiz del error cuadrático medio de acuerdo 
    a la siguiente fórmula:
                                            ______________________
                                           |       N             |
                                           |      ___            |
                                   RMSE =  | 1    \            2 |
                                           | -    /   (Yi - Y*i) |
                                         \ | N    ___            |
                                          \|      i=1
    
    Donde:
    N                       : El total de puntos marcados
    Yi                      : Los puntos marcados manualmente
    Y*i                     : Los puntos marcados automáticamente
    
    Parámetros de entrada de la función:
    
    coordenadas_manuales    : Es el archivo .mat con los puntos marcados manualmente.
                              Se debe especificar la ruta donde esta el archivo .mat.
                              Por ejemplo: ./ruta/archivo/mat_manual.mat
    coordenadas_automaticas : Es el archivo .mat con los puntos marcados automáticamente
                              Se debe especificar la ruta donde esta el archivo .mat.
                              Por ejemplo: ./ruta/archivo/mat_automatico.mat
                              
    Parámetros de salida de la función:
    
    error_final             : Es el error en pixeles de las landmarks
    """
    manual_sx = []#Lista vacia para guardar la landmark superior manual en el eje x
    automa_sx = []#Lista vacia para guardar la landmark superior automática en el eje x
    manual_ix = []#Lista vacia para guardar la landmark inferior manual en el eje x
    automa_ix = []#Lista vacia para guardar la landmark inferior automática en el eje x
    manual_sy = []#Lista vacia para guardar la landmark superior manual en el eje y
    automa_sy = []#Lista vacia para guardar la landmark superior automática en el eje y
    manual_iy = []#Lista vacia para guardar la landmark inferior manual en el eje y
    automa_iy = []#Lista vacia para guardar la landmark inferior automática en el eje y
    
    ###############################Lectura de los archivos csv################################
    # archivo_manual = 'Manual_landmarks.csv'#Se leé el csv con las landmarks manual
    with open(coordenadas_manuales) as f:#Se guarda en el objeto f
        reader=csv.reader(f)#Se pasa la información a la variable reader
        header_row=next(reader)#Se va leyendo las filas del archivo
        lista_manual=[]#Se crea una lista donde se irá guardando los datos leídos
        for row in reader:#Ciclo para guardar los datos
            lista_manual.append(row)#Se va agregando los datos a las listas
    
    # archivo_automa = 'E:/Maestria/una_imagen/ipilab/Alignded_Images/Landmarks.csv'#Se leé el csv con las landmarks automáticas
    with open(coordenadas_automaticas) as f2:#Se guarda en el objeto f
        reader2=csv.reader(f2)#Se pasa la información a la variable reader
        header_row2=next(reader2)#Se va leyendo las filas del archivo
        lista_automa=[]#Se crea una lista donde se irá guardando los datos leídos
        for row2 in reader2:#Ciclo para guardar los datos
            lista_automa.append(row2)#Se va agregando los datos a las listas
    #####################################################################################
    for i in range(0,len(lista_manual)):#Ciclo para crear las lsitas donde se obtendrá el error
        nombrem,xsm,ysm,xim,yim=lista_manual[i]#Lista con los datos manuales
        nombrea,xsa,ysa,xia,yia=lista_automa[i]#Lista con los datos automáticos
        if nombrem==nombrea:#Si los nombres de la imagen automática y manual coinciden
            manual_sx.append(float(xsm))#Se agrega la lista correspondiente
            automa_sx.append(float(xsa))#Se agrega la lista correspondiente
            manual_sy.append(float(ysm))#Se agrega la lista correspondiente
            automa_sy.append(float(ysa))#Se agrega la lista correspondiente
            manual_ix.append(float(xim))#Se agrega la lista correspondiente
            automa_ix.append(float(xia))#Se agrega la lista correspondiente
            manual_iy.append(float(yim))#Se agrega la lista correspondiente
            automa_iy.append(float(yia))#Se agrega la lista correspondiente
    manual_x=manual_sx+manual_ix#Se guarda el punto manual x en la variable
    automa_x=automa_sx+automa_ix#Se guarda el punto automático x en la variable
    manual_y=manual_sy+manual_iy#Se guarda el punto manual y en la variable
    automa_y=automa_sy+automa_iy#Se guarda el punto automático y en la variable
    
    error_x = mean_squared_error(manual_x, automa_x, squared = False)#Se calcula el rmse para el eje x
    error_y = mean_squared_error(manual_y, automa_y, squared = False)#Se calcula el rmse para el eje y
    error_final = (error_x + error_y) / 2#Se obtiene el mae al promediar el eje x y el eje y
    return error_final#La funcón devuelve el error en pixeles

def archivo_log(ruta, test_total_im, test_tam, mae, rmse):
    """Crea un archivo tipo log con información sobre el set de entrenamiento y evalaución.
    
    Parámetros de entrada de la función:
    
    ruta          : Donde se desea guardar el archivo.
    test_total_im : Número total de imágenes evaluadas durante la evaluación.
    test_tam      : Tamaño de las imágenes de evaluación.
    mae           : Valor del error promedio absoluto.
    rmse          : Valor del error cuadrático promedio.
    
    Parámetros de salida de la función:
    
    información.log : Archivo con la información acerca del entrenamiento y la evaluación de las landmarks.
    """

    LOG_FILENAME = ruta + '/' + 'informacion.log'
    logging.basicConfig(level=logging.DEBUG, format= '%(asctime)s %(levelname)s : %(message)s',filename=LOG_FILENAME, filemode='w')
    logging.info('Las imágenes evaluadas son ' + test_total_im)
    logging.info('Donde su tamaño es de ' + test_tam)
    logging.info('El error mae es de ' + mae)
    logging.info('El error rmse es de ' + rmse)
    logging.shutdown()

def resultados(Directorio, num_imag_evaluadas, filas, columnas, archivo_manual, archivo_automatico):
    """Programa que crea el archivo log con información sobre el conjunto de evaluación.
    
    Parámetros de entrada de la función:
        
    Directorio         : Ruta donde se desea guardar el archivo log
    num_imag_evaluadas : Total de imágenes evaluadas.
    dimension_imag     : Tamaño de las imágenes evaluadas.
    archivo_manual     : Archivo csv con las landmarks manuales.
    archivo_automatico : Archivo csv con las landmarks automáticas.
    
    Parámetros de salida de la función:
    
    información.log    : Archivo con la información acerca del entrenamiento y la evaluación de las landmarks.
    """
    
    rmse = error_rmse(archivo_manual, archivo_automatico)#Se obtiene el error rmse
    mae = error_mae(archivo_manual, archivo_automatico)#Se obtiene el error mae
    dimensiones = str(filas) + 'x' + str(columnas)
    archivo_log(Directorio, str(num_imag_evaluadas), dimensiones, str(mae), str(rmse))#Se crea el archivo log