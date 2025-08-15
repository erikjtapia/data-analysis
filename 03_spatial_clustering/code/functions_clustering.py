#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: eriktapia

"""
import platform
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
from sklearn.metrics import silhouette_score, davies_bouldin_score

def limpiar():
    sistema_operativo = platform.system()
    if sistema_operativo == 'Windows':
        limpiar = 'cls'
    else:
        limpiar = 'clear'
    return limpiar

def generarDatos(rutaE,fase,var1,var2):
    datos = pd.read_csv(f'{rutaE}/Variación_{fase}.txt', sep= '\t' , usecols= ['lat','lon',var1,var2]) 
    return datos

def segundo_maximo_indice(lista):
    max_val = max(lista)
    max_index = lista.index(max_val)
    lista_copia = lista.copy()
    lista_copia[max_index] = float('-inf')
    segundo_max_val = max(lista_copia)
    segundo_max_index = lista.index(segundo_max_val)
    return segundo_max_index

def numeroGrupos(datos, var1, var2, fase, estadistico):
    grupos = []
    inercias = []
    siluetas = []
    davies = []
    
    normalizar = StandardScaler() 
    datos[['STDlat', 'STDlon', f'STD{var1}',f'STD{var2}']] = normalizar.fit_transform(datos[['lat','lon',var1,var2]]) 
    
    for i in range(10):
        kmeans = KMeans(n_clusters=i+1, init='k-means++', random_state=50) 
        kmeans.fit(datos[['STDlat', 'STDlon', f'STD{var1}',f'STD{var2}']]) 
        grupos.append(i+1) 
        inercias.append(kmeans.inertia_) 
        
        if i > 0: 
            silhouette = silhouette_score(datos[['STDlat', 'STDlon', f'STD{var1}', f'STD{var2}']], kmeans.labels_)
            daviesbouldin = davies_bouldin_score(datos[['STDlat', 'STDlon', f'STD{var1}', f'STD{var2}']], kmeans.labels_)
            siluetas.append(silhouette)
            davies.append(daviesbouldin)
        else:
            siluetas.append(float('0'))
            davies.append(float('0')) 
    
    k = grupos[siluetas.index(max(siluetas[1:]))]
    return k, grupos, siluetas, davies

def SilouetteDavis(rutaS, fase, estadistico, grupos, siluetas, davies):
    figFE, (sil,dav) = plt.subplots(2, 1, figsize=(10, 12))
    plt.subplots_adjust(wspace=0, hspace=-0.4)

    # Primer gráfico: Índices de Silhouette
    sil.plot(grupos, siluetas, marker='o')
    sil.set_title('Método de Silhouette')
    sil.set_xlabel('Número de grupos (k)')
    sil.set_ylabel('Coeficiente [1]')
    sil.set_xticks(grupos)
    sil.grid(True)

    # Segundo gráfico: Índices de Davies-Bouldin
    dav.plot(grupos, davies, marker='o')
    dav.set_title('Método de Davies-Bouldin')
    dav.set_xlabel('Número de grupos (k)')
    dav.set_ylabel('Coeficiente [1]')
    dav.set_xticks(grupos)
    dav.grid(True)

    plt.tight_layout()
    plt.savefig(f'{rutaS}/{fase}_{estadistico}_SilouetteDavis.pdf')
    plt.close()
    
def Silouette(rutaS, fase, estadistico, grupos, siluetas):
    
    if fase == 'Nino':
        texto = 'El Niño'
    elif fase == 'Nina':
        texto = 'La Niña'
    elif fase == 'Neutro':
        texto = 'Fase neutra'
        
    plt.plot (grupos, siluetas, 'o-')
    plt.xlabel('Número de grupos (k)')
    plt.ylabel('Coeficiente [1]')
    plt.grid (True)
    plt.title(f'{texto} - {estadistico}')
    plt.savefig(f'{rutaS}/{fase}_{estadistico}_Silouette.pdf')
    plt.close()

def generarResultados(rutaSD, rutaSC, fase, estadistico, k, datos, var1, var2):
    normalizar = StandardScaler() 
    datos[['STDlat', 'STDlon', f'STD{var1}',f'STD{var2}']] = normalizar.fit_transform(datos[['lat','lon',var1,var2]]) 
    
    kmeans = KMeans(n_clusters=k, init='k-means++', random_state=50) 
    kmeans.fit(datos[['STDlat', 'STDlon', f'STD{var1}',f'STD{var2}']]) 
    datos['cluster']=kmeans.labels_
    datos['cluster'] = datos['cluster'] + 1
    
    centroides = kmeans.cluster_centers_
    centroides = normalizar.inverse_transform(centroides)
    centroides = pd.DataFrame(centroides, columns=['lat', 'lon', var1, var2])
    centroides['cluster'] = centroides.index
    centroides['cluster'] = centroides['cluster'] + 1
    centroides = centroides.reindex(columns=['cluster','lat','lon',f'{var1}',f'{var2}'])
    
    with open(f'{rutaSD}/{fase}_Centros-{estadistico}.txt','w') as archivoGenerado:
        centroides.to_csv(archivoGenerado, sep = '\t', index=False)
    
    return datos, centroides
