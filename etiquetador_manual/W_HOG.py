#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 16 11:00:24 2019

@author: longinos
"""
import numpy as np
import cv2
from hist_weight import hist_weight
import matplotlib.pyplot as plt

def W_HOG (imagen, h_mask, gradiente="sobel",debug=0):
    
    imagen = imagen.astype(np.float_)
    
    filas, columnas = imagen.shape

    if gradiente == "sobel":
        ###Se obtiene el grandiente de dirección de la imagen
        sx = cv2.Sobel(np.float32(imagen), cv2.CV_32F, 1, 0)
        sy = cv2.Sobel(np.float32(imagen), cv2.CV_32F, 0, 1)
    else:#gradiente == "prewit":
        ###Se obtiene el grandiente de dirección de la imagen
        sx = cv2.Sobel(np.float32(imagen), cv2.CV_32F, 1, 0)
        sy = cv2.Sobel(np.float32(imagen), cv2.CV_32F, 0, 1)
    
    if debug:
        plt.imshow(sx)
        plt.show()
        plt.imshow(sy)
        plt.show()
    
    Gmag, Gdir = cv2.cartToPolar(sx, sy, angleInDegrees=True)
    
    hist_wieghted = hist_weight(h_mask,Gmag, Gdir, filas, columnas)
    
    hist_scaled = np.round(hist_wieghted)
    
    return hist_scaled