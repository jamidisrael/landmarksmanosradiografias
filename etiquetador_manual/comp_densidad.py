#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 13 15:07:49 2019

esta funcion pretende medir la diferencia de densidad de una matriz de bordes  tomando como argumento:
    la imagen
    angulo "dominante
    
@author: longinos
"""
from skimage.morphology import binary_closing, disk
import numpy as np
import cv2
import matplotlib.pyplot as plt
import math
# from Corregir_Contraste import correccion

import warnings


def comp_densidad(im, ang_dom, kernel_size,debug=0):
    
#    print(im.shape)
#    ang_dom = ang_dom + 90
    
#    im2 = im.copy()
    ang_dom = ang_dom%360
    
    if debug:
        if ang_dom>=0 and ang_dom<=90:
            xx=np.linspace(0,im.shape[0]/2,im.shape[0])
            ang_dom_dg=ang_dom*(math.pi/180)
            yy=np.sin(ang_dom_dg)*(xx/np.cos(ang_dom_dg))
            
            
        elif ang_dom>90 and ang_dom<=180:
            xx=-np.linspace(0,im.shape[0]/2,im.shape[0])
            ang_dom_dg=ang_dom*(math.pi/180)
            yy=np.sin(ang_dom_dg)*(xx/np.cos(ang_dom_dg))
            
            
        elif ang_dom>180 and ang_dom<=270:
            xx=-np.linspace(0,im.shape[0]/2,im.shape[0])
            ang_dom_dg=ang_dom*(math.pi/180)
            yy=np.sin(ang_dom_dg)*(xx/np.cos(ang_dom_dg))
            
        elif ang_dom>270 and ang_dom<=360:
            xx=np.linspace(0,im.shape[0]/2,im.shape[0])
            ang_dom_dg=ang_dom*(math.pi/180)
            yy=np.sin(ang_dom_dg)*(xx/np.cos(ang_dom_dg))
    
        xx=xx+im.shape[0]/2+kernel_size
        yy=yy+im.shape[1]/2+kernel_size
                
    
    
#    im = cv2.Canny(im,70,100) #Valores para obtener los bordes 70,100
    
    filas, columnas = im.shape
    mask=disk(np.round(filas/2))
    mask = cv2.resize(mask, (im.shape))
    mask_1 = mask.copy()
    
    mask = np.pad(mask,(kernel_size,kernel_size),'constant', constant_values=(0,0))
    mask_1 = np.pad(mask_1,(kernel_size,kernel_size),'constant', constant_values=(0,0))
    im = np.pad(im,(kernel_size,kernel_size),'constant', constant_values=(0,0))

#    print(im.shape)
#    plt.imshow(mask,cmap="gray")
#    plt.show()

    promedio_gris = np.sum(im)/np.sum(mask_1)
        
    half = np.zeros((mask.shape[0],mask.shape[1]//2) )
    
    if im.shape[0]%2!=0:
        mask[:,:mask.shape[1]//2] = half 
        mask_1[:,mask.shape[1]//2+1:] = half
    else:
        mask[:,:mask.shape[1]//2] = half 
        mask_1[:,mask.shape[1]//2:] = half
    

    
    (cx,cy) = im.shape
    
    center= (cx//2,cy//2)
    
    M = cv2.getRotationMatrix2D(center,-ang_dom, 1.0)
    
    r_mask_1 = cv2.warpAffine(mask, M, (im.shape[1],im.shape[0]))
    r_mask_2 = cv2.warpAffine(mask_1, M, (im.shape[1],im.shape[0]))
    
#    plt.plot(xx,yy)
#    plt.imshow(r_mask_1,cmap="gray")
#    plt.show()
    
#    plt.plot(xx,yy)
#    plt.imshow(r_mask_2,cmap="gray")
#    plt.show()

    im_mask_1 = im*r_mask_1
    im_mask_2 = im*r_mask_2
    
#    plt.title("im_mask_1")
#    plt.plot(xx,yy)
#    plt.imshow(im_mask_1,cmap="gray")
#    plt.show()
#    
#    plt.title("im_mask_2")im
#    plt.plot(xx,yy)#    im_mirror= cv2.flip(imagen, 1)
#    plt.imshow(im_mask_2,cmap="gray")im
#    plt.show()im
    
    vec_1 = np.array([])
    vec_2 = np.array([])
    
    for j in range(kernel_size, im.shape[0]-kernel_size):
        for i in range (kernel_size, im.shape[1]-kernel_size):
            if im_mask_1[i,j]>=promedio_gris:
                suma = np.sum(im_mask_1[i-kernel_size:i+kernel_size+1,j-kernel_size:j+kernel_size+1])
                vec_1 = np.append(vec_1,suma)
            
    for j in range(kernel_size, im.shape[0]-kernel_size):
        for i in range (kernel_size, im.shape[1]-kernel_size):
            if im_mask_2[i,j]>=promedio_gris:
                suma = np.sum(im_mask_2[i-kernel_size:i+kernel_size+1,j-kernel_size:j+kernel_size+1])
                vec_2 = np.append(vec_2,suma)
    
    
    if debug:
        
#        plt.title("im_mask_1 \n densidad "+str(int(np.mean(vec_1)))+"\n numero de pixeles " + str(len(vec_1)))
        plt.plot(xx,yy)
        plt.imshow(im_mask_1,cmap="gray")
        plt.show()
        
#        plt.title("im_mask_2 \n densidad "+str(int(np.mean(vec_2)))+"\n numero de pixeles " + str(len(vec_2)))
        plt.plot(xx,yy)#    im_mirror= cv2.flip(imagen, 1)
        plt.imshow(im_mask_2,cmap="gray")
        plt.show()
        
        
        plt.title("im_mask_1 \n densidad "+str(np.sum(im*r_mask_1)/np.sum(r_mask_1)))
        plt.plot(xx,yy)
        plt.imshow((im*r_mask_1),cmap="gray")
        plt.show()
        
        plt.title("im_mask_2 \n densidad "+str(np.sum(im*r_mask_2)/np.sum(r_mask_2)))
        plt.plot(xx,yy)
        plt.imshow((im*r_mask_2),cmap="gray")
        plt.show()
    
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", category=RuntimeWarning)
        try:
            mean1 = np.mean(vec_1)
        except:
            mean1=0
            
        try:
            mean2 = np.mean(vec_2)
        except:
            mean2=0
        
    if mean1>mean2:
#        print("1>>2")
        return True 
    else:
#        print("2>>1")
        return False