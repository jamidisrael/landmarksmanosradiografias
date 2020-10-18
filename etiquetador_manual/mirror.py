#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 20 18:04:43 2019

@author: longinos
"""



import numpy as np
import cv2
import matplotlib.pyplot as plt
from skimage.morphology import binary_closing, disk

def mirror(indice, mRHO):
    
    if (indice-90) <= 0:
        mRHO[0,0:indice+90] = 0
        mRHO[0,360 + (indice-90)+1:360] = 0
    elif (indice+90) > 360:
        mRHO[0,indice-90:360] = 0;
        mRHO[0,0:(indice+90) - 360 - 1] = 0
    else:
        mRHO[0,indice-90:indice+90] = 0
    return mRHO
    