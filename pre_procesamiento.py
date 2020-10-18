# -*- coding: utf-8 -*-
"""
Módulo que contiene las funciones que se utlizan para elpre-procesamiento
de la mano.

@author: Jamid Israel Saenz Giron
"""
#Bibliotecas necesarias
import numpy as np
import matplotlib.pyplot as plt
import cv2
from scipy.spatial import distance
import imutils
import math

def cambio_tam(imagen):
   """Toma la imagen y pasa su lado menor a 256 y el otro a un valor proporcional
   Entradas:
       imagen --> imagen a evaluar
   Salidas:
       m --> Imagen ya con el valor de 256 y valor proporcional
   """
   filas,columnas=imagen.shape#Se opbtienen las dimensiones de la imagen
   if filas<columnas:#Si las columnas son mayores que las filas
      m=imutils.resize(imagen, height=256)#filas son 256 y las columnas a un valor proporcional
   elif columnas==filas:#Caso especial donde la imagen es cuadrada
         m=imutils.resize(imagen, width=256,height=256)#Las dimensiones se pasan a 256x256
   else: #Si las filas son mayores que las columnas
      m=imutils.resize(imagen, width=256)#columna son 256 y filas a un valor proporcional
   return m#Se regresa la imagen con las dimensiones mencionadas

def mascara_circular(filas, columnas, centro=None, radio=None):
    """Función para aplicar una máscara circular sobre una imagen.
    
    Ésta función aplica una máscara circular sobre una imagen, donde lo que esta dentro del círculo
    es de valor 1 y lo demás es de valor 0. Para esto se deben ingresar las filas, columnas de la imagen,
    el centro del circulo y el radio al que se quiere.
    
    Entradas:
        filas --> Valor de las filas de la imagen
        columnas --> Valor de las columnas de la imagen
        centro --> Centro del círculo (Si no se escribe el centro, se toma el centro de la imagen)
        radio --> Radio del circulo (Si no se especifica el radio se toma el tamaño de la imagen)
    Salidas:
        mascara --> Máscara sobre la imagen
    """
    
    if centro is None:#Se toma la mitad de la imagen
        centro = [int(columnas/2), int(filas/2)]#El centro se toma de acuerdo a los valores dados
    if radio is None: #Se usa la distancia a las filas y columnas para el radio, si no se especifica
        radio = min(centro[0], centro[1], columnas-centro[0], filas-centro[1])#Se toma el radio que se especifica
    Y, X = np.ogrid[:filas, :columnas] #Crea una matriz del tamaño especificado
    dist_from_center = np.sqrt((X - centro[0])**2 + (Y-centro[1])**2)#Se calcula la distancia al centro
    #Se convierte a binaria la imagen
    mask = dist_from_center <= radio#Toma los valores que estan dentro del radio
    mascara = np.zeros((filas,columnas))#Crea una matriz del tamaño de las filas y columnas
    mascara[mask==False] = 0#Si los valores en la variable mask son False, se asigna a todos ellos el valor de 0
    mascara[mask==True] = 1#Si los valores en la variable mask son True, se asigna a todos ellos el valor de 1
    return mascara.astype('uint8')#Se regresa la variable mascara con valores uin8

def centroide(imagen,grafica):
      """Localiza el centroide de una imagen y devuelve las coordenadas.
      Entradas:
      imagen --> Imagen a evaluar
      grafica --> si se elige grafica=1, se grafica el centroide con los bordes de canny
                  si grafica=2 se grafica el centroide con la imagen de entrada
      Salidas:
      cx --> coordenada x del baricentro
      cy --> coordenada y del baricentro
      """
      M2 = cv2.moments(imagen) #Función de opencv para obtener propiedas de la imagen
      if M2["m00"] != 0: #Condición para obtener el baricentro si es diferente de 0
           cx = int(M2['m10']/M2['m00']) #Fórmula para obtner la coordenada x
           cy = int(M2['m01']/M2['m00']) #Fórmula para obtner la coordenada y
      else: #Si m00 == 0 las dos coordenadas son 0
           cx, cy = 0, 0
      if grafica == 1: #Condición para graficar el centroide con bordes
         plt.plot(cx,cy,'ro')
         plt.imshow(imagen,cmap="gray")
         plt.show()
      elif grafica == 2: #Condición para graficar el centroide con la imagen de entrada
         plt.plot(cx,cy,'ro')
         plt.imshow(imagen,cmap="gray")
         plt.show()
      return cx,cy#Se regresa el baricentro
  
def parche(imagen, cy, cx, lado):
    """Se extraera un cuadrado de ladoxlado de la imagen, centrado en cx,cy.
    
    Función para obtener un segmento de una imagen de acuerdo al centro que se
    determine y de las dimensiones que se requieran.
    
    Entradas:
        imagen --> Imagen a obtener el parche
        cx --> Coordenada x del baricentro de la imagen
        cy --> Coordenada y del baricentro de la imagen
        lado --> Valor para el cuadrado extraido
    Salidas:
        parche --> Segmento de la imagen original
    """
    parche = imagen[cx - lado // 2 : cx + lado // 2, cy - lado // 2 : cy + lado // 2]#Obtención del parche
    return parche#Se regresa el segmento de la imagen

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

def baricentro_correccion_contraste(imagen):
   """Función para obtener el baricentro dentro de la mano.
   Entradas:
   imagen --> Imagen a evaluar
   Salidas:
   cx --> coordenada x de la imagen
   cy --> coordenada y de la imagen
   edges --> bordes de la imagen de la mano
   """
   radio_inicial =100 #Se inicia el radio con 100 pixeles
   filas,columnas=imagen.shape #Obtiene el valor de las dimensiones de la imagen
   edges = cv2.Canny(imagen,5,20) #Primera obtención de los bordes con valores umbrales mínimo de 5 y máximo de 20 
   cx,cy = centroide(edges,0)#Se localiza por primera vez el centroide
   parche_=parche(imagen,cx,cy,60)#Se toma una ventana de tamaño 60x60 pixeles a partir del baricentro
   correcion_cont = correccion_contraste_pormuestra(imagen,parche_,1.5,0)#Corrección de contraste con 1.5sigma
   edges = cv2.Canny(correcion_cont,70,100) #Segunda obtención de los bordes con valores umbrales mínimo de 70 y máximo de 100 
   cx,cy = centroide(edges,0) #Segunda localización del centroide
   centroide_anterior = np.array([cx,cy])#Variable para ir guardando el centroide previo
   condicion=True#Condición 
   cond2 = True #Condición
   
   #Inicio ciclo while
   while condicion == True or cond2 == True:#Se tienen dos condiocnes para el ciclo while
      mascara = mascara_circular(filas,columnas,centro=[cx,cy],radio=radio_inicial) #Se aplica la función de mascara_circular
      zona = (mascara*edges) #multiplica la mascara y la imagen para obtener la zona de interes
      cx,cy = centroide(zona,0) #Obtención del centroide
      centroide_actual=np.array([cx,cy])#Se guarda el centroide calculado
      distancia =  distance.euclidean(centroide_anterior, centroide_actual)#Calculo de la distancia euclideana del centroide anterior con el actual
      centroide_anterior = centroide_actual#Se asigna el centroide actual como anterior para continuar la búsqueda
      radio_inicial = radio_inicial - 10 #Va disminuyendo de 10 en 10 el radio
      #Condiciones para continuar o salir del bucle
      if distancia > 1:#Si la distancia del centroide aanterior y actual es mayor que 1
         cond2=False #cond2 es falso
      if distancia <= 1:#Si la distancia es menor o igual que 1
         condicion=False#condicion es falso
      else:#De otro modo
         condicion = True#Se continua en el bucle
      if radio_inicial<=30:#Si el radio inicial es menor o igual a 30
         condicion=False#condicion es falso
         cond2=False#cond2 es falso y se sale del bucle
   return cx,cy,edges#la función regresa las coordenadas del baricentro y los bordes de la imagen

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

def circulo_mano(imagen):
   """Función que obtiene el baricentro, el radio de la mano y el circulo que contiene a la mano.
   Entradas:
       imagen-->Imagen a evaluar
   Salidas:
       circulo_mano-->circulo que contiene a la mano
       radio_mano-->radio en pixeles del circulo de la mano
       cx-->Coordenada x del baricentro
       cy-->Coordenada y del baricentro
   """
   cx,cy,edges = baricentro_correccion_contraste(imagen)#Función para obtener el baricentro y los bordes de la mano
   circulo_mano, radio_mano = circunferencia_densidad(imagen,edges,cx,cy,0)#Función que obtiene el circulo con la mano y el radio de éste
   return circulo_mano, radio_mano,cx,cy#Variables de regreso

def cuadrado_mano_centrado(imagen_original):
    """Función que regresa la mano en tamaño de 256x256 en su respectivo circulo contenido.
    
    Se ingresa la imagen radiográfica con sus dimensiones originales, no importa cuales sean.
    Después se calcula el centroide y se obtiene una circunferencia donde se encuentra la mano,
    a partir de esta circunferencia se corta solamente dicha zona.
    Finalmente se regresa la mano con su circunferencia, en las dimensiones 256x256.
    
    Entradas:
        imagen_original-->Imagen a evaluar
    Salidas:
        imagen_final-->Imagen de la mano con dimensiones de 256x256
        cxc-->Valor del centroide en el eje x
        cyc-->Valor del centroide en el eje y
    """

    filas_o,columnas_o=imagen_original.shape#Se toman las dimensiones de la imagen original
    imagen = cambio_tam(imagen_original)#Toma el valor menor de las dimensiones y lo pasa a 256 y su lado mayor a un calor proporcional
    filas,columnas=imagen.shape#Obtiene las dimensiones de la imagen reducida
    cir_mano, radio_mano,cx,cy=circulo_mano(imagen)#Obtiene la mano en conjunto con su circulo contenida, el baricentro y el radio del círculo
    proporcion=round((columnas_o/columnas),1)#A partir de las filas y columnas de la imagen reducida, se obtiene un valor de proporción
    cx_p=cx*proporcion#Se obtiene el valor en x del centroide en la imagen original
    cy_p=cy*proporcion#Se obtiene el valor en y del centroide en la imagen original
    radio_p=round(radio_mano*proporcion)#Se obtiene el radio en la imagen original
    mascara=mascara_circular(filas_o,columnas_o,centro=[cx_p,cy_p],radio=radio_p)#Se obtiene la máscara circular en la imagen original
    zona=mascara*imagen_original#Se aplica la máscara circular en la imagen original
    cx_p=int(round(cx_p))#Se redondea el valor del centroide en el punto x
    cy_p=int(round(cy_p))#Se redondea el valor del centroide en el punto y
    radio_p=int(radio_p)#Se redondea el valor del radio
    dimy1=cy_p-radio_p#Valor mínimo en el eje y para realizar el recorte del circulo
    dimy2=cy_p+radio_p#Valor máximo en el eje y para realizar el recorte del circulo
    dimx1=cx_p-radio_p#Valor mínimo en el eje x para realizar el recorte del circulo
    dimx2=cx_p+radio_p#Valor máximo en el eje x para realizar el recorte del circulo
    if dimx1 <0:#En caso de que el valor sea un valor negativo en el eje x
       dimx1=0#Se obtiene el valor inicial de la imagen
    if dimy1<0:#En caso de que el valor sea un valor negativo en el eje y
       dimy1=0#Se obtiene el valor inicial de la imagen
    if dimx2 > columnas_o:#Si el valor es mayor al de las columnas
       dimx2=columnas_o#Se deja el valor de las columnas
    if dimy2 > filas_o:#Si el valor es mayor al de las filas
       dimy2=filas_o#Se deja el valor de las filas
    recorte=zona[dimy1:dimy2,dimx1:dimx2]#Recorte de la mano en conjunto con el circulo
    if recorte.shape[0]==recorte.shape[1]:#Si los recortes son cuadrados
       imagen_final=cv2.resize(recorte,dsize=(256, 256))#Se cambian las dimensiones del recorte a 256x256
       cxc=imagen_final.shape[0]//2#Se calcula el centroide del recorte en el eje x
       cyc=imagen_final.shape[0]//2#Se calcula el centroide del recorte en el eje y
    else:#En caso de que los recortes sean rectangulares
       if (cx_p-radio_p>0):#Si la resta entre el radio y el valor en x del centroide es mayor que 0
          diferencia1=cx_p-radio_p#Se guarda el valor de la resta en la variable diferencia1
       else:
          diferencia1=0#De otra manero se asigna a la variable el valor de 0
       cx_nuevo = cx_p-diferencia1#Nuevo valor para el valor del centroide en el eje x
       cy_nuevo=cy_p-dimy1#Nuevo valor para el centroide en el eje y
       final=np.zeros((radio_p*2,radio_p*2))#Se realiza una matriz del tamaño del radio
       aux1=radio_p-cx_nuevo#Variable en el eje x para recortar el rectangulo
       aux2=radio_p-cy_nuevo#Variable en el eje y para recortar el rectangulo
       final[aux2:aux2+recorte.shape[0] , aux1:aux1+recorte.shape[1]]=recorte#Se toma de la matriz final, una matriz del tamaño de recorte
       imagen_final=cv2.resize(final,dsize=(256, 256))#Se cambian las dimensiones de la matriz a 256x256
       cxc=imagen_final.shape[0]//2#Se calcula el centroide del recorte en el eje x
       cyc=imagen_final.shape[0]//2#Se calcula el centroide del recorte en el eje y
       
    return imagen_final,cxc,cyc#Se regresa la imagen de la mano de tamaño de 256x256 y su respectivo centroide

def contraste_imagen(imagen_orig):
    imagen_cuadrada, cxc, cyc = cuadrado_mano_centrado(imagen_orig)
    lado = 70#tamaño de la ventana
    cx = imagen_cuadrada.shape[0] // 2#Se obtiene la coordenada x
    cy = imagen_cuadrada.shape[0] // 2#Se obtiene la coordenada y
    parche_c = imagen_cuadrada[cx - lado // 2 : cx + lado // 2, cy - lado // 2 : cy + lado // 2]#Ventana
    correccion_cont = correccion_contraste_pormuestra(imagen_cuadrada, parche_c, 2.5, 0)#correcion de contraste final
    return correccion_cont