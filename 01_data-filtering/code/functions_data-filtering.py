#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: eriktapia
"""

import platform 
import os
import pathlib
import datetime as dt
import calendar
import pandas as pd
import sys
import math
import xarray as xr
import statistics

def limpiar():
    sistema_operativo = platform.system()
    if sistema_operativo == 'Windows':
        limpiar = 'cls'
    else:
        limpiar = 'clear'
    return limpiar

def menu_principal(limpiar):
    os.system(limpiar)
    print('                                 MENÚ PRINCIPAL')
    print('1) Generar series de tiempo horarias, solo potencias \n2) Generar series de tiempo promedios diarios, solo potencias \n3) Estadísticos de potencias para periodos ingresados en un archivo \n0) Salir')
    opc_uno = input('\nSelecciona una opción: ')
    try:
        opc_uno = int(opc_uno)
    except:
        opc_uno = -1
    os.system(limpiar)
    return opc_uno

def solicitar_periodo(limpiar):
    continuar_p1 = True
    while continuar_p1:
        os.system(limpiar)
        print('                                 PERIODO DE ANÁLISIS')
        print('1) Un año \n2) Un intervalo de tiempo')
        opc_dos = input('\nSelecciona una opción: ')
        try:
            opc_dos = int(opc_dos)
        except:
            opc_dos = -1
        os.system(limpiar)
        
        if opc_dos == 1: #Un año
            periodo = [0]
            continuar_p2 = True
            while continuar_p2:
                print('Asegúrate de que el año de análisis se encuentre entre los años 1940 y 2022.')
                periodo[0] = input('Indica el año de estudio: ')
                os.system(limpiar)
                try:
                    periodo[0] = int(periodo[0])
                    continuar_p2 = False
                    os.system(limpiar)
                except:
                    print('El año de estudio debe ser un dato del tipo entero.')
            fecha_i = dt.datetime(periodo[0], 1, 1, 0)
            fecha_f = dt.datetime(periodo[0], 12, calendar.monthrange(periodo[0], 12)[1], 23)
            continuar_p1 = False
                        
        elif opc_dos == 2: #Un periodo de tiempo
            dia = [0, 0]
            mes = [0, 0]
            periodo = [0, 0]
            for i in range(2):
                continuar_p3 = True
                while continuar_p3:
                    print('NOTA: Asegúrate de que el año de inicio sea menor al año final y que ambas fechas se encuentren entre los años 1940 y 2022..')
                    if i == 0:
                        dia[i] = input('Indica el día de inicio del periodo: ')
                        mes[i] = input('Indica el mes de inicio del periodo: ')
                        periodo[i] = input('Indica el año de inicio del periodo: ')
                    else:
                        dia[i] = input('Indica el día final del periodo: ')
                        mes[i] = input('Indica el mes final del periodo: ')
                        periodo[i] = input('Indica el año final del periodo: ')
                    os.system(limpiar)
                    
                    try:
                        dia[i] = int(dia[i])
                        mes[i] = int(mes[i])
                        periodo[i] = int(periodo[i])
                        continuar_p3 = False
                        os.system(limpiar)
                    except:
                        print('La fecha ingresada debe ser un dato del tipo entero.')
            fecha_i = dt.datetime(periodo[0], mes[0], dia[0], 0)
            fecha_f = dt.datetime(periodo[1], mes[1], dia[1], 23)
            continuar_p1 = False
            
        else: #Opcion no válida
            input('Opción no válida, presiona enter para continuar...')
            
    return periodo, fecha_i, fecha_f

def generar_subRutas(rutaE, periodo, tipo):
    rutaGeneral = pathlib.Path(f'{rutaE}')
    subRutas = []
    for i in range(periodo[-1]-periodo[0]+1):
        subRutas += rutaGeneral.glob(f'*{periodo[0]+i}*{tipo}.nc')
    return subRutas

def generar_coordenadas(rutaCoord, limpiar):
    try:
        df_coord = pd.read_csv(rutaCoord, sep='\t')
        lat = df_coord['lat'].tolist()
        lon = df_coord['lon'].tolist()
        if isinstance(lat, list) and isinstance(lon, list):
            os.system(limpiar)
            print('Las coordenadas se cargaron con éxito.')
            input('Presiona ENTER para continuar con la ejecución del programa...')
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

def leer_periodos(rutaPeriodos, limpiar):
    try:
        df_periodos = pd.read_csv(rutaPeriodos, sep='\t')
        di = df_periodos['di'].tolist()
        mi = df_periodos['mi'].tolist()
        ai = df_periodos['ai'].tolist()
        df = df_periodos['df'].tolist()
        mf = df_periodos['mf'].tolist()
        af = df_periodos['af'].tolist()
        suf = df_periodos['suf'].tolist()
        if isinstance(di, list) and isinstance(mi, list) and isinstance(ai, list) and isinstance(df, list) and isinstance(mf, list) and isinstance(af, list) and isinstance(suf, list):
            os.system(limpiar)
            print('Los periodos se cargaron con éxito.')
            input('Presiona ENTER para continuar con la ejecución del programa...')
            os.system(limpiar)
    except:
        os.system(limpiar)
        print('Hubo un error al tratar de cargar los periodos.')
        print('- Los periodos deben colocarse en un archivo periodos.txt el cual tendrá en la primera columna, con encabezado “di”, el día de inicio; en la segunda, con encabezado “mi”, el mes de inicio; en la tercera, con encabezado “ai”, el año de inicio; en la cuarta, con encabezado “df”, el día final; en la quinta, con encabezado “mf”, el mes final; en la sexta, con encabezado “af”, el año final; y en la séptima, con encabezado “suf”, el identifiador del periodo, todas separadas entre sí por tabulaciones.')
        print(f'- Revisa que la ruta del archivo sea correcta, actualmente esta es: {rutaPeriodos}')
        input('\nPresiona ENTER para terminar la ejecución del programa...')
        sys.exit()
    return di, mi, ai, df, mf, af, suf

def generar_periodos(di, mi, ai, df, mf, af):
    fecha_i = []
    fecha_f = []
    dia = [di, df]
    mes = [mi, mf]
    periodo = [ai, af]
    for i in range(len(di)):
        fecha_i.append(dt.datetime(periodo[0][i], mes[0][i], dia[0][i], 0))
        fecha_f.append(dt.datetime(periodo[1][i], mes[1][i], dia[1][i], 23))
    return periodo, fecha_i, fecha_f

def generar_arregloFinal(tipo,subRutas,lat,lon, fecha_i, fecha_f): 
    dataframes = []
    for archivoIt in subRutas:
        with xr.open_dataset(archivoIt) as archivoAbierto:
            if tipo == 'HT':
                infoFiltrada = archivoAbierto.sel(latitude=lat, longitude=lon, time=slice(fecha_i, fecha_f))[['swh', 'pp1d']] 
            elif tipo == 'WP':
                infoFiltrada = archivoAbierto.sel(latitude=lat, longitude=lon, time=slice(fecha_i, fecha_f))[['u10', 'v10']]
            df = infoFiltrada.to_dataframe()
            dataframes.append(df)
    arregloFinal = ordenar_arregloFinal(tipo, dataframes)
    return arregloFinal

def ordenar_arregloFinal(tipo, dataframes):
    arregloBase = pd.concat(dataframes)

    if tipo == 'HT':
        arregloBase['longitude'] = arregloBase['longitude'].round(1)
        arregloBase['latitude'] = arregloBase['latitude'].round(1)
        arregloBase = arregloBase.rename(columns={'longitude': 'Lon'})
        arregloBase = arregloBase.rename(columns={'latitude': 'Lat'})
        arregloBase['Año'] = arregloBase.index.year
        arregloBase['Mes'] = arregloBase.index.month
        arregloBase['Día'] = arregloBase.index.day
        arregloBase['Hora'] = arregloBase.index.hour
        
        arregloBase['Pwave'] =  arregloBase.apply(lambda row: 1025*9.81**2/(64*math.pi)*row['pp1d']*row['swh']**2/1000, axis=1)
        arregloBase['Pwave'] = arregloBase['Pwave'].round(4)
        arregloBase = arregloBase.drop(columns=['swh','pp1d'])
        ordenVariables = ['Lat','Lon','Año','Mes','Día','Hora','Pwave']
        arregloFinal = arregloBase.reindex(columns=ordenVariables)  
        
    elif tipo == 'WP':
        arregloBase = arregloBase.drop(columns='longitude')
        arregloBase = arregloBase.drop(columns='latitude')
        arregloBase['vw'] = arregloBase.apply(lambda row: (row['u10']**2 + row['v10']**2)**(1/2), axis=1)  
        arregloBase['Pwind'] =  arregloBase.apply(lambda row: 0.5*1.225*row['vw']**3/1000, axis=1)
        arregloBase['Pwind'] = arregloBase['Pwind'].round(4)
        arregloBase = arregloBase.drop(columns=['u10','v10','vw'])
        ordenVariables = ['Pwind']
        arregloFinal = arregloBase.reindex(columns=ordenVariables)
        
    return arregloFinal
       
def generar_txt(periodo, fecha_i, fecha_f, rutaE, lat, lon, rutaS):
    print(f'                     SERIES DE TIEMPO HORARIAS {fecha_i} - {fecha_f}')
    for i in range(len(lat)): 
        for tipo in ['HT','WP']: 
            subRutas = generar_subRutas(rutaE, periodo, tipo)
            if tipo == 'HT':
                print(f'Generando el archivo de datos tipo Potencias para las coordenadas ({lat[i]},{lon[i]})...')
                dfDatosHT = generar_arregloFinal(tipo,subRutas,lat[i],lon[i], fecha_i, fecha_f)
            else:
                dfDatosWP = generar_arregloFinal(tipo,subRutas,lat[i],lon[i], fecha_i, fecha_f)
                dfDatos = pd.concat([dfDatosHT, dfDatosWP], axis = 1)
                with open(f'{rutaS}/({lat[i]},{lon[i]})_PotH_{periodo}.txt','w') as archivoGenerado:
                    dfDatos.to_csv(archivoGenerado, sep = '\t', index=False)
    return None

def generar_txtPD(periodo, fecha_i, fecha_f, rutaE, lat, lon, rutaS):
    print(f'                     SERIES DE TIEMPO PROMEDIO DIARIO {fecha_i} - {fecha_f}')
    subRutasHT = generar_subRutas(rutaE, periodo, 'HT')
    subRutasWP = generar_subRutas(rutaE, periodo, 'WP')
    for i in range(len(lat)):
        print(f'Generando el archivo de datos para las coordenadas ({lat[i]},{lon[i]})...')
        dfDatosHT = generar_arregloFinal('HT',subRutasHT,lat[i],lon[i], fecha_i, fecha_f)
        dfDatosWP = generar_arregloFinal('WP',subRutasWP,lat[i],lon[i], fecha_i, fecha_f)
        dfDatos = pd.concat([dfDatosHT, dfDatosWP], axis=1)  
        dfProm = dfDatos.groupby(['Lat','Lon','Año','Mes','Día'])[['Pwave', 'Pwind']].mean().reset_index()
        dfProm['Pwave'] = dfProm['Pwave'].round(4)
        dfProm['Pwind'] = dfProm['Pwind'].round(4)

        with open(f'{rutaS}/({lat[i]},{lon[i]})_PotD_{periodo}.txt','w') as archivoGenerado:
            dfProm.to_csv(archivoGenerado, sep = '\t', index=False)
    return None

def generar_estadisticosPIndef(periodo, fecha_i, fecha_f, rutaE, lat, lon, rutaS, suf):
    print('                     PROMEDIOS PARA PERIODOS INGRESADO EN UN ARCHIVO')
    for i in range(len(suf)):
        PwaveProm, PwaveS, PwaveCV, PwaveMed, PwaveMax, PwaveMin = [], [], [], [], [], []
        PwindProm, PwindS, PwindCV, PwindMed, PwindMax, PwindMin = [], [], [], [], [], []
        dataframes = []
        Periodo = [periodo[0][i],periodo[1][i]]
        for tipo in ['HT','WP']:
            subRutas = generar_subRutas(rutaE, Periodo, tipo)
            for j in range(len(lat)):
                dfDatos = generar_arregloFinal(tipo,subRutas,lat[j],lon[j], fecha_i[i], fecha_f[i])
                if tipo == 'HT':
                    print(f'Generando estadísticos de Pwave para {suf[i]} coordenada {lat[j]}°,{lon[j]}°...')
                    PwaveCol = dfDatos['Pwave'].tolist()
                    waveprom = sum(PwaveCol)/len(PwaveCol)
                    PwaveProm.append(waveprom)
                    waves = statistics.stdev(PwaveCol)
                    PwaveS.append(waves)
                    PwaveCV.append(waves/waveprom*100)
                    PwaveMed.append(statistics.median(PwaveCol))
                    PwaveMax.append(max(PwaveCol))
                    PwaveMin.append(min(PwaveCol))
 
                elif tipo == 'WP':
                    print(f'Generando estadísticos de Pwind para {suf[i]} coordenada {lat[j]}°,{lon[j]}°...')
                    PwindCol = dfDatos['Pwind'].tolist()
                    windprom = sum(PwindCol)/len(PwindCol)
                    PwindProm.append(windprom)
                    winds = statistics.stdev(PwindCol)
                    PwindS.append(winds)
                    PwindCV.append(winds/windprom*100)
                    PwindMed.append(statistics.median(PwindCol))
                    PwindMax.append(max(PwindCol))
                    PwindMin.append(min(PwindCol))
                    
        
        estadisticos = ['PwaveProm', 'PwaveS', 'PwaveCV', 'PwaveMed', 'PwaveMax', 'PwaveMin','PwindProm', 'PwindS', 'PwindCV', 'PwindMed', 'PwindMax', 'PwindMin']
        for columna, nombreCol in zip([PwaveProm, PwaveS, PwaveCV, PwaveMed, PwaveMax, PwaveMin, PwindProm, PwindS, PwindCV, PwindMed, PwindMax, PwindMin], estadisticos):
            dfAux = pd.DataFrame(columna, columns=[nombreCol])
            dataframes.append(dfAux)
        dfEstadisticos = pd.concat(dataframes, axis=1)
        dfEstadisticos.insert(0, 'lat', lat)
        dfEstadisticos.insert(1, 'lon', lon)
        
        for col in ['lat', 'lon']:
            dfEstadisticos[col] = dfEstadisticos[col].round(1)
            
        for col in ['PwaveS', 'PwaveCV', 'PwindS', 'PwindCV']:
            dfEstadisticos[col] = dfEstadisticos[col].round(2)
            
        for col in ['PwaveProm', 'PwaveMed', 'PwaveMax', 'PwaveMin', 'PwindProm', 'PwindMed', 'PwindMax', 'PwindMin']:
            dfEstadisticos[col] = dfEstadisticos[col].round(4)
    
        with open(f'{rutaS}/{suf[i]}.txt','w') as archivoGenerado:
            dfEstadisticos.to_csv(archivoGenerado, sep = '\t', index=False)
            print(f'Archivo de promedios generado para {suf[i]}...')
    return None
