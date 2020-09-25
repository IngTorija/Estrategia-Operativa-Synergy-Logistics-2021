"""
Created on Wed Sep 23 20:11:06 2020
@author: Alejandro Torija Méndez
"""
"""
register_id,direction,origin,destination,year,date,product,
transport_mode,company_name,total_value
"""
import csv
"""Función para recolectar las rutas, obtener la ocurrencia de viajes en cada una
   y los ingresos que genera cada una"""
def rutas(direccion,lista_datos):
    contador = 0
    valor = 0
    rutas_contadas = []
    conteo_rutas = []
    for ruta in lista_datos:
        if ruta[1] == direccion:
            ruta_actual = [ruta[2],ruta[3]]
            if ruta_actual not in rutas_contadas:
                for movimiento in lista_datos:
                    if ruta_actual == [movimiento[2],movimiento[3]]:
                        contador+=1
                        valor+= int(movimiento[9])
                rutas_contadas.append(ruta_actual)
                conteo_rutas.append([ruta[2],ruta[3],contador,valor])
                contador = 0
                valor = 0
    conteo_rutas.sort(key = lambda item: item[2],reverse = True)
    return(conteo_rutas)
""" Función para recolectar los modos de transportes 
    y la ocurrencia y ganancia de cada uno"""
def func_transport(transportes,lista_datos):
    contador = 0
    valor = 0
    transportes_contados = []
    conteo_transporte = []
    for transport in transportes:
        for dato in lista_datos:
            if dato[7] == transport:
                trans_actual = dato[7]
                if trans_actual not in transportes_contados:
                    for movimiento in lista_datos:
                        if trans_actual == movimiento[7]:
                            contador+=1
                            valor+= int(movimiento[9])
                    transportes_contados.append(trans_actual)
                    conteo_transporte.append([dato[7],contador,valor])
                    contador = 0
                    valor = 0
    conteo_transporte.sort(key = lambda item: item[2],reverse = True)
    return(conteo_transporte)
"""
Función para encontrar los ingresos recibidos de cada pais
tanto en importaciones como exportaciones"""
def func_paises(paises,lista_datos):
    contador = 0
    valor = 0
    paises_contados = []
    paises_contados_imp = [] 
    conteo_pais = []
    conteo_pais_imp = []
    for pais in paises:
        for dato in lista_datos:
            if dato[2] == pais and dato[1] == "Exports":
                pais_actual = dato[2]
                if pais_actual not in paises_contados:
                    for movimiento in lista_datos:
                        if pais_actual == movimiento[2]:
                            contador+=1
                            valor+= int(movimiento[9])
                    paises_contados.append(pais_actual)
                    conteo_pais.append([dato[2],contador,valor])
                    contador = 0
                    valor = 0
            elif dato[3] == pais and dato[1] == "Imports":
                pais_actual = dato[3]
                if pais_actual not in paises_contados_imp:
                    for movimiento in lista_datos:
                        if pais_actual == movimiento[3]:
                            contador+=1
                            valor+= int(movimiento[9])
                    paises_contados_imp.append(pais_actual)
                    conteo_pais_imp.append([dato[3],contador,valor])
                    contador = 0
                    valor = 0

                
    conteo_pais.sort(key = lambda item: item[2],reverse = True)
    conteo_pais_imp.sort(key = lambda item: item[2],reverse = True)
    
    return(conteo_pais,conteo_pais_imp)

lista_datos = []
transportes = []
paises = []
#---------Abrir archivo de texto y extracción de valores necesarios------------
with open("synergy_logistics_database.csv","r") as archivo_csv:
    lector = csv.reader(archivo_csv)
 
    for linea in lector:
        lista_datos.append(linea)
        transportes.append(linea[7])
        paises.append(linea[2])
        paises.append(linea[3])
    #Eliminación de los elementos repetidos en transporte y países    
    transportes = set(transportes)
    transportes = list(transportes)
    paises = set(paises)
    paises = list(paises)

#------------------------------GENERAR RUTAS----------------------------------

rutas_exportacion = rutas("Exports",lista_datos)
rutas_importacion = rutas("Imports",lista_datos)

rutas_export_valor = sorted(rutas_exportacion,key = lambda item: item[3],reverse = True)
rutas_import_valor = sorted(rutas_importacion,key = lambda item: item[3],reverse = True)

#------------------------------TRANSPORTE-------------------------------------
lista_datos = lista_datos[1:]
transportes = func_transport(transportes,lista_datos)


#------------------------------80% de Ganancias--------------------------------

lista_datos = lista_datos[1:]
paises_exp,paises_imp = func_paises(paises,lista_datos)

#-------Obtención del total de ingresos para exportaciones e importaciones-----
ingresos_exp = 0
ingresos_imp = 0

for dato in lista_datos:
    if dato[1] == "Exports":
        ingresos_exp += int(dato[9])
    elif dato[1] == "Imports":
        ingresos_imp += int(dato[9])

#-------------Cálculo del 80% de dichos ingresos
ochnt_prcnt_exp = 80*ingresos_exp/100
ochnt_prcnt_imp = 80*ingresos_imp/100


## Paises que contribuyen al 80% del ingreso total
suma_pais = int(paises_exp[0][2])
paises_80_exp =[]
paises_80_imp = []
i =0
while suma_pais <= ochnt_prcnt_exp:
    paises_80_exp.append(paises_exp[i])
    suma_pais += int(paises_exp[i+1][2])
    i+=1
    
suma_pais = int(paises_imp[0][2])
i = 0
while suma_pais <= ochnt_prcnt_imp:
    paises_80_imp.append(paises_imp[i])
    suma_pais += int(paises_imp[i+1][2])
    i+=1

####--------------Despliegue de todos lo datos------------------------------
def impresion(lista):
    for item in lista:
        print(item)

##10 Mejores rutas
print("Synergy Logistics \nReporte de Ingresos y Estrategia de inversión \n\n")
print("Mejores Rutas de Exportación, por ingresos: \n")
print("[Destino,Origen,Viajes,Ingresos]\n")
impresion(rutas_export_valor[0:10])
print("--------------------------------------------")

print("Mejores Rutas de Importación, por ingresos: \n")
print("[Destino,Origen,Viajes,Ingresos]\n")
impresion(rutas_import_valor[0:10])
print("--------------------------------------------")

##Mejores Transportes
print("Mejores Medios de Transporte, por ingresos: \n")
print("[Modo de Transporte,Viajes,Ingresos]\n")
impresion(transportes[0:3])
print("--------------------------------------------")

##80% de ingresos

print("Países que aportan el 80% de ingresos, por Exportación: \n")
print("[País,Viajes,Ingresos]\n")
impresion(paises_80_exp)
print("--------------------------------------------")


print("Países que aportan el 80% de ingresos, por Importación: \n")
print("[País,Viajes,Ingresos]\n")
impresion(paises_80_imp)
print("--------------------------------------------")


            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            



