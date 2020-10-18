#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 20 17:04:08 2019

@author: longinos
"""
import numpy as np
import cv2
import matplotlib.pyplot as plt
from skimage.morphology import binary_closing, disk
# from Corregir_Contraste import correccion


def rot_image_masscenter(imagen):
   
   imagen=imagen.astype(np.float_)
   
   filas, columnas = imagen.shape
   
   h_mask=disk(np.round(filas/2))
   h_mask = cv2.resize(h_mask, (imagen.shape))
   image = imagen * h_mask # correccion(imagen,sigma=1.5)*h_mask
   
   col_res = 0
   row_res = 0
   
   for i in range(0,filas):
      for j in range(0,columnas):
         if h_mask[i,j]:
            col_res = col_res + image[i,j]*j
            row_res = row_res + image[i,j]*i 
         
   col_res = col_res/(np.sum(image)+2.2250738585072014e-308)
   row_res = row_res/(np.sum(image)+2.2250738585072014e-308)
   
#   plt.title("centro de masa en "+ str(col_res) + " "+ str(row_res)+"\n"+"centro de la imagen "+ str(filas/2) + " "+ str(columnas/2) + "\n norma del centro de masa " + str(np.linalg.norm(((col_res-filas/2),(row_res-columnas/2)))))
#   plt.plot(imagen.shape[0]//2,imagen.shape[1]//2,"co")
#   plt.plot(col_res,row_res,"go")
#   plt.imshow(image,cmap="gray")
#   plt.show()
   
   return col_res, row_res

#######################################

#   contours = cv2.findContours(image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
#   mayor_contorno = max(contours, key = cv2.contourArea)
#   
#   M = cv2.moments(mayor_contorno)
#   cx = int(M['m10']/M['m00'])
#   cy = int(M['m01']/M['m00'])
#   plt.title("centro de masa en "+ str(cx) + " "+ str(cy)+"\n"+"centro de la imagen "+ str(filas/2) + " "+ str(columnas/2) )
#   plt.plot(imagen.shape[0]//2,imagen.shape[1]//2,"ro")
#   plt.plot(cx,cy,"bo")
#   plt.imshow(image)
#   plt.show()
#   return cx,cy

#####################################33
          
#   blur = cv2.GaussianBlur(image,(3,3),0)
#  
#   BW_canny = cv2.Canny(blur,150,300)#(I,50,100)
#  
#   M = cv2.moments(BW_canny)
#   cx = int(M['m10']/M['m00'])
#   cy = int(M['m01']/M['m00'])
#
#   plt.title("centro de masa en "+ str(cx) + " "+ str(cy)+"\n"+"centro de la imagen "+ str(filas/2) + " "+ str(columnas/2) )
#   plt.plot(imagen.shape[0]//2,imagen.shape[1]//2,"ro")
#   plt.plot(cx,cy,"bo")
#   plt.imshow(BW_canny)
#   plt.show()
#   plt.imshow(image)
#   plt.show()
#   return cx,cy
   

   
