#!/usr/bin/python

import fileinput
import re

def process(line):
    if re.match("\\s*\\d+-\\d+-[\\d.]+ (N|S), \\d+-\\d+-[\\d.]+ (E|W)\\s*", line):
        dms(line)
    else:
        print("Format unrecognized.")

def dms(line):
    parts = re.split("[-, ]+", line.strip())
    #for x in range(len(parts)):
    #    print(str(x) + "=" + parts[x]) 
    lat = int(parts[0]) + float(parts[1])/60 + float(parts[2])/3600
    if parts[3] == "S":
        lat = lat * -1
    lon = int(parts[4]) + float(parts[5])/60 + float(parts[6])/3600
    if parts[7] == "W":
        lon = lon * -1
    print(str(lat) + " " + str(lon))

for line in fileinput.input():
    process(line)
