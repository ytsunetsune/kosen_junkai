# -*- coding: utf-8 -*-

import math
import csv
import pandas


def hubeny(p1, p2):
    a2 = 6378137.0 ** 2
    b2 = 6356752.314140 ** 2
    e2 = (a2 - b2) / a2

    def d2r(deg):
        return deg * (2 * math.pi) / 360

    (lon1, lat1, lon2, lat2) = map(d2r, p1 + p2)
    w = 1 - e2 * math.sin((lat1 + lat2) / 2) ** 2
    c2 = math.cos((lat1 + lat2) / 2) ** 2
    return math.sqrt((b2 / w ** 3) * (lat1 - lat2) ** 2 + (a2 / w) * c2 * (lon1 - lon2) ** 2)


class kosen:

    def __init__(self, name, longitude, latitude):
        self.name = name
        self.point = [longitude, latitude]

    def distance_to(self, another_kosen):
        #print self.name, another_kosen.name
        #print self.point, another_kosen.point
        return hubeny(self.point, another_kosen.point)


def read_address_list(filename):
    reader = csv.reader(open(filename, 'r'))
    address_list = []
    for row in reader:
        address_list.append(map(lambda x: x.decode('utf-8'), row))
    return address_list


def load_kosen_data(filename):
    reader = csv.reader(open(filename, 'r'))
    kosen_list = []
    for row in reader:
        print row
        kosen_list.append(kosen(row[0], float(row[1]), float(row[2])))
    return kosen_list


def make_distance_list(kosen_list):
    lst = kosen_list[:]
    distance_list = []
    while(len(lst) > 1):
        route_kosen = lst.pop()
        distance_list.extend(
            map(lambda x: [route_kosen.name, x.name, route_kosen.distance_to(x)], lst))
    return distance_list
