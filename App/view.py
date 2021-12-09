"""
 * Copyright 2020, Departamento de sistemas y Computación, Universidad
 * de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along withthis program.  If not, see <http://www.gnu.org/licenses/>.
 """

import config as cf
import sys
import controller as c
from DISClib.ADT import list as lt
from DISClib.ADT import graph as gr
from DISClib.ADT import map as mp
from DISClib.ADT import stack as st
from DISClib.DataStructures import mapentry as me
assert cf
import time
import threading

"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""


def printFirst(catalogo, i):
    llaves=mp.keySet(catalogo[i])
    p=lt.firstElement(llaves)
    pri=mp.get(catalogo[i], p)
    valor = me.getValue(pri)
    if i=="aeropuertos":
        print("Nombre: "+valor["Name"] +" Ciudad: "+valor["City"]+" País: "+valor["Country"]+" Latitud: "+valor["Latitude"]+" Longitud: "+valor["Longitude"])
    elif i=="ciudades":
        valor = lt.removeLast(valor)
        print("Nombre: " + valor["city_ascii"]+" Latitud: "+valor["lat"]+" Longitud: "+valor["lng"]+" Población: "+valor["population"])

def printReq1(datos):
    tamanio = lt.size(datos)
    if tamanio>0:
        for d in lt.iterator(datos):
            if d is not None:
                print('IATA: ' + d['IATA'] + ', Nombre: ' + d['Name']+ ', Ciudad: ' + d['City'] + ', Pais: ' + d['Country']) 
    else:   
        print ("No hay datos")


def printAero(d):
    if d is not None:
        print('IATA: ' + d['IATA'] + ', Nombre: ' + d['Name']+ ', Ciudad: ' + d['City'] + ', Pais: ' + d['Country'])

def printreq3(catalogo,origen,destino):
    respuesta=c.Req3(catalogo,origen,destino)
    aero_origen=lt.removeFirst(respuesta)
    aero_destino=lt.removeFirst(respuesta)
    ruta = lt.removeFirst(respuesta)
    dt_origen= lt.removeFirst(respuesta)
    dt_destino= lt.removeFirst(respuesta)
    d_aerea=lt.newList()
    print('Aeropuerto de origen: ')
    printAero(aero_origen)
    print('Aeropuerto de destino: ')
    printAero(aero_destino)
    print('Ruta Aérea por segmentos: ')
    tamanio=st.size(ruta)
    i=0
    while i<tamanio:
        path=st.pop(ruta)
        print(str(path))
        lt.addLast(d_aerea,float(path['weight']))
        i += 1
    total_a = 0
    for distancia in lt.iterator(d_aerea):
        total_a+=distancia
    print('Distancia total ruta: ' + str(int(dt_origen+dt_destino+total_a)))
    print('Distancia total aereo: ' + str(int(total_a)))
    print('Distancia ciudad aeropuerto origen: ' + str(int(dt_origen)))
    print('Distancia ciudad aeropuerto destino: ' + str(int(dt_destino)))

def printreq5(catalogo,aeropuerto):
    respuesta=c.Req5(catalogo,aeropuerto)
    num=lt.removeFirst(respuesta)
    l=lt.removeFirst(respuesta)
    print('Numero de aeropuertos afectados: ' + str(num))
    print('Lista de aeropuertos afectados: ')
    printReq1(l)
    return None

def printDatos(catalogo):
    print("Información Grafo Dirigido")
    print("Total de aeropuertos: " + str(gr.numVertices(catalogo['red'])))
    print("Total de rutas: " + str(gr.numEdges(catalogo['red'])))
    print("Información Grafo No Dirigido")
    print("Total de aeropuertos: " + str(gr.numVertices(catalogo['blue'])))
    print("Total de rutas: " + str(gr.numEdges(catalogo['blue'])))
    print("Total de ciudades: "+  str(mp.size(catalogo["ciudades"])))
    print("Primer Aeropuerto Cargado: ")
    printFirst(catalogo, "aeropuertos")
    print("Primera Ciudad Cargada: ")
    printFirst(catalogo, "ciudades")


def printMenu():
    print("\n")
    print("***************")
    print("Bienvenido")
    print("1- Carga de datos")
    print("2- Encontrar puntos de interconexión aérea ")
    print("3- Encontrar clústeres de tráfico aéreo")
    print("4-  Encontrar la ruta más corta entre ciudades ")
    print("5- Utilizar las millas de viajero ")
    print("6- Cuantificar el efecto de un aeropuerto cerrado ")
    print("0- Salir")
    print("***************")

catalog = None

"""
Menu principal
"""
while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar\n')
    if int(inputs[0]) == 1:
        print("Cargando información de los archivos ....")
        catalogo=c.initCatalog()
        start_time=time.process_time()
        c.loadData(catalogo)
        stop_time=time.process_time()
        elapsed_time_mseg=(stop_time - start_time)*1000
        print("Tiempo empleado: " + str(elapsed_time_mseg))
        printDatos(catalogo)
    
    elif int(inputs[0]) == 2:
        start_time=time.process_time()
        aeropuertos=c.Req1(catalogo)
        conectados=lt.removeLast(aeropuertos)
        printReq1(aeropuertos)
        stop_time=time.process_time()
        elapsed_time_mseg=(stop_time - start_time)*1000
        print("Tiempo empleado: " + str(elapsed_time_mseg))
        print('Número de aeropuertos: ' + str(conectados))

    elif int(inputs[0]) == 3:
        a1=input("Ingrese el Codigo IATA del primer aeropuerto: ")
        a2= input("Ingrese el Codigo IATA del segundo aeropuerto: ")
        start_time = time.process_time()
        Req2(catalogo, a1, a2)
        stop_time = time.process_time()
        elapsed_time_mseg = (stop_time - start_time)*1000
        print("Tiempo empleado: " + str(elapsed_time_mseg))
    
    elif int(inputs[0]) == 4:
        o=input('Ciudad origen: ')
        d=input('Ciudad destino: ' )
        start_time = time.process_time()
        printreq3(catalogo,o,d)
        stop_time = time.process_time()
        elapsed_time_mseg = (stop_time - start_time)*1000
        print("Tiempo empleado: " + str(elapsed_time_mseg))

    elif int(inputs[0]) == 5:
        start_time = time.process_time()
        Requerimiento4(catalogo)
        stop_time = time.process_time()
        elapsed_time_mseg = (stop_time - start_time)*1000
        print("Tiempo de ejecución: " + str(elapsed_time_mseg))


    elif int(inputs[0]) == 6:
        a=input('Ingrese el IATA del aeropuerto fuera de funcionamiento: ')
        start_time = time.process_time()
        printreq5(catalogo,a)
        stop_time = time.process_time()
        elapsed_time_mseg = (stop_time - start_time)*1000
        print("Tiempo empleado: " + str(elapsed_time_mseg))
    else:
        sys.exit(0)
sys.exit(0)
