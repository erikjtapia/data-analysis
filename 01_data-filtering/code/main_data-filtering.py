#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: eriktapia
Este código usa la base de datos ERA5 México para:
    1) Generar series de tiempo horarias solo de potencias 
        - Un archivo unificado, con las variables: "Lat, Lon, Año, Mes, Día, Hora, Pwave, Pwind"
    2) Generar series de tiempo promedios diarios solo de potencias 
        - Un archivo unificado, con las variables: "Lat, Lon, Año, Mes, Día, Pwave, Pwind"
    3) Promedios de potencias para periodos ingresados en un archivo
        - Un archivo unificado, con las variables: "Lat, Lon, 'PwaveProm', 'PwaveS', 'PwaveCV', 'PwaveMed', 'PwaveMax', 'PwaveMin','PwindProm', 'PwindS', 'PwindCV', 'PwindMed', 'PwindMax', 'PwindMin'"
"""
import functions_data-filtering as fg
import os


def main():
    limpiar = fg.limpiar()
    rutaE = 'DatoRemovidoPorPrivacidad'
    rutaCoord = 'DatoRemovidoPorPrivacidad'
    rutaPeriodos = 'DatoRemovidoPorPrivacidad'
    rutaS = 'DatoRemovidoPorPrivacidad'
    lat, lon = fg.generar_coordenadas(rutaCoord, limpiar)
    continuar = True
    while continuar:
        opc_uno = fg.menu_principal(limpiar)
        
        if opc_uno == 1: # Series de tiempo horarias  
            periodo, fecha_i, fecha_f = fg.solicitar_periodo(limpiar)
            fg.generar_txt(periodo, fecha_i, fecha_f, rutaE, lat, lon, rutaS,)
            os.system(limpiar)
            input(f'Los archivos se han generado con éxito en la siguiente ruta: {rutaS} \nPresiona ENTER para continuar...')
            
        elif opc_uno == 2: # Series de tiempo promedios diarios
            periodo, fecha_i, fecha_f = fg.solicitar_periodo(limpiar)
            fg.generar_txtPD(periodo, fecha_i, fecha_f, rutaE, lat, lon, rutaS,)
            os.system(limpiar)
            input(f'Los archivos se han generado con éxito en la siguiente ruta: {rutaS} \nPresiona ENTER para continuar...')
        
        elif opc_uno == 3: # Promedios periodo en archivo
            di, mi, ai, df, mf, af, suf = fg.leer_periodos(rutaPeriodos, limpiar)
            periodo, fecha_i, fecha_f = fg.generar_periodos(di, mi, ai, df, mf, af)
            fg.generar_estadisticosPIndef(periodo, fecha_i, fecha_f, rutaE, lat, lon, rutaS, suf)
            os.system(limpiar)
            input(f'Los archivos se han generado con éxito en la siguiente ruta: {rutaS} \nPresiona ENTER para continuar...')
 
        elif opc_uno == 0: #Salir
            continuar = False
            
        else: #Opcion no válida
            input('Opción no válida, presiona enter para continuar...')
    return None

if __name__== '__main__':
    main()
