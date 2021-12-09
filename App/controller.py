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
 """

import config as cf
import model as m
import csv


def initCatalog():
    catalogo=m.newCatalogo()
    return catalogo


def loadData(catalogo):
    loadAirports(catalogo)
    loadRoutes(catalogo)
    loadCities(catalogo)
    loadRoutes(catalogo)
    return catalogo

def loadAirports(catalogo):
    booksfile = cf.data_dir + 'airports_full.csv'
    input_file = csv.DictReader(open(booksfile, encoding='utf-8'))
    for airport in input_file:
        m.addAirport(catalogo, airport)
    
def loadRoutes(catalogo):
    booksfile = cf.data_dir + 'routes_full.csv'
    input_file = csv.DictReader(open(booksfile, encoding='utf-8'))
    for route in input_file:
        m.addRoute(catalogo, route)

def loadCities(catalogo):
    booksfile = cf.data_dir + 'worldcities.csv'
    input_file = csv.DictReader(open(booksfile, encoding='utf-8'))
    for city in input_file:
        m.addCity(catalogo, city)

def loadRoutesCompleto(catalogo):
    booksfile = cf.data_dir + 'routes_full.csv'
    input_file = csv.DictReader(open(booksfile, encoding='utf-8'))
    for route in input_file:
        m.addRouteCompleto(catalogo, route)


def Req1(catalogo):
    return m.Req1(catalogo)


def Req3(catalogo,origen,destino):
    return m.req3(catalogo,origen,destino)

def Req5(catalogo,aeropuerto):
    return m.req5(catalogo,aeropuerto)