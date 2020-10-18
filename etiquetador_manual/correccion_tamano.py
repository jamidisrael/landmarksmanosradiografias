# -*- coding: utf-8 -*-
"""
Created on Wed Feb 12 21:02:16 2020

@author: israe
"""

import cv2

def correccion_tamano(ruta, imagen):
    imagen = cv2.imread(ruta,0)
    