# -*- coding: utf-8 -*-
"""
Created on Mon Sep 28 21:27:51 2020

@author: israe
"""

def landmarks_csv(ruta, puntos):
    """Función que crea un archivo csv con las coordenadas de las imágenes evaluadas.
    
    Parámetros de entrada de la función:
    
    ruta               : Ruta donde se desea guardar el archivo
    puntos             : coordenadas de las imagánes evaluadas. Éste debe de venir en un diccionario.
                         Por ejemplo {123.png:[10,20,30,40],789.png:[50,60,70,80]}
    
    Parámetros de salida de la función:
    
    test_landmarks.csv : Archivo csv con el nombre y las coordenadas de las imágenes evaluadas
    """
    archivo = ruta + '/' + 'Landmarks.csv'#Nombre del archivo
    csv = open(archivo,'w')#Se crea el archivo y se especifica que se va a escribir('w')
    titulor = 'nombre,xs,ys,xi,yi\n'#Nombres de cada fila
    csv.write(titulor)#Se escribe los nombres en el archivo
    for nombres,valores in puntos.items():#Se crea un cilo for para escribir los puntos de las imágenes leídas
        nombre=nombres#Se escribe el noombre de la imagen
        xs=valores[0]#Se escribe la landmark superior en x
        ys=valores[1]#Se escribe la landmark superior en y
        xi=valores[2]#Se escribe la landmark inferior en x
        yi=valores[3]#Se escribe la landmark inferior en y
        filas=nombre+','+str(xs)+','+str(ys)+','+str(xi)+','+str(yi)+'\n'#Se separan los valores de acuerdo al orden dado
        csv.write(filas)#Se escribe los puntos en el archivo
    csv.close()#Se finaliza la escritura del archivo