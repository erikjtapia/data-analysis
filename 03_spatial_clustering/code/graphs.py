#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: eriktapia
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns

rutaE = 'DatoRemovidoPorPrivacidad'
rutaS = 'DatoRemovidoPorPrivacidad'

datosNino = pd.read_csv(f'{rutaE}/groups_event-3.txt', sep='\t')
datosNina = pd.read_csv(f'{rutaE}/groups_event-2.txt', sep='\t')
datosNeutro = pd.read_csv(f'{rutaE}/groups_event-1.txt', sep='\t')

for datosfase, fase in zip([datosNino,datosNina,datosNeutro],['Niño','Niña','Neutro']):
    for var, estadistico, color, subt in zip(['cMin','cMed','cMax'],['Mínimos','Mediana','Máximos'],['Blues','Greys','Reds'],['a)','b)','c)']):
        matriz = pd.pivot_table(datosfase, values=var, index='lat', columns='lon')
        grupos = datosfase[var].unique()
        grupos.sort()
        
        cmap = plt.get_cmap(color)
        norm = plt.Normalize(vmin=0, vmax=max(grupos))

        fig, ax = plt.subplots(figsize=(6,4))
        sns.heatmap(matriz, cmap=cmap, norm=norm, ax=ax, cbar=False)

        ax.invert_yaxis()
        ax.set_aspect('equal', adjustable='box')
        ax.set_title(subt, fontsize=14, fontweight='bold', loc='left', x=-0.08, y=0.9)
        ax.set_xlabel('Lon [°]', fontsize=10, fontweight='bold')
        ax.set_ylabel('Lat [°]', fontsize=10, fontweight='bold')

        ax.tick_params(axis='x', labelsize=8) 
        ax.tick_params(axis='y', labelsize=8)
        ax.set_xticks(ax.get_xticks()[::4]) 
        ax.set_yticks(ax.get_yticks()[::4])
        ax.set_xticklabels(ax.get_xticklabels(), rotation=0)

        etiquetas = [f'{v}' for v in grupos]
        parches = [mpatches.Patch(color=cmap(norm(grupo)), label=etiqueta) for grupo, etiqueta in zip(grupos, etiquetas)]
        legend = ax.legend(handles=parches, title='Grupos', loc='upper right', bbox_to_anchor=(1.17, 1), fontsize=8, title_fontsize=10)
        legend.get_title().set_fontweight('bold')

        plt.subplots_adjust(right=0.86)
        
        plt.savefig(f'{rutaS}/Clusters_{fase}_{estadistico}.pdf')
        plt.close()
