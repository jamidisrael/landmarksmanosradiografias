#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#Bibliotecas y funciones utilizadas
from tkinter import *
from PIL import Image, ImageTk
from tkinter.filedialog import askopenfilename
from tkinter.filedialog import askdirectory
import os
from os import walk
import scipy.io
import sys 
from landmarks_csv import landmarks_csv
from carga_csv import carga_csv
from cuadrado_mano_centrado import cuadrado_mano_centrado
from parche import parche
from correccion_contraste_pormuestra import correccion_contraste_pormuestra
import cv2
from shog import shog
import pathlib

"""
Programa para marcar los puntos manuales.

Se selecciona la carpeta donde se encuentren las radiografias de manos, despues se crea una carpeta llamada
"Correccion" la cual se almacena las imagenes corregidas en contraste y posición. Realizado dicho proceso
se abre una ventana con las imagenes para marcar las landmarks. Una vez finalizado los puntos manuales
se genera un archivo csv donde se muestra la siguiente información:
nombre   xs   ys   xi   yi
imagen1  123  144  189  195
  .
  .
  .
imagenN  125  140  190  199
"""
#Se trabaja con clases
class Window(Frame):
#Se inicia
    def __init__(self, master=None):
        Frame.__init__(self, master)
        global imgSize
        self.master = master
        self.pos = []
        self.master.title("GUI")
        self.pack(fill=BOTH, expand=1)
        self.counter = 0
        self.pointer = 0
        self.clickk()
        self.contador = 0
        self.Directory = askdirectory(title='Choose an image.')
        self.matFile = os.path.join(self.Directory,"Manual_landmarks.csv")
        #Aqui se carga el directorio, los archivos que hay en la carpeta
        for self.dirpath, self.dirnames, self.filenames in walk(self.Directory):
            print(self.filenames)
            break
        
        self.correccion=self.dirpath + '/Corregidas/'#Se agrega a la carpeta raiz la carpeta Corregidas donde
        pathlib.Path(self.correccion).mkdir(parents=True, exist_ok=True)#Se guardaran las imagenes corregidas en contraste
        
        #Solo se leen los archivos con el formato jpg y png
        for i in self.filenames:
              if not(i[-3:]=="png" or i[-3:]=='jpg'):
                 self.filenames.remove(i)
        for j in self.filenames:
            if j[-3:] == 'png' or j[-3:] == 'png':
                self.correccion_imagen()
                self.contador+=1
        #Se crea un diccionario donde se guardan los puntos
        if ( not os.path.exists(self.matFile)):
            self.dict1={}
        else:
            print("recuperar valores")
            # self.dict1=scipy.io.loadmat(self.matFile) ###### define el nombre del archivo .mat
            self.dict1=carga_csv(self.matFile)
            # print(self.dict1)
            while self.filenames[self.pointer] in self.dict1.keys():
                self.pointer +=1
                if self.pointer+1 >= len(self.filenames):
                    root.destroy()
                    sys.exit()

    def printcoords(self,event):
        print (self.pointer,len(self.filenames))        
        x = canvas.canvasx(event.x)
        y = canvas.canvasy(event.y)
        print("x=",x,"y=",y)
        self.pos.append(x)
        self.pos.append(y)
        print("pos:",self.pos)
        root.config(cursor="circle")
        self.counter += 1
        if self.pointer+1 >= len(self.filenames):
            if self.counter < 2: ##### este define el nummero de puntos en cada imagen
                canvas.create_line(x - 5, y, x + 5, y, fill="red", tags="crosshair")
                canvas.create_line(x, y - 5, x, y + 5, fill="red", tags="crosshair")
            else:
                self.dict1.update({self.filenames[self.pointer]:self.pos})
                self.pos=[]
                self.counter = 0
                print(self.dict1)
                landmarks_csv(self.matFile,self.dict1)
                # scipy.io.savemat(self.matFile,self.dict1) ###### define el nombre del archivo .mat
                root.destroy()
                sys.exit()
        else:
            if self.counter < 2: ##### este define el nummero de puntos en cada imagen
                canvas.create_line(x - 5, y, x + 5, y, fill="red", tags="crosshair")
                canvas.create_line(x, y - 5, x, y + 5, fill="red", tags="crosshair")
            else:
                print(self.pointer)
                self.dict1.update({self.filenames[self.pointer]:self.pos})
                self.pos=[]
                self.counter = 0
                print(self.dict1)
                landmarks_csv(self.matFile,self.dict1)#Guarda el archivo csv con los puntos
                self.pointer += 1
                self.update_image()
                
    #Función para el click de los puntos
    def clickk (self):
        canvas.bind("<ButtonPress-1>",self.printcoords)
    #función para aplicar el proceso de corrección en las imágenes
    def correccion_imagen(self):
        imagen=cv2.imread(os.path.join(self.dirpath,self.filenames[self.contador]),0)
        imagen_cuadrada,cxc,cyc=cuadrado_mano_centrado(imagen)
        parche_c=parche(imagen_cuadrada,imagen_cuadrada.shape[0]//2,imagen_cuadrada.shape[0]//2,70)
        correcion_cont = correccion_contraste_pormuestra(imagen_cuadrada,parche_c,2.5,0)
        ima, angulo = shog(correcion_cont,ventana=90)
        cv2.imwrite(self.correccion+self.filenames[self.contador],ima)

    #Función para cargar las imágenes y verlas en Tkinter
    def update_image(self):
         app.master.title(app.filenames[self.pointer])
         # im = Image.open(os.path.join(self.dirpath,self.filenames[self.pointer]))
         im = Image.open(os.path.join(self.correccion,self.filenames[self.pointer]))
         tkimage = ImageTk.PhotoImage(im)
         canvas.tkimage=tkimage    
         canvas.create_image(0,0,image=tkimage,anchor="nw")
         canvas.configure(scrollregion = canvas.bbox("all"))
         root.geometry('%dx%d' % (im.size[0],im.size[1]))

event2canvas = lambda e, c: (c.canvasx(e.x), c.canvasy(e.y))
root = Tk()#Se abre la ventana para buscar la carpeta
frame = Frame(root, bd=2, relief=SUNKEN)
frame.grid_rowconfigure(0, weight=1)
frame.grid_columnconfigure(0, weight=1)
xscroll = Scrollbar(frame, orient=HORIZONTAL)
xscroll.grid(row=1, column=0, sticky=E+W)
yscroll = Scrollbar(frame)
yscroll.grid(row=0, column=1, sticky=N+S)
canvas = Canvas(frame, bd=0, xscrollcommand=xscroll.set, yscrollcommand=yscroll.set)
canvas.grid(row=0, column=0, sticky=N+S+E+W)
xscroll.config(command=canvas.xview)
yscroll.config(command=canvas.yview)
frame.pack(fill=BOTH,expand=1)
#Se manda a llamar a las clases
app = Window(root)
app.master.title(app.filenames[0])
print(app.dirpath)
im = Image.open(os.path.join(app.correccion,app.filenames[0]))
tkimage = ImageTk.PhotoImage(im)
canvas.create_image(0,0,image=tkimage,anchor="nw")
canvas.config(scrollregion=canvas.bbox(ALL))
print(app.dirpath)
root.mainloop()