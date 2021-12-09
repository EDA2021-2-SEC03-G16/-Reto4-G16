"""
 * Copyright 2020, Departamento de sistemas y Computación,
 * Universidad de Los Andes
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
 *
 * Contribuciones:
 *
 * Dario Correal - Version inicial
 """

import config
from DISClib.DataStructures import mapentry as me
from DISClib.Algorithms.Graphs import scc
from DISClib.Algorithms.Sorting import mergesort as ms
from DISClib.Algorithms.Graphs import dfs
from DISClib.Algorithms.Graphs import dijsktra as djk
from DISClib.DataStructures.arraylist import addLast
from DISClib.ADT.graph import gr
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.ADT import orderedmap as om
from DISClib.Algorithms.Graphs import prim
from DISClib.ADT import queue as q
from DISClib.ADT import stack as st
assert config
from math import radians, cos, sin, asin, sqrt

"""
En este archivo definimos los TADs que vamos a usar y las operaciones
de creacion y consulta sobre las estructuras de datos.
"""

def newCatalogo():
    """ Inicializa el analizador
    airports: tabla de hash para guardar los vertices del grafo
    red: grafo para representar los vuelos entre aeropuertos
    """
    
    catalogo={'red': None,
            'aeropuertos': None,
            'components': None}

    catalogo['red']=gr.newGraph(datastructure='ADJ_LIST',directed=True,size=14000,comparefunction=None)
    catalogo['blue']=gr.newGraph(datastructure='ADJ_LIST',directed=False,size=14000,comparefunction=None)                                       
    catalogo['aeropuertos']=mp.newMap()
    catalogo['ciudades']=mp.newMap()
    catalogo['ciudades_id']=mp.newMap()
    catalogo['latlng']=om.newMap() 
    return catalogo


def addAirport(catalogo,aeropuerto):
    iata=aeropuerto['IATA']
    mp.put(catalogo['aeropuertos'],iata,aeropuerto)
    if not gr.containsVertex(catalogo['red'], iata):
            gr.insertVertex(catalogo['red'], iata)
    mapaordenado=catalogo['latlng']
    latitud=float(aeropuerto['Latitude'])
    longitud=float(aeropuerto['Longitude'])
    existelatitud=om.contains(mapaordenado,latitud)
    if existelatitud:
        pareja=om.get(mapaordenado,latitud)
        ordenmapa=me.getValue(pareja)
        existelongitud=om.contains(ordenmapa,longitud)
        if existelongitud:
            pareja2=om.get(ordenmapa,longitud)
            lista=me.getValue(pareja2)
        else:
            lista=lt.newList()
        lt.addLast(lista,aeropuerto)
        om.put(ordenmapa,longitud,lista)
    else:
        ordenmapa=om.newMap()
        lista=lt.newList()
        lt.addLast(lista,aeropuerto)
        om.put(ordenmapa,longitud,lista)
        om.put(mapaordenado,latitud,ordenmapa)
    return catalogo


def addRoute(catalogo, ruta):
    origin = ruta['Departure']
    destination = ruta['Destination']
    distance = ruta['distance_km']
    edge = gr.getEdge(catalogo['red'], origin, destination)
    if edge is None:
        gr.addEdge(catalogo['red'], origin, destination, float(distance))
    return catalogo


def addCity(catalogo, ciudad):
    name = ciudad['city_ascii']
    ciudades = catalogo['ciudades']
    existecity = mp.contains(ciudades,name)
    if existecity:
        pareja=mp.get(ciudades,name)
        lista=me.getValue(pareja)
    else:
        lista=lt.newList()
    lt.addLast(lista,ciudad)
    mp.put(ciudades,name,lista)
    id=ciudad['id']
    ciudades_id=catalogo['ciudades_id']
    mp.put(ciudades_id,id,ciudad)
    return catalogo


def addRouteCompleto(catalogo, ruta):
    origen=ruta['Departure']
    destino=ruta['Destination']
    distancia=ruta['distance_km']
    red=catalogo["red"]
    edge=gr.getEdge(red, destino, origen)
    if edge is not None:
        if gr.containsVertex(catalogo["blue"], destino) is not True:
            gr.insertVertex(catalogo["blue"], destino)
        if gr.containsVertex(catalogo["blue"], origen) is not True:
            gr.insertVertex(catalogo["blue"], origen)
        gr.addEdge(catalogo["blue"], destino, origen, distancia)
    return catalogo


def ordenAscendenteD(a1,a2):
    if (a1>a2):
        return 0
    return -1


def Req1(catalogo):
    red=catalogo['red']
    aeropuertos=gr.vertices(red)
    conexiones=lt.newList()
    for aeropuerto in lt.iterator(aeropuertos):
        numero=gr.degree(red,aeropuerto)
        if numero>200:
            lt.addLast(conexiones,numero)
    ms.sort(conexiones,ordenAscendenteD)
    conexiones=lt.lastElement(conexiones)
    maximo_conectados=lt.newList()
    for aeropuerto in lt.iterator(aeropuertos):
        n=gr.degree(red,aeropuerto)
        if int(n)==int(conexiones):
            lt.addLast(maximo_conectados,aeropuerto)
    aeropuertos=catalogo['aeropuertos']
    resultado=lt.newList('ARRAY_LIST')
    for ide in lt.iterator(maximo_conectados):
        pareja=mp.get(aeropuertos,ide)
        valor=me.getValue(pareja)
        lt.addLast(resultado,valor)
    lt.addLast(resultado,conexiones)
    return resultado


#R2

#R3
def formula(longitud1, latitud1, longitud2, latitud2):
    longitud1, latitud1, longitud2, latitud2=map(radians, [longitud1, latitud1, longitud2, latitud2])
    distancialon=longitud2-longitud1 
    distancialat=latitud2-latitud1 
    a=sin(distancialat/2)**2+cos(latitud1)*cos(latitud2)*sin(distancialon/2)**2
    c=2*asin(sqrt(a)) 
    radio=6371
    return c*radio

def igual(origen,destino):
    print('Posibles ciudades origen: ')
    for valor in lt.iterator(origen):
        print("ID: " + valor['id'] + " Nombre: " + valor["city_ascii"] + " Latitud: " + valor["lat"] + " Longitud: " + valor["lng"] + " Pais: " + valor["country"] + " Subregion: " + valor['admin_name'])
    print('Posibles ciudades destino: ')                                                        
    for valor in lt.iterator(destino):
        print("ID: " + valor['id'] + " Nombre: " + valor["city_ascii"] + " Latitud: " + valor["lat"] + " Longitud: " + valor["lng"] + " Pais: " + valor["country"] + " Subregion: " + valor['admin_name'])                                             
    id_origen=input('Escoja la ciudad de origen deseada (ID): ')
    id_destino=input('Escoja la ciudad de destino deseada (ID): ')
    ids=lt.newList()
    lt.addLast(ids,id_origen)
    lt.addLast(ids,id_destino)
    return ids


def req3(catalogo,origen,destino):
    ciudades=catalogo['ciudades']
    aeropuertos_ord=catalogo['latlng']
    origen=mp.get(ciudades,origen)
    lista_origen=me.getValue(origen)
    destino=mp.get(ciudades,destino)
    lista_destino=me.getValue(destino)
    if (lt.size(lista_origen)>1) or (lt.size(lista_destino)>1):
        ids=igual(lista_origen,lista_destino)
        id_origen=lt.removeFirst(ids)
        id_destino=lt.removeFirst(ids)
        mapa=catalogo['ciudades_id']
        porigen=mp.get(mapa,id_origen)
        pdestino=mp.get(mapa,id_destino)
        o=me.getValue(porigen)
        d=me.getValue(pdestino)
    else:
        o=lt.removeLast(lista_origen)
        d=lt.removeLast(lista_destino)
    aeropuertos_o=lt.newList()
    aeropuertos_d= lt.newList()
    origen_lat=float(o['lat'])
    origen_lng=float(o['lng'])
    destino_lat=float(d['lat'])
    destino_lng=float(d['lng'])
    olat_1=origen_lat-1
    olat_2=origen_lat+1
    olng_1=origen_lng-1
    olng_2=origen_lng+1
    aeropuerto_o = om.values(aeropuertos_ord,olat_1,olat_2)
    for omap in lt.iterator(aeropuerto_o):
        listas = om.values(omap,olng_1,olng_2)
        for lista in lt.iterator(listas):
            tamanio = lt.size(lista)
            i=0
            while i<tamanio:
                e = lt.removeLast(lista)
                lt.addLast(aeropuertos_o,e)
                i += 1
    dlat_1=destino_lat-1
    dlat_2=destino_lat+1
    dlng_1=destino_lng-1
    dlng_2=destino_lng+1
    aeropuerto_d=om.values(aeropuertos_ord,dlat_1,dlat_2)
    for omap2 in lt.iterator(aeropuerto_d):
        listas2=om.values(omap2,dlng_1,dlng_2)
        for lista2 in lt.iterator(listas2):
            tamanio=lt.size(lista2)
            j = 0
            while j<tamanio:
                el = lt.removeLast(lista2)
                lt.addLast(aeropuertos_d,el)
                j += 1
    distancias_o= lt.newList()
    for a_o in lt.iterator(aeropuertos_o):
        latitud = float(a_o['Latitude'])
        longitud = float(a_o['Longitude'])
        d = formula(origen_lng,origen_lat,longitud,latitud)
        lt.addLast(distancias_o,d)
    ms.sort(distancias_o,ordenAscendenteD)
    dist_origen=lt.firstElement(distancias_o)
    for a_o in lt.iterator(aeropuertos_o):
        latitud_o=float(a_o['Latitude'])
        longitud_o=float(a_o['Longitude'])
        d_o=formula(origen_lng,origen_lat,longitud_o,latitud_o)
        if d_o==dist_origen:
            aero_o=a_o
            break
    distancias_d = lt.newList()
    for a_d in lt.iterator(aeropuertos_d):
        latitud_d = float(a_d['Latitude'])
        longitud_d = float(a_d['Longitude'])
        dista = formula(destino_lng,destino_lat,longitud_d,latitud_d)
        lt.addLast(distancias_d,dista)
    ms.sort(distancias_d,ordenAscendenteD)
    dist_d = lt.firstElement(distancias_d)
    for a_d in lt.iterator(aeropuertos_d):
        latitud_d = float(a_d['Latitude'])
        longitud_d = float(a_d['Longitude'])
        d_d = formula(destino_lng,destino_lat,longitud_d,latitud_d)
        if d_d == dist_d:
            aero_d = a_d
            break
    k = 0
    while k < 1:
        grafo = catalogo['red']
        IATA_o = aero_o['IATA']
        IATA_d = aero_d['IATA']     
        search = djk.Dijkstra(grafo,IATA_o)
        existspath = djk.hasPathTo(search,IATA_d)
        if existspath:
            camino = djk.pathTo(search,IATA_d)
            latitud_o = float(aero_o['Latitude'])
            longitud_o = float(aero_o['Longitude'])
            latitud_d = float(aero_d['Latitude'])
            longitud_d = float(aero_d['Longitude'])
            dt_o = formula(origen_lng,origen_lat,longitud_o,latitud_o)
            dt_d = formula(destino_lng,destino_lat,longitud_d,latitud_d)
            k += 1
        else:
            o1 = lt.removeFirst(distancias_o)
            o2 = lt.firstElement(distancias_o)
            d1 =lt.removeFirst(distancias_d)
            d2 = lt.firstElement(distancias_d)
            if o2 <= d2:
                for a_o in lt.iterator(aeropuertos_o):
                    latitud_o = float(a_o['Latitude'])
                    longitud_o = float(a_o['Longitude'])
                    d_o=formula(origen_lng,origen_lat,longitud_o,latitud_o)
                    if d_o==o2:
                        aero_o=a_o
                        break
            if d2<o2:
                for a_d in lt.iterator(aeropuertos_d):
                    latitud_d = float(a_d['Latitude'])
                    longitud_d = float(a_d['Longitude'])
                    d_d = formula(destino_lng,destino_lat,longitud_d,latitud_d)
                    if d_d == d2:
                        aero_d = a_d
                        break
    respuesta = lt.newList()
    lt.addLast(respuesta,aero_o)
    lt.addLast(respuesta,aero_d)
    lt.addLast(respuesta,camino)
    lt.addLast(respuesta,dt_o)
    lt.addLast(respuesta,dt_d)
    return respuesta

#R4


#R5
def req5(analyzer,aeropuerto):
    grafo = analyzer['red']
    iatas = gr.adjacents(grafo,aeropuerto)
    aeropuertos = analyzer['aeropuertos']
    resultado = lt.newList()
    lt.addLast(resultado,lt.size(iatas))
    lista = lt.newList()
    for iata in lt.iterator(iatas):
        pareja = mp.get(aeropuertos,iata)
        aeropuerto = me.getValue(pareja)
        lt.addLast(lista,aeropuerto)
    lt.addLast(resultado,lista)
    return resultado