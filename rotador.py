# -*- coding: utf-8 -*-
"""
Módulo que contiene las funciones que se utlizan para corregir el ángulo
de la mano.

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
from sklearn.preprocessing import normalize
import math
import warnings
# from rot_image_masscenter import rot_image_masscenter
# from bin_sum import bin_sum
# from polar_graph import polar_graph
# from angulo_dominante_fix import angulo_dominante_fix
# from W_HOG import W_HOG
# from comp_densidad import comp_densidad

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
   return col_res, row_res

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
        X_nueva[0,i]=np.sum(XX*pond)/ventana
        Y_nueva[0,i]=np.sum(YY*pond)/ventana
        rho,theta = cv2.cartToPolar(X_nueva,Y_nueva)
    return rho,theta

def polar_graph(angulos,hist):
    ax = plt.subplot(111, polar=True)  # Crea una sub-grafica
    ax.set_theta_zero_location('E')  # elige la orientacion de la grafica polar
    
    for i in range(360):
        ax.plot((0,angulos[i]), (0,hist[i]), zorder = 3)
    plt.show()

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

def angulo_dominante_fix(rho,theta,x_cm, y_cm,debug=0):
    vector = np.arange(360)
    vector.resize(1,360)
    maxi = np.amax(rho)
    indice = np.argmax(rho)
    u,v=cv2.polarToCart(maxi,indice*math.pi/180)
    u=float(u[0])
    v=float(v[0])
    #Angulo dominante espejo
    mRHO = rho.copy()
    mRHO = mirror(indice, mRHO)
    maxi2 = np.max(mRHO)
    indice2 = np.argmax(mRHO)
    [u2,v2]=cv2.polarToCart(maxi2,indice2*math.pi/180)
    u2=float(u2[0])
    v2=float(v2[0])
    vec_max = np.array([u,v],dtype='float')
    vec_mirror = np.array([u2,v2],dtype='float')
    vec_centermass = np.array([x_cm,-y_cm],dtype='float')
    if not maxi2>=maxi*.7:
        angulodominante = indice
        return angulodominante
    # Proyecciones
    projection_max = np.dot(vec_centermass,vec_max)/((np.linalg.norm(vec_max) + 2.2250738585072014e-308));
    projection_mirror = np.dot(vec_centermass,vec_mirror)/((np.linalg.norm(vec_mirror) + 2.2250738585072014e-308));
    projection_max_v = normalize(vec_max.reshape(1,-1), axis=1).ravel() * projection_max
    projection_mirror_v = normalize(vec_mirror.reshape(1,-1), axis=1).ravel() * projection_mirror
    if (projection_max >= projection_mirror):
        angulodominante = indice #180*indice/(np.pi);
    else:
        angulodominante = indice2 #180*indice2/(np.pi);
    if debug:
        vec_max = normalize(vec_max.reshape(1,-1), axis=1).ravel()
        vec_mirror = normalize(vec_mirror.reshape(1,-1), axis=1).ravel()
        angulos =np.linspace(0,359,360) 
        angulos = (angulos/360) * (2 * np.pi)
        polar_graph(angulos,rho.T)
        polar_graph(angulos,mRHO.T)
        plt.plot(mRHO.T)
        plt.show()
        print(projection_max,projection_mirror)
        print(np.linalg.norm(projection_max_v) , np.linalg.norm(projection_mirror_v))
        print(indice,indice2)
        print(angulodominante)
        plt.grid(True)
        plt.xscale('linear')
        plt.yscale("linear")
        plt.yticks(np.linspace(-1000,2500,8))
        plt.xticks( np.linspace(-500,1500,5))
        plt.plot(0,0,"co")
        plt.plot(vec_max[0],vec_max[1],"bo")
        plt.plot(projection_max_v[0],projection_max_v[1],"b+")
        plt.plot([0,vec_max[0]],[0,vec_max[1]],"b")
        plt.plot([0,projection_max_v[0]],[0,projection_max_v[1]],"b")
        plt.plot(vec_mirror[0],vec_mirror[1],"ro")
        plt.plot(projection_mirror_v[0],projection_mirror_v[1],"rx")
        plt.plot([0,vec_mirror[0]],[0,vec_mirror[1]],"r")
        plt.plot([0,projection_mirror_v[0]],[0,projection_mirror_v[1]],"r")
        plt.plot(vec_centermass[0],vec_centermass[1],"go")
        plt.plot(vec_centermass[0],vec_centermass[1],"g")
        plt.axis('equal')
        plt.show()
    return angulodominante

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

def comp_densidad(im, ang_dom, kernel_size,debug=0):
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
    filas, columnas = im.shape
    mask=disk(np.round(filas/2))
    mask = cv2.resize(mask, (im.shape))
    mask_1 = mask.copy()
    mask = np.pad(mask,(kernel_size,kernel_size),'constant', constant_values=(0,0))
    mask_1 = np.pad(mask_1,(kernel_size,kernel_size),'constant', constant_values=(0,0))
    im = np.pad(im,(kernel_size,kernel_size),'constant', constant_values=(0,0))
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
    im_mask_1 = im*r_mask_1
    im_mask_2 = im*r_mask_2
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
        plt.plot(xx,yy)
        plt.imshow(im_mask_1,cmap="gray")
        plt.show()
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
        return True 
    else:
        return False

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
    resta=360-angulodominante
    angulodominante=resta+angulodominante##israel agrego
    (h, w) = imagen.shape[:2]
    center = (w / 2, h / 2)
    M = cv2.getRotationMatrix2D(center, angulodominante, 1.0)
    rotated = cv2.warpAffine(imagen, M, (w, h))
    rotated = rotated * h_mask
    return rotated, angulodominante