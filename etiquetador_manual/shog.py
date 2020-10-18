#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 21 00:17:25 2019

entradas:
imagen cuadradda
tipo de gradiente: prewit sobel roberts
nota:revisar funcion de canni, endonde se especifique el tipo de gradiente.
investigar regla de aplicacion de kernel para busquedda de borde.


debe devolver:
el histograma normalizado
la imagen des rotada
el angiulo dominante


@author: longinos
"""
import numpy as np
import cv2
import matplotlib.pyplot as plt
from skimage.morphology import binary_closing, disk
from rot_image_masscenter import rot_image_masscenter
from bin_sum import bin_sum
from polar_graph import polar_graph
from angulo_dominante_fix import angulo_dominante_fix
from W_HOG import W_HOG
from comp_densidad import comp_densidad

def shog(imagen,ventana=90,gradiente="sobel",debug=0):
    
    filas, columnas = imagen.shape

    h_mask=disk(np.round(filas/2))
    h_mask = cv2.resize(h_mask, (imagen.shape))
    
    hist_scaled = W_HOG (imagen,h_mask)
    
    col_res, row_res = rot_image_masscenter(imagen)
    
    rho,theta = bin_sum(hist_scaled, ventana)
    
##################################################
    if debug:
        angulos =np.linspace(0,359,360) 
        angulos = (angulos/360) * (2 * np.pi)
        polar_graph(angulos,hist_scaled.T)
        
        plt.title("centro de masa en "+ str(col_res) + " "+ str(row_res)+"\n"+"centro de la imagen "+ str(filas/2) + " "+ str(columnas/2) )
        plt.plot(imagen.shape[0]//2,imagen.shape[1]//2,"ro")
        plt.plot(col_res,row_res,"bo")
        plt.imshow(imagen)
        plt.show()
        
        polar_graph(angulos,rho.T)
#################################################
    
    col_res = -(col_res - imagen.shape[0]//2)
    row_res = row_res - imagen.shape[1]//2

    angulodominante = angulo_dominante_fix(rho,theta,col_res, row_res)

    im_mirror= imagen.copy()
    
    k_size=im_mirror.shape[0]//4
    if comp_densidad(im_mirror,angulodominante,k_size):
        angulodominante=(angulodominante+180)%360
    resta=360-angulodominante#israel agrego
    angulodominante=resta+angulodominante##israel agrego
    (h, w) = imagen.shape[:2]
    
    center = (w / 2, h / 2)
    
    M = cv2.getRotationMatrix2D(center, angulodominante, 1.0)
    
    rotated = cv2.warpAffine(imagen, M, (w, h))
    
    rotated = rotated * h_mask
    
    return rotated, angulodominante