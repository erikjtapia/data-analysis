"""
@author: eriktapia

Este código genera mapas de calor segun los resultados de variación de los estadísticos
analizados para cada evento, potencia y estadístico.
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

rutaE = 'DatoRemovidoPorPrivacidad'
rutaS = 'DatoRemovidoPorPrivacidad'

datosNeutro = pd.read_csv(f'{rutaE}/data-variation_event-1.txt', sep='\t')
datosNina = pd.read_csv(f'{rutaE}/data-variation_event-2.txt', sep='\t')
datosNino = pd.read_csv(f'{rutaE}/data-variation_event-3.txt', sep='\t')

for var, fase in zip([datosNino,datosNina,datosNeutro],['Niño','Niña','Neutra']):
    figFase, ejes = plt.subplots(3, 2, figsize=(12, 13))
    (PwindMin,PwaveMin),(PwindMed,PwaveMed),(PwindMax,PwaveMax) = ejes
    plt.subplots_adjust(wspace=0, hspace=-0.5)
    
    s_PwaveMed = pd.pivot_table(var, values='s_PwaveMed', index='lat', columns='lon')
    s_PwaveMin = pd.pivot_table(var, values='s_PwaveMin', index='lat', columns='lon')
    s_PwaveMax = pd.pivot_table(var, values='s_PwaveMax', index='lat', columns='lon')
    s_PwindMed = pd.pivot_table(var, values='s_PwindMed', index='lat', columns='lon')
    s_PwindMin = pd.pivot_table(var, values='s_PwindMin', index='lat', columns='lon')
    s_PwindMax = pd.pivot_table(var, values='s_PwindMax', index='lat', columns='lon')
    
    grafs = [PwindMin, PwindMed, PwindMax, PwaveMin, PwaveMed, PwaveMax]
    matrices = [s_PwindMin, s_PwindMed, s_PwindMax, s_PwaveMin, s_PwaveMed, s_PwaveMax]
    subtitulos = ['a)', 'b)', 'c)', 'd)', 'e)', 'f)']
    
    for graf, matriz, subtitulo in zip(grafs, matrices, subtitulos):
        if subtitulo == subtitulos[0] or subtitulo == subtitulos[1] or subtitulo == subtitulos[2]:
            cbar_kws={'label': r'W/m$^2$/año', 'shrink': 0.4}
        if subtitulo == subtitulos[3] or subtitulo == subtitulos[4] or subtitulo == subtitulos[5]:
            cbar_kws={'label': 'W/m/año', 'shrink': 0.4}
        heatmap = sns.heatmap(matriz, cmap='coolwarm', center=0 ,ax=graf, cbar_kws=cbar_kws)
        graf.invert_yaxis()
        graf.set_aspect('equal', adjustable='box')
        graf.set_title(subtitulo, fontsize=14, fontweight='bold', loc='left', x=-0.08, y=0.9)
        graf.set_xlabel('Lon [°]', fontsize=10, fontweight='bold')
        graf.set_ylabel('Lat [°]', fontsize=10, fontweight='bold')
        
        cbar = heatmap.collections[0].colorbar
        cbar.set_label(cbar.ax.get_ylabel(), fontsize=7, fontweight='bold')
        cbar.ax.yaxis.set_label_position('left')
        cbar.ax.yaxis.label.set_rotation(0)
        cbar.ax.yaxis.set_label_coords(0.5, 1.02)
        cbar.ax.tick_params(labelsize=6)
        
        
        graf.tick_params(axis='x', labelsize=8)
        graf.tick_params(axis='y', labelsize=8)
        
        graf.set_xticks(graf.get_xticks()[::4])
        graf.set_yticks(graf.get_yticks()[::4])
        
        graf.set_xticklabels(graf.get_xticklabels(), rotation=0)
        
        if subtitulo == subtitulos[3] or subtitulo == subtitulos[4] or subtitulo == subtitulos[5]:
            graf.set_ylabel('')
            graf.set_yticklabels([])
         
        if subtitulo == subtitulos[0] or subtitulo == subtitulos[1] or subtitulo == subtitulos[3] or subtitulo == subtitulos[4]:
            graf.set_xlabel('')
            graf.set_xticklabels([])
        
    figFase.suptitle(f'Variación de las potencias en la fase {fase}', fontsize=18, fontweight='bold')  
    plt.savefig(f'{rutaS}/variation-graph_event-{fase}.pdf')
    plt.close()
