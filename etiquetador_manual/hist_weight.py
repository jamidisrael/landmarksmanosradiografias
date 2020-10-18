#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 20 18:50:05 2019

@author: longinos
"""


import numpy as np
import cv2
import matplotlib.pyplot as plt
from skimage.morphology import binary_closing, disk

def hist_weight(h_mask,Gmag, Gdir, filas, columnas):
    
    hist_wieghted = np.zeros((1,360))
    
    # Se hace una busqueda en cada pixel de la imagen
    
    for i in range(0,filas):
        for j in range(0,filas):
            if (round(Gdir[i,j]+180) ==0):
                angle = 360
                angle = int(angle)
            else:
                angle = round(Gdir[i,j]+180)
             
                angle = int(angle)

            hist_wieghted[0,angle%360]=hist_wieghted[0,angle%360]+h_mask[i,j]*Gmag[i,j]
          
    return hist_wieghted
