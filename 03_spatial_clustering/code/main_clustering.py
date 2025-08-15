#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: eriktapia

1. Cálcula del coeficiente de silueta y/o índice de Davies–Bouldin para determinar el número óptimo de grupos.
2. Grafica uno o ambos coeficientes para el número de grupos propuesto (líneas 34 y 35).
3. Genera tres archivos, uno por evento, donde se indica a que grupo pertenece cada coordenada según su
   agrupación por estadísticos (min, med, max).
4. Se generan 9 archivos con los centroides de los grupos formados por evento y estadístico.

"""
import functions_clustering as fa
import pandas as pd
import importlib
importlib.reload(fa)

rutaE = 'DatoRemovidoPorPrivacidad'
rutaSG = 'DatoRemovidoPorPrivacidad'
rutaSD = 'DatoRemovidoPorPrivacidad'
rutaSC = 'DatoRemovidoPorPrivacidad'

estadisticos = ['Mínimos','Mediana','Máximos']
vars1 = ['s_PwaveMin','s_PwaveMed','s_PwaveMax']
vars2 = ['s_PwindMin','s_PwindMed','s_PwindMax']



for fase in ['Nino', 'Nina', 'Neutro']:
    clusters = pd.read_csv(f'{rutaE}/Variación_{fase}.txt', sep= '\t' , usecols= ['lat','lon'])
    for estadistico, var1, var2 in zip(estadisticos,vars1,vars2):
        datos = fa.generarDatos(rutaE,fase,var1,var2)
        k, grupos, siluetas, davies = fa.numeroGrupos(datos, var1, var2, fase, estadistico)
        #fa.SilouetteDavis(rutaSG, fase, estadistico, grupos[1:], siluetas[1:], davies)
        fa.Silouette(rutaSG, fase, estadistico, grupos[1:], siluetas[1:])
        datos, centroides = fa.generarResultados(rutaSD, rutaSC, fase, estadistico, k, datos, var1, var2)
        if estadistico == 'Mínimos':
            clusters['cMin'] = datos['cluster']
        elif estadistico == 'Mediana':
            clusters['cMed'] = datos['cluster']
        elif estadistico == 'Máximos':
            clusters['cMax'] = datos['cluster']
    
    with open(f'{rutaSD}/Grupos_{fase}.txt','w') as archivoGenerado:
        clusters.to_csv(archivoGenerado, sep = '\t', index=False)
