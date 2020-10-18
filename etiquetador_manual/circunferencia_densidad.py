# -*- coding: utf-8 -*-
#Bibliotecas y funciones utilizadas
import numpy as np
from mascara_circular import mascara_circular
import math
import matplotlib.pyplot as plt

def circunferencia_densidad(imagen,bordes, cx, cy,grafica):
   """Obtiene una circunferencia del tamaño de la mano.
   Entradas:
   imagen --> Imagen original
   bordes --> Imagen con bordes
   cx --> Coordenada x del baricentro de la imagen
   cy --> Coordenada y del baricentro de la imagen
   grafica --> Si se asigna 1 se muestra la imagen_muestra en consola
   Salidas:
   zona_final --> Circunferencia con la mano contenida
   radio_final --> Radio de la circunferencia final
   """

   vector_suma_circulo = np.zeros((1,18)) #vector para almacenar la suma de los bordes de cada circulo
   vector_resta_circulos = np.zeros((1,17)) #vector para almacenar la resta del circulo contenido
   vector_areas=np.zeros((1,18)) #vector que almacena las áreas de los círculos
   vector_areas_resta = np.zeros((1,17)) #vector para almacenar la resta de los círculos
   vector_densidades = np.zeros((1,17)) #vector para las densidades
   vector_Densidades = np.zeros((1,18))#vector para las densidades con el primer circulo
   cradio=1.32#Constante para multiplicar el radio del circulo
   radios = np.array([30,cradio*30,(cradio**2)*30,(cradio**3)*30,(cradio**4)*30,(cradio**5)*30,(cradio**6)*30,(cradio**7)*30,(cradio**8)*30,(cradio**9)*30,(cradio**10)*30,(cradio**11)*30,(cradio**12)*30,(cradio**13)*30,(cradio**14)*30,(cradio**15)*30,(cradio**16)*30,(cradio**17)*30])
   filas,columnas=imagen.shape #se almacena en las variables el numero de filas y columnas

   for b in range(0,18):
         mascara = mascara_circular(filas,columnas,centro=[cx,cy],radio=radios[b]) #Función para aplicar la mascara circular
         zona = (mascara*bordes) #Se aplica la máscara sobre la imagen de bordes
         binaria = np.zeros(zona.shape) #Crea una matriz del tamaño de la imagen
         imagennuevab = zona #se asigna a la variable la mascara circular y la imagen con los bordes
         binaria[imagennuevab==0] = 0 #Si el valor en la variable zona es igual a False se asigna 0
         binaria[imagennuevab==255] = 1 #Si el valor es 255 se asigna 1
         vector_suma_circulo[:,b] = binaria.sum() #Se cuantan los 1 dentro del circulo
         vector_areas[:,b] = math.pi*radios[b]**2 #Se calcula el área del circulo
   for i in range(0,17):
      vector_resta_circulos[:,i] = vector_suma_circulo[:,i+1]-vector_suma_circulo[:,i] #Se resta la suma del circulo continuo
      vector_areas_resta[:,i] = vector_areas[0,i+1]-vector_areas[0,i]#Se resta el area del circulo continuo
   primero = vector_suma_circulo[0,0]/vector_areas[0,0] #Se realiza la operacion de densidad para el primer circulo
   vector_densidades = np.divide(vector_resta_circulos,vector_areas_resta)#Se obtiene las densidaes de los circulos
   vector_Densidades = np.append(primero,vector_densidades) #Agrega la primera densidad al vector anterior
   densidad_ord=np.sort(vector_Densidades)#Se ordenan los valores de las densidades de menor a mayor
   densidad_maxima= np.max(vector_Densidades) #Localiza la densidad máxima
   seg_max=densidad_ord[-2]#Se obtiene el valor de la segunda densidad máxima
   prom_max=(densidad_maxima+seg_max)/2#Promedio de la primera y segunda densidades máximas
   vector_densidades_normalizado = (vector_Densidades/prom_max).T #Normaliza de acuerdo al promedio de las densidades máximas
   contador_indice= 0 #Contador para conocer el circulo evaluado
   for j in range(0,len(vector_densidades_normalizado)):
      evaluacion = vector_densidades_normalizado[j] #Se recorre el vector de densidades normalizado
      if evaluacion<0.2:#Umbral de 0.2 para obtener el circulo que contiene la mano
         contador_indice=contador_indice#Se guarda el circulo en la variable contador_indice
         break #Se sale de la condición
      else:
         contador_indice+=1 #Si no se cumple la condición se aumenta en 1 el contador_indice
   radio_final = radios[contador_indice] #De acuerdo al contador_indice se selecciona el radio final
   mascara_final = mascara_circular(filas,columnas,centro=[cx,cy],radio=radio_final) #Se aplica la máscara de acuerdo al radio final
   zona_final = (mascara_final*imagen) #Aplica la mascara a la imagen
######GRafica#######################
   if grafica == 1:#Si en grafica se tiene un 1 se muestra
      ejex= np.arange(0,18,1)#Vector de 19 unidades para el eje x
      ejey=vector_densidades_normalizado#Vector donde se muestra las densidades y se toma como eje y
      plt.plot(ejex,ejey,'ro')#Se muestra la gráfica y cada valor en un punto rojo
      plt.xlim(0, 18)#Límite del eje x
      plt.grid(True)#Se muestra las lineas del plano
      plt.show()
   return zona_final, radio_final#Variables que se regresan