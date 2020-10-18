#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 20 17:33:10 2019

@author: longinos
"""

import numpy as np
import cv2
import matplotlib.pyplot as plt
from skimage.morphology import binary_closing, disk

#    angulos =np.linspace(0,359,360)
#    angulos = (angulos/360) * (2 * np.pi)

def polar_graph(angulos,hist):
    
    ax = plt.subplot(111, polar=True)  # Crea una sub-grafica
    ax.set_theta_zero_location('E')  # elige la orientacion de la grafica polar
    
    for i in range(360):
        ax.plot((0,angulos[i]), (0,hist[i]), zorder = 3)
    plt.show()
