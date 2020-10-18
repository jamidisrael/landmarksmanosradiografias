# -*- coding: utf-8 -*-
import csv

def carga_csv(archivo_csv):
    # manual_sx = []#Lista vacia para guardar la landmark superior manual en el eje x
    # automa_sx = []#Lista vacia para guardar la landmark superior automática en el eje x
    # manual_ix = []#Lista vacia para guardar la landmark inferior manual en el eje x
    # automa_ix = []#Lista vacia para guardar la landmark inferior automática en el eje x
    # manual_sy = []#Lista vacia para guardar la landmark superior manual en el eje y
    # automa_sy = []#Lista vacia para guardar la landmark superior automática en el eje y
    # manual_iy = []#Lista vacia para guardar la landmark inferior manual en el eje y
    # automa_iy = []#Lista vacia para guardar la landmark inferior automática en el eje y
    
    ###############################Lectura de los archivos csv################################
    # archivo_manual = 'Manual_landmarks.csv'#Se leé el csv con las landmarks manual
    with open(archivo_csv) as f:#Se guarda en el objeto f
        reader=csv.reader(f)#Se pasa la información a la variable reader
        header_row=next(reader)#Se va leyendo las filas del archivo
        # print('header_row')
        # print(header_row)
        lista_manual=[]#Se crea una lista donde se irá guardando los datos leídos
        for row in reader:#Ciclo para guardar los datos
            lista_manual.append(row)#Se va agregando los datos a las listas
    # dicc1.update({header_row:lista_manual})
    dicc1={}
    for nombre in header_row:
        # print(nombre)
        for inf in lista_manual:
            for nom in inf:
                # print(nom)
                dicc1.update({nombre:nom})
    # print(lista_manual)
    # print('carga csv')
    # print('diccionario')
    # print(dicc1)
    return dicc1#lista_manual