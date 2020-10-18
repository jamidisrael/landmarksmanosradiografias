# -*- coding: utf-8 -*-

from baricentro_correccion_contraste import baricentro_correccion_contraste
from circunferencia_densidad import circunferencia_densidad

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