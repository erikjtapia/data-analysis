#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: eriktapia
"""

import pandas as pd
import pathlib
import platform 
import os
import sys

def limpiar():
    sistema_operativo = platform.system()
    if sistema_operativo == 'Windows':
        limpiar = 'cls'
    else:
        limpiar = 'clear'
    return limpiar

def generar_coordenadas(rutaCoord, limpiar):
    try:
        df_coord = pd.read_csv(rutaCoord, sep='\t')
        lat = df_coord['lat'].tolist()
        lon = df_coord['lon'].tolist()
        if isinstance(lat, list) and isinstance(lon, list):
            os.system(limpiar)
            input('Las coordenadas se cargaron con éxito.\nPresiona ENTER para continuar con la ejecución del programa...')
            os.system(limpiar)
    except:
        os.system(limpiar)
        print('Hubo un error al tratar de cargar las coordenadas.')
        print('- Recuerda que la malla de la subregión abarca las latitudes [14,33] y las longitudes [-120,-85], en una resolución de 0.5° por lo que solo se aceptan coordenadas que sean múltiplos de esta.')
        print('- Las coordenadas deben colocarse en un archivo input.txt el cual tendrá en la primera columna, con encabezado “lat”, los valores de latitud y en la segunda, con encabezado “lon”, los de longitud, separados entre sí por tabulaciones.')
        print(f'- Revisa que la ruta del archivo sea correcta, actualmente esta es: {rutaCoord}')
        input('\nPresiona ENTER para terminar la ejecución del programa...')
        sys.exit()
    return lat, lon


def generar_subRutas(rutaE, fase):
    rutaGeneral = pathlib.Path(f'{rutaE}')
    subRutas = list(rutaGeneral.glob(f'*{fase}*'))
    subRutas.sort()
    return subRutas

def year(archivoIt, rutaE, fase):
    year = str(archivoIt).replace(rutaE, "")
    year = year.replace(f"/{fase}_", "")
    year = year.replace("_Otono.txt", "")
    return year

def generarSerie(subRutas, lat, lon, fase, rutaE):
    print(f'Generando serie temporal para la coordenada ({lat},{lon}), fase {fase}')
    PwaveMed, PwaveMin, PwaveMax = [], [], []
    PwindMed, PwindMin, PwindMax = [], [], []
    Año = []
    for archivoIt in subRutas:
        datos = pd.read_csv(archivoIt, sep= '\t' , usecols= ['lat','lon','PwaveMed','PwaveMin','PwaveMax','PwindMed','PwindMin','PwindMax']) #lee la información del archivo, solo las columnas indicadas
        datos = datos[(datos['lat'] == lat) & (datos['lon'] == lon)]
        PwaveMed.append(datos['PwaveMed'].values[0])
        PwaveMin.append(datos['PwaveMin'].values[0])
        PwaveMax.append(datos['PwaveMax'].values[0])
        PwindMed.append(datos['PwindMed'].values[0])
        PwindMin.append(datos['PwindMin'].values[0])
        PwindMax.append(datos['PwindMax'].values[0])
        Año.append(year(archivoIt, rutaE, fase))
    serie = {'Año':Año,'PwaveMed':PwaveMed,'PwaveMin':PwaveMin,'PwaveMax':PwaveMax,'PwindMed':PwindMed,'PwindMin':PwindMin,'PwindMax':PwindMax}
    serie = pd.DataFrame(serie)
    return serie
