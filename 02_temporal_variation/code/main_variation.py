#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: eriktapia

Este código calcula la variación en la magnitud de los estadisticos de las potencias 
a lo largo de los periodos de análisis.

"""
import functions_variation as fv
import pandas as pd
import os
from scipy.stats import linregress
import importlib
importlib.reload(fv)

rutaE = 'DatoRemovidoPorPrivacidad'
rutaS = 'DatoRemovidoPorPrivacidad'
rutaCoord = 'DatoRemovidoPorPrivacidad'

limpiar = fv.limpiar()
lat, lon = fv.generar_coordenadas(rutaCoord, limpiar)

for fase in ['Nino', 'Nina', 'Neutro']:
    print(f'------------ FASE {fase} ------------')
    lat_aux = []
    lon_aux= []
    sPwaveMed_aux = []
    sPwaveMin_aux = []
    sPwaveMax_aux = []
    sPwindMed_aux = []
    sPwindMin_aux = []
    sPwindMax_aux = []
    subRutas = fv.generar_subRutas(rutaE, fase) 
    
    for i in range(len(lat)): 
        serie = fv.generarSerie(subRutas, lat[i], lon[i], fase, rutaE)
        serie['Año'] = pd.to_numeric(serie['Año'], errors='coerce')
        
        print(f'Generando ajuste lineal para la coordenada ({lat[i]},{lon[i]}), fase {fase}')
        s_PwaveMed, i_PwaveMed, r_PwaveMed, p_PwaveMed, std_PwaveMed = linregress(list(serie['Año']),list(serie['PwaveMed']))
        s_PwaveMin, i_PwaveMin, r_PwaveMin, p_PwaveMin, std_PwaveMin = linregress(list(serie['Año']),list(serie['PwaveMin']))
        s_PwaveMax, i_PwaveMax, r_PwaveMax, p_PwaveMax, std_PwaveMax = linregress(list(serie['Año']),list(serie['PwaveMax']))
        s_PwindMed, i_PwindMed, r_PwindMed, p_PwindMed, std_PwindMed = linregress(list(serie['Año']),list(serie['PwindMed']))
        s_PwindMin, i_PwindMin, r_PwindMin, p_PwindMin, std_PwindMin = linregress(list(serie['Año']),list(serie['PwindMin']))
        s_PwindMax, i_PwindMax, r_PwindMax, p_PwindMax, std_PwindMax = linregress(list(serie['Año']),list(serie['PwindMax']))
        
        lat_aux.append(lat[i])
        lon_aux.append(lon[i])
        sPwaveMed_aux.append(s_PwaveMed*1000)
        sPwaveMin_aux.append(s_PwaveMin*1000)
        sPwaveMax_aux.append(s_PwaveMax*1000)
        sPwindMed_aux.append(s_PwindMed*1000)
        sPwindMin_aux.append(s_PwindMin*1000)
        sPwindMax_aux.append(s_PwindMax*1000)
        
    variacion = {'lat':lat_aux,'lon':lon_aux,'s_PwaveMed':sPwaveMed_aux,'s_PwaveMin':sPwaveMin_aux,'s_PwaveMax':sPwaveMax_aux,'s_PwindMed':sPwindMed_aux,'s_PwindMin':sPwindMin_aux,'s_PwindMax':sPwindMax_aux}
    variacion = pd.DataFrame(variacion)
    
    for col in ['s_PwaveMed','s_PwaveMin','s_PwaveMax','s_PwindMed','s_PwindMin','s_PwindMax']:
        variacion[col] = variacion[col].round(4)
    
    with open(f'{rutaS}/data-variation-event-{fase}.txt','w') as archivoGenerado:
        variacion.to_csv(archivoGenerado, sep = '\t', index=False)
    print(f'Se generaron exitosamente los ajustes lineales para la fase {fase}.')
    os.system(limpiar)
