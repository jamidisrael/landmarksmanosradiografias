# -*- coding: utf-8 -*-
"""
Created on Mon Sep 28 20:02:46 2020

@author: israe
"""
from tkinter import *
from tkinter.filedialog import askdirectory
import os
from os import walk
from resultados import resultados
import cv2
from pre_procesamiento import contraste_imagen
from rotador import shog
from localizacion_landmarks import localizacion_landmarks
from landmarks_csv import landmarks_csv
import pathlib
import tkinter.messagebox


if __name__ == '__main__':#Se dice a python que este es el programa principal
    # seleccion de carpeta de imagenes
    root = Tk()
    root.withdraw()
    root.attributes("-topmost", True)
    Directory = askdirectory(title = 'Choose an image.')
    # adquisicion de archivos dentro de la carpeta actual
    for dirpath, dirnames, filenames in walk(Directory): 
        print(filenames)
        break
    #Se inicializan variables
    coor_aut = {}#Diccionario para guardar los puntos en el csv
    puntos_mat = {}#Diccionario para guardar los puntos en el mat
    Directorio = Directory + '/Alignded_Images/Estimated_landmarks_images'#Se crea la carpeta donde se guardan los resultados
    pathlib.Path(Directorio).mkdir(parents=True, exist_ok=True)#Crea la carpeta y si ya existe la deja
    contador_imagenes = 0#Contador para saber cuantas imagenes se evaluaran
    
    for im in filenames:
        if im[-3:] == 'jpg' or im[-3:] =='png':#Se leen unicamente con el formato png y jpg
          ruta = Directory + '/' + im#Crea la ruta donde esta la imagen
          imagen = cv2.imread(ruta,0)#color.rgb2gray(io.imread(ruta))#Carga la imagen y la convierte a uint8
          imagen_cuadrada = contraste_imagen(imagen)#se obtiene la mano con su circunferencia y de 256x256
          c_pos, angulo = shog(imagen_cuadrada, ventana=90)#Se rota la imagen
          cv2.imwrite(Directory + '/Alignded_Images/' + 'aligned_'+im, c_pos)#Se guarda la imagen corregida sin los puntos
          punto = localizacion_landmarks(c_pos)
          ##############################Archivo CSV####################################
          coor_aut.update({im:punto})#Se alamcena el nombre de la imagen y las coordenadas en un diccionario
          #####################Se guarda la imagen en opencv#######################
          colores=(255, 0, 0)#Se habilita rgb
          c_pos = cv2.cvtColor(c_pos, cv2.COLOR_GRAY2RGB)#Se convierte a rgb
          puntos = cv2.circle(c_pos, (punto[2], punto[3]), 1, colores, - 1)#Se coloca la landmark superior
          puntos = cv2.circle(puntos, (punto[0], punto[1]), 1, (0, 0, 255), - 1)#Se coloca la landmark inferior
          cv2.imwrite(Directorio +'/'+ 'aligned_' + str(im), puntos)#Se guarda la imagen con los puntos en carpeta
          contador_imagenes += 1
    ##################Finaliza el codigo de búsqueda de puntos y proceso de la mano
    landmarks_csv(Directory + '/Alignded_Images',coor_aut)#Se guarda el archivo csv con las landmarks automáticas
    ####################################Proceso para guardar información sobre la evaluación
    for doc in filenames:#Se inica un ciclo para leer los archivos en la carpeta raiz
        if doc == 'Manual_landmarks.csv':#Si se encuentra el archivo con las landmarks manuales
            resultados(Directory + '/Alignded_Images', contador_imagenes, imagen_cuadrada.shape[0],imagen_cuadrada.shape[1], Directory + '/Manual_landmarks.csv', Directory + '/Alignded_Images/Landmarks.csv')#Se genera el archivo log
    contador_imagenes = 0#Se reinicia el contador de las imágenes
    tkinter.messagebox.showinfo("Terminado", "La localización ha finalizado")#Mensaje que finaliza el programa