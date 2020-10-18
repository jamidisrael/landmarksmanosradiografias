#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 20 17:48:54 2019

@author: longinos
"""



import numpy as np
import cv2
import matplotlib.pyplot as plt
from skimage.morphology import binary_closing, disk

def bin_sum(h_var, ventana):
    vector = np.arange(360)
    vector.resize(1,360)

    X,Y = cv2.polarToCart(h_var,vector*(np.pi/180))
    
    X_nueva = np.zeros((1,360))
    Y_nueva = np.zeros((1,360))
    
    for i in range(0,360):
        if((i+ventana-1)>360):
            topeX=(i+ventana-1) -360
            topeY=(i+ventana-1) -360
            
            X1=X[0,i:360].reshape(i-360,1)
            X2=X[0,0:topeX].reshape(topeY,1)
            
            if X1.shape[0] == 0  :
                XX = X2
            elif X2.shape[0] == 0:
                XX = X1
            else:
                XX = np.append(X1,X2)
                 
            Y1=Y[0,i:360].reshape(i-360,1)
            Y2=Y[0,0:topeY].reshape(topeY,1)
           
            if Y1.shape[0] == 0  :
                YY = Y2
            elif Y2.shape[0] == 0:
                YY = Y1
            else:
                YY = np.append(Y1,Y2)
    
        else:
           XX = X[0,i:i+ventana-1]
           YY = Y[0,i:i+ventana-1]
        
        pond= np.linspace(0,1,ventana-1)
        
#        print(XX.shape)
#        print(pond.shape)
        
        X_nueva[0,i]=np.sum(XX*pond)/ventana
        Y_nueva[0,i]=np.sum(YY*pond)/ventana
       
        rho,theta = cv2.cartToPolar(X_nueva,Y_nueva)
       
    return rho,theta