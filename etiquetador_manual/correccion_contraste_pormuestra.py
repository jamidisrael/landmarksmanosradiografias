# -*- coding: utf-8 -*-

def correccion_contraste_pormuestra(imagen,imagen_muestra,sigma=1.5,grafica = 1):
        """Función para corregir el contraste a partir de un segmento de la imagen
        Esta funcion ayuda a extraer los valores de la dispercion de los valores de gris 
        de un cuadro de la imagen, que estara centrado en (cx, cy), de tamaño lado x lado 
        y en funcion de la desviacion estandar de los valores de este cuadro se ajustaran 
        los niveles de gris de toda la imagen.
        Entradas:
        imagen --> Imagen a evaluar
        imagen_muestra --> segmento de una imagen con los valores de gris a ajustar
        sigma --> valor para ajustar la correción de contraste
        grafica --> Si se asigna 1 se muestra la imagen_muestra en consola
        Salidas
        NF --> Imagen resultante con contraste corregido
        """
        import numpy as np
        import matplotlib.pyplot as plt
        
        f2=imagen_muestra#Segmento de la imagen
        if grafica == 1:#En caso de que se muestre la gráfica
           plt.title('Parche')#Título de la imagen
           plt.imshow(f2,cmap='gray')#Se muestra la imagen
           plt.show()
        # convertir cada imagen en vector
        x, y = f2.shape#Se obtienen las dimensiones de la imagen
        f2=f2.reshape(x*y,1)#Se pasa a vector la imagen
        fm=np.mean(f2)#Promedio de las imágenes:
        DesvStd=np.std(f2, axis=0)#Desviación estándar del vector
        #Nuevos valores: mínimo y máximo:
        minA=fm-(DesvStd*sigma)#Valor mínimo
        maxA=fm+(DesvStd*sigma)#Valor máximo
        #(fórmula de la pendiente):
        NF=255*(imagen-minA)/((maxA-minA)+2.2250738585072014e-308)
        NF = np.clip(NF,0,255)#Si los valores son cercanos a 0, se asigna a ese valor, si son cercanos a 255 se asignan a ese valor
        #Esto es para evitar la saturación en la imagen
        return NF.astype(np.uint8)#Se regresa la imagen en enteros de 8 bits sin signo