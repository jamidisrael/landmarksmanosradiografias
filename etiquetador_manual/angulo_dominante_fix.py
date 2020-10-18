#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 20 17:42:14 2019

@author: longinos
"""

import time
import numpy as np
import cv2
import math
import matplotlib.pyplot as plt
from skimage.morphology import binary_closing, disk
from mirror import mirror
from polar_graph import polar_graph
from sklearn.preprocessing import normalize


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
#    [u3,v3] = cv2.cartToPolar(vec_centermass[0],vec_centermass[1])
#    u3=float(u3[0])
#    v3=(float(v3[0])*180/math.pi)-90
#    
#    [u4,v4]=cv2.polarToCart(u3,v3*math.pi/180)
#        
#    u4=float(u4[0])
#    v4=float(v4[0])
#    
#    vec_centermass = np.array([u4,v4],dtype='float')
    ################################################################################
    # probe normalizando los vectores, ya que la diferencia de magnitudes era muy grande
#    vec_max = normalize(vec_max.reshape(1,-1), axis=1).ravel()
#    vec_mirror = normalize(vec_mirror.reshape(1,-1), axis=1).ravel()
#    vec_centermass = normalize(vec_centermass.reshape(1,-1), axis=1).ravel()
    
    #en este caso no se normaliza
#    vec_max = vec_max.reshape(1,-1).ravel()
#    vec_mirror = vec_mirror.reshape(1,-1).ravel()
#    vec_centermass = vec_centermass.reshape(1,-1).ravel()
    ################################################################################
    
    # Proyecciones
    projection_max = np.dot(vec_centermass,vec_max)/((np.linalg.norm(vec_max) + 2.2250738585072014e-308));
    projection_mirror = np.dot(vec_centermass,vec_mirror)/((np.linalg.norm(vec_mirror) + 2.2250738585072014e-308));
    
    projection_max_v = normalize(vec_max.reshape(1,-1), axis=1).ravel() * projection_max
    projection_mirror_v = normalize(vec_mirror.reshape(1,-1), axis=1).ravel() * projection_mirror
    
    #%%
    if (projection_max >= projection_mirror):
        angulodominante = indice #180*indice/(np.pi);
    else:
        angulodominante = indice2 #180*indice2/(np.pi);
        

#    if (np.linalg.norm(projection_max_v) > np.linalg.norm(projection_mirror_v)):
#        
#        angulodominante = indice
#    else:
#        angulodominante = indice2

#    angulodominante = indice

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
    