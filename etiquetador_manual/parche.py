#!/usr/bin/env python3
# -*- coding: utf-8 -*-


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