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
from DISClib.ADT import map as mp
from DISClib.DataStructures import mapentry as me
from DISClib.Algorithms.Sorting import shellsort as sa
assert cf


def newCatalogo():
    catalogo = {'red': None,
            'aeropuertos': None}

    catalogo['red'] = gr.newGraph(datastructure='ADJ_LIST',directed=True,size=14000,comparefunction=None)
    catalogo['aeropuertos'] = mp.newMap()
    catalogo['ciudades'] = mp.newMap()
    return catalogo


def addAirport(catalogo,airport):
    id=airport['IATA']
    mp.put(catalogo['aeropuertos'],id,airport)
    if not gr.containsVertex(catalogo['red'], id):
        gr.insertVertex(catalogo['red'], id)
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