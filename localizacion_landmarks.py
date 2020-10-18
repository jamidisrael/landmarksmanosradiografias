# -*- coding: utf-8 -*-
"""
Created on Mon Sep 28 20:44:05 2020

@author: israe
"""

import cv2
import numpy as np
from skimage.morphology import disk
from rotador import shog
from numpy import linalg as la
import scipy.io as sio

def im_projection(testface,im_av, eig_faces,row_num, col_num):
    #se adquiere el numero de eigenfaces
    k= eig_faces.shape[1]
    #se lee la imagen que se desea proyectar
    #se le resta la imagen promedio
    testface= testface - im_av
    #se define un vector para almacenar los pesos que se calculen
    omegatest=np.zeros((k,1))
    #se define un vector para almacenar la proyeccion de la imagen
    sum_com=np.zeros((row_num*col_num,1))
    #se itera por el numero de eigen face
    for i in range(0,k):
        #se calcula el peso correspondiente de la imagen con cada eigen face
        w=np.matmul(eig_faces [:,i].T,testface)
        #se almacena el peso en un vector columna
        omegatest[i,0]=w
        #se calcula la recosntruccion mutiplicando cada peso por su correspondiente eigenfacce
        component=w*eig_faces [:,i].reshape(row_num*col_num,1)
        #se calcula la sumatoria de componentes
        sum_com+=component
    #se suma la imagen promedio
    im_proy=sum_com+im_av
    #se redimesiona la imagen promedio para adquirir su tamaño original
    im_proy=im_proy.reshape(row_num,col_num)
    #se devuelven los valores de los pesos junto con la imagen proyecctada
    return omegatest, im_proy

def min_localizer(imagen_entrada, mean0, k_eig_faces0, row_num0, col_num0, omega0):
    """
    Localiza las coordenadas del punto mínimo, el cual será donde se encuentre una landmark.
    
    Función que realiza la búsqueda de landmark en la imagen radiográfica. Se necesita la 
    imagen a evaluar, el vector promedio, la matriz de eigenfaces, el valor de las filas y
    columnas y el vector omega o pesos.
    
    Entradas:
        imagen --> Imagen a evaluar
        cx --> Valor en el eje x del centroide de la imagen
        cy --> Valor en el eje y del centroide de la imagen
        dimension_ventana --> Tamaño de la ventana donde se realizará la búsqueda
        vector_promedio --> Vector promedio del vector de eigenfaces
        vector_eigenfaces --> Matriz donde se proyectará la imagen a evaluar
        num_filas --> Valor de las filas
        num_columnas --> valor de las columnas
        omega_vec --> Vector de omega o pesos de las eigenfaces
    Salidas:
        oxp0 --> Cooredenda en el eje x de la landmark localizada
        oyp0 --> Cooredenda en el eje y de la landmark localizada
    """

    ventana = imagen_entrada#Se crea una variable para la imagen a evaluar
    kernel_size = row_num0 // 2#kernel es el parche que se tomara para proyectarse al eigenespacio,se divide en dos para el proceso
    kernel_size = int(kernel_size)#Se vuelve entero
    error0= np.zeros(ventana[kernel_size : - (kernel_size), kernel_size : - (kernel_size)].shape)#se generan la matriz en donde se almacenará el valor de error para cada eigenespacio
    #se compienza el procedimiento
    for i in range(kernel_size, ventana.shape[0] - (kernel_size)):#Se comienza desde el primer valor del kernel, para el segundo límite se va restando el valor del kernel al de las filas
        for j in range (kernel_size, ventana.shape[1] - (kernel_size)):#Se comienza en el primer valor del kernel, para el segundo límite resta el valor del kernel al de las columnas
           #Ventana de busqueda
            parche = ventana[i - kernel_size : i + (kernel_size), j - kernel_size : j + (kernel_size)]#Se va recorriendo la ventana pixelxpixel
            parche_rotado, angulo_domm = shog(parche)#Se obtiene el parche ya rotado de acuerdo a su ángulo dominate
            filas = parche.shape[0]#Se obtiene el valor de las filas del parche
            h_mask = disk(np.round(filas / 2))#Se crea una máscara circular al parche
            h_mask = cv2.resize(h_mask, (parche.shape))#La máscara se pasa al tamaño del parche
            parche_rotado = parche_rotado * h_mask#Se aplica la máscara circular al parche
            parche_rotado = parche_rotado.reshape(parche.shape[1] ** 2, 1)#Se vuelve un vector el parche
            row_num0 = int(row_num0)#Se vuelve valor entero las filas
            col_num0 = int(col_num0)#Se vuelve valor entero las columnas
            omegatest0, proyeccion0 = im_projection(parche_rotado, mean0.T, k_eig_faces0, row_num0, col_num0)#Se proyecta el parche
            proyeccion = proyeccion0.reshape(proyeccion0.shape[0] * proyeccion0.shape[0], 1)#Se vuelve vector la proyección
            c = parche_rotado - proyeccion#Se restael parche original y su proyección
            norma = la.norm(c, axis=0)#Se aplica la norma
            error0[i - kernel_size, j - kernel_size] = norma#Se va guardando el valor de la norma en la matriz de error
    points = 1#Se muestra solo el punto mínimo
    mins0 = np.argsort(error0.reshape(error0.shape[0] * error0.shape[1], 1), axis=0)[: points]#Se vuelve vector la matriz de errores y se ordena de menor a mayor de acuerdo a su índice
    xx0, yy0 = np.unravel_index(mins0, error0.shape)#De acuerdo al valor del mínimo, se obtiene la coordenada que le corresponde
    oyp0 = xx0 + kernel_size#Se realiza la suma con el valor del kernel, para que se regrese el valor de coordenada de acuerdo a la imagen de entrada
    oxp0 = yy0 + kernel_size#Se realiza la suma con el valor del kernel, para que se regrese el valor de coordenada de acuerdo a la imagen de entrada
    return int(oxp0[0,0]), int(oyp0[0,0])#Se regresa la coordenada de la landmark

def carga_archivosmat(direccioncarpeta, eigenfaces, omega, vectorpromedio, filas, columnas):
    """Carga los 4 archivos .mat del programa de eigenfaces.
    
    Función que carga los archivos de entrenamiento de eigenfaces, para poder ocuparlos en la parte de 
    evaluación. Con esto se omite el estar ejecutando y obteniendo todos los valores de eigenfaces, los 
    pesos, entre otros.
    Al colocar los nombres de las variables, estas deben ir con comilla simple y sin la extensión de este.
    
    Entradas:
        direccioncarpeta --> Ubicación de los archivos .mat a cargar
        eigenfaces --> Archivo de eigenfaces
        omega --> Archivo con los pesos u omega
        vectorpromedio --> Archivo del vector promedio de las imagenes de eigenfaces
        filas --> Número de filas de las imágenes ocupadas
        columnas --> Número de columnas de las imágenes ocupadas
    Salidas:
        mateigenfaces --> Eigenafaces en tipo array
        matomega --> Omega en tipo array
        matvectorpromedio --> Vector promedio en tipo array
        matfilas --> Valor de las filas en tipo array
        matcolumnas --> Valor de las columnas en tipo array
        
    Ejemplo:
    eigenfaces, omega, vectorpromedio, filas, columnas = carga_arcvhivosmat('./', 'archivo_eigenfaces', 'archivo_omega', archivo_vectorpromedio, archivo_filas, archivo_columnas)
    """
    
    mateigenfaces = sio.loadmat(direccioncarpeta + eigenfaces + '.mat')#Se carga la matriz de eigenfaces
    matomega = sio.loadmat(direccioncarpeta + omega +'.mat')#Se cargan los pesos
    matvectorpromedio = sio.loadmat(direccioncarpeta + vectorpromedio +'.mat')#Se carga el vecto pormedio
    matfilas = sio.loadmat(direccioncarpeta + filas +'.mat')#Se carga el valor de las filas
    matcolumnas = sio.loadmat(direccioncarpeta + columnas +'.mat')#Se carga el valor de las columnas
 
 
    return mateigenfaces[eigenfaces], matomega[omega], matvectorpromedio[vectorpromedio], matfilas[filas], matcolumnas[columnas]#Se coloca el nombre del archivo en corchetes junto con su varibale, para que se pase a matrices, sin necesidad de hacer esto en lineas extras.

def localizacion_landmarks(im_correccion):
    """Programa para localizar las landmarks en las imágenes radiográficas.
    
    Parámetros de entrada de la función:
    im_correccion : Imagen corregida en contraste y ángulo
    """
    ###############################################
    ########## Tercer nivel piramide ##############Mayor resolución
    #Carga de archivos mat
    #Espacio 0
    k_eig_faces0M, omega0M, mean0M, row_num0M, col_num0M = carga_archivosmat('./espacios/p0/', 'k_eig_faces0M', 'omega0M', 'mean0M', 'row_num0M', 'col_num0M')
    #Espacio 1
    k_eig_faces1M, omega1M, mean1M, row_num1M, col_num1M = carga_archivosmat('./espacios/p0/', 'k_eig_faces1M', 'omega1M', 'mean1M', 'row_num1M', 'col_num1M')
    ###############################################
    ########## Segundo nivel piramide ##############Resolución Media
    #Carga de archivos mat
    #Espacio 0
    k_eig_faces0D, omega0D, mean0D, row_num0D, col_num0D = carga_archivosmat('./espacios/p1/', 'k_eig_faces0d', 'omega0d', 'mean0d', 'row_num0d', 'col_num0d')
    #Espacio 1
    k_eig_faces1D, omega1D, mean1D, row_num1D, col_num1D = carga_archivosmat('./espacios/p1/', 'k_eig_faces1d', 'omega1d', 'mean1d', 'row_num1', 'col_num1d')
    ###############################################
    ########### Primer nivel de la piramide ###############
    #Carga de archivos mat
    #Espacio 0
    k_eig_faces0m, omega0m, mean0m, row_num0m, col_num0m = carga_archivosmat('./espacios/p2/', 'k_eig_faces0m', 'omega0m', 'mean0m', 'row_num0m', 'col_num0m')
    #Espacio 1
    k_eig_faces1m, omega1m, mean1m, row_num1m, col_num1m = carga_archivosmat('./espacios/p2/', 'k_eig_faces1m', 'omega1m', 'mean1m', 'row_num1m', 'col_num1m')
    ###############################################
    #######Zona de busqueda de la parte superior#######
    p0_iy = 48
    p0_fy = 142
    p0_ix = 116
    p0_fx = 150
    ########Zona de busqueda de la parte inferior##########
    p1_iy = 115
    p1_fy = 195
    p1_ix = 109
    p1_fx = 150
    kernel = 32#tamaño del kernel de busqueda
    side = kernel // 2#Se divide el kernel a la mitad
    #######################reducciones de escala#####################
    reduccion1 = cv2.pyrDown(im_correccion).astype('uint8')#Se reduce a 128x128 pixeles
    reduccion2 = cv2.pyrDown(reduccion1).astype('uint8')#Se reduce a 64x64 pixeles
    ###########################################
    ##################################################Resolucion menor###########################################
    #######Búsqueda de la landmark superior#######
    cte = 12#valor para la ventana de búsqueda
    reduccion_2ceros = np.pad(reduccion2, (cte, ), 'constant', constant_values = (0, ))#se agregan los ceros
    ventana_s0m = reduccion_2ceros[(p0_iy // 4) + cte - side : (p0_fy // 4) + cte + side, (p0_ix // 4) + cte - side : (p0_fx // 4) + cte + side]#Ventana de resolucion menor a evaluar
    x0m, y0m = min_localizer(ventana_s0m, mean0m, k_eig_faces0m, row_num0m, col_num0m, omega0m)#se busca la landmark en la parte sueprpo
    ###########landmark superior en menor resolucion########################
    ps0mx = x0m + p0_ix // 4 - side
    ps0my = y0m + p0_iy // 4 - side
    ######Búsqueda de la landmark inferior
    ventana_i1m = reduccion2[p1_iy // 4 - side : p1_fy // 4 + side, p1_ix // 4 - side : p1_fx // 4 + side]#ventana de menor resolucion
    x1m, y1m = min_localizer(ventana_i1m, mean1m, k_eig_faces1m, row_num1m, col_num1m, omega1m)#Búsqueda de la landmark
    ##############landmark inferior en menor resolucion
    pi1mx = x1m + p1_ix // 4 - side
    pi1my = y1m + p1_iy // 4 - side
##################################################resolucion media#################################################
    ########Se busca la landmark superior
    reduccion_2ceros = np.pad(reduccion1, (cte, ), 'constant', constant_values = (0, ))#se agregan los ceros
    ventana_s0d = reduccion_2ceros[(ps0my * 2 - 2) + cte - side : (ps0my * 2 + 2) + cte + side, (ps0mx * 2 - 2) + cte - side : (ps0mx * 2 + 2) + cte + side]#venatana de resolucion media superior
    x0d, y0d = min_localizer(ventana_s0d, mean0D, k_eig_faces0D, row_num0D, col_num0D, omega0D)#Se busca el punto
    #######Se busca la landmark inferior
    ventana_i1d = reduccion1[pi1my * 2 - 4 - side : pi1my * 2 + 4 + side, pi1mx * 2 - 4 - side : pi1mx * 2 + 4 + side]###Ventana de resolución media de la zona inferior
    x1d, y1d = min_localizer(ventana_i1d, mean1D, k_eig_faces1D, row_num1D, col_num1D, omega1D)#Se busca el punto
############################Landmarks resolucion media############################
    ps0dx = x0d + (ps0mx * 2 - 2 - side)#landmark zona superior
    ps0dy = y0d + (ps0my * 2 - 2 - side)#landmark zona superior
    pi1dx = x1d + (pi1mx * 2 - 4 - side)#landmark zona inferior
    pi1dy = y1d + (pi1my * 2 - 4 - side)#landmark zona inferior
#################################################resolucion mayor (búsqueda final)##################################
    ####Se busca la landmark superior
    ceros_orig = np.pad(im_correccion, (cte, ), 'constant', constant_values = (0, ))#se agregan los ceros
    ventana_s0M = ceros_orig[(ps0dy * 2 - 4) + cte - side : (ps0dy * 2 + 4) + cte + side, (ps0dx * 2 - 4) + cte - side : (ps0dx * 2 + 4) + cte + side]#venatana de resolucion menor a evaluar
    x0M, y0M = min_localizer(ventana_s0M, mean0M, k_eig_faces0M, row_num0M, col_num0M, omega0M)#Se busca el punto
    #####Se busca la landmark inferior
    ventana_i1M = im_correccion[pi1dy * 2 - 4 - side : pi1dy * 2 + 4 + side, pi1dx * 2 - 4 - side : pi1dx * 2 + 4 + side]#venatana de resolucion menor a evaluar
    x1M, y1M = min_localizer(ventana_i1M, mean1M, k_eig_faces1M, row_num1M, col_num1M, omega1M)#Se busca el punto
    #########################################Landmarks finales##############################
    sx = x0M + (ps0dx * 2 - 4 - side)#landmark zona superior
    sy = y0M + (ps0dy * 2 - 4 - side)#landmark zona superior
    ix = x1M + (pi1dx * 2 - 4 - side)#landmark zona inferior
    iy = y1M + (pi1dy * 2 - 4 - side)#landmark zona inferior
    ####Se van guardando los puntos
    ##############################Archivo CSV####################################
    puntos=[sx,sy,ix,iy]#Se guardan los valores en una lista
    # coor_aut.update({im:puntos})#Se alamcena el nombre de la imagen y las coordenadas en un diccionario
    return puntos