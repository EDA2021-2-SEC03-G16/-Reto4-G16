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


import config as cf
from DISClib.ADT import list as lt
from DISClib.ADT.graph import gr
from DISClib.ADT import orderedmap as om
from DISClib.Algorithms.Graphs import scc
from DISClib.Algorithms.Sorting import mergesort as ms
from DISClib.ADT import map as mp
from DISClib.DataStructures import mapentry as me
from DISClib.Algorithms.Sorting import shellsort as sa
assert cf


def newCatalogo():
    catalogo = {'red': None,
            'aeropuertos': None}

    catalogo['red'] = gr.newGraph(datastructure='ADJ_LIST',directed=True,size=14000,comparefunction=None)
    catalogo['blue']=['blue'] = gr.newGraph(datastructure='ADJ_LIST',directed=False,size=14000, comparefunction=None)
    catalogo['aeropuertos'] = mp.newMap()
    catalogo['ciudades'] = mp.newMap()
    return catalogo


def addAirport(catalogo,airport):
    id=airport['IATA']
    mp.put(catalogo['aeropuertos'],id,airport)
    if not gr.containsVertex(catalogo['red'], id):
        gr.insertVertex(catalogo['red'], id)
        ordmap = catalogo['latlng']
    latitud = float(airport['Latitude'])
    longitud = float(airport['Longitude'])
    existid=om.contains(ordmap,latitud)
    if existid:
        pareja = om.get(ordmap,latitud)
        ordmap2 = me.getValue(pareja)
        existlongitud = om.contains(ordmap2,longitud)
        if existlongitud:
            pareja2 = om.get(ordmap2,longitud)
            lista = me.getValue(pareja2)
        else:
            lista = lt.newList()
        lt.addLast(lista,airport)
        om.put(ordmap2,longitud,lista)
    else:
        ordmap2 = om.newMap()
        lista = lt.newList()
        lt.addLast(lista,airport)
        om.put(ordmap2,longitud,lista)
        om.put(ordmap,latitud,ordmap2)
    return catalogo


def addRoute(catalogo, route):
    origen=route['Departure']
    destino=route['Destination']
    distancia=route['distance_km']
    edge=gr.getEdge(catalogo['red'], origen, destino)
    if edge is None:
        gr.addEdge(catalogo['red'], origen, destino, distancia)
    return catalogo


def addCity(catalogo, city):
    ciudad=city['city']
    mp.put(catalogo['ciudades'],ciudad,city)
    return catalogo


def addRoute2(catalogo, ruta):
    origen=ruta['Departure']
    destino=ruta['Destination']
    distancia=ruta['distance_km']
    red=catalogo["red"]
    edge=gr.getEdge(red, destino, origen)
    if edge is not None:
        if gr.containsVertex(catalogo["blue"], destino) is False:
            gr.insertVertex(catalogo["blue"], destino)
        if gr.containsVertex(catalogo["blue"], origen) is False:
            gr.insertVertex(catalogo["blue"], origen)
        gr.addEdge(catalogo["blue"], destino, origen, distancia)
    return catalogo


def ordenarAscendente(a,b):
    if (a > b):
        return 0
    return -1


def Req1(catalogo):
    grafo=catalogo['red']
    aeropuertos=gr.vertices(grafo)
    conexiones=lt.newList()
    for aeropuerto in lt.iterator(aeropuertos):
        num=gr.degree(grafo,aeropuerto)
        if num>200:
            lt.addLast(conexiones,num)
    ms.sort(conexiones,ordenarAscendente)
    a = lt.lastElement(conexiones)
    maximo = lt.newList()
    for aeropuerto in lt.iterator(aeropuertos):
        b = gr.degree(grafo,aeropuerto)
        if int(a) == int(b):
            lt.addLast(maximo,aeropuerto)
    mapa = catalogo['aeropuertos']
    resultado = lt.newList('ARRAY_LIST')
    for id in lt.iterator(maximo):
        pareja = mp.get(mapa,id)
        valor = me.getValue(pareja)
        lt.addLast(resultado,valor)
    lt.addLast(resultado,b)
    return resultado


def req2(catalogo, I1, I2):
    catalogo["components"] = scc.KosarajuSCC(catalogo["red"])
    existe=scc.stronglyConnected(catalogo["components"], I1, I2)
    total=scc.connectedComponents(catalogo["components"])
    return existe, total