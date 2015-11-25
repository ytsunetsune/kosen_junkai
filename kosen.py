# -*- coding: utf-8 -*-

import math
import csv
from geopy.geocoders import GoogleV3


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


def make_loc_data(address_list):
    geolocator = GoogleV3()
    loc_list = map(lambda x: [x[0], geolocator.geocode(x[1])], address_list)
    return loc_list


def make_kosen_data(loc_list):
    kosen_list = map(lambda x: kosen(x[0], x[1].longitude, x[1].latitude), loc_list)
    return kosen_list


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


def save_distance_list(dlist, filename):
    writer = csv.writer(open(filename, 'w'))
    for row in dlist:
        writer.writerow([row[0].encode('utf-8'), row[1].encode('utf-8'), row[2]])


if __name__ == '__main__':
    add_list = read_address_list("kosen_address.csv")
    print "Getting Location Data..."
    loc_list = make_loc_data(add_list)
    kosen_list = make_kosen_data(loc_list)
    dlist = make_distance_list(kosen_list)
    save_distance_list(dlist, "dlist.csv")

