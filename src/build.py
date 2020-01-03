#!/usr/bin/python

import yaml
import os
import simplekml

def main():
    target = "../target"
    if (not os.path.isdir(target)):
        os.mkdir("../target")
    
    kml = simplekml.Kml(open=1)
    kml.document.name = "radio-mapping"
                
    sites = "../data/site"
    for (dirpath, dirnames, filenames) in os.walk(sites):
        for name in filenames:
            filename = os.path.join(dirpath, name)
            stream = open(filename, 'r')
            site = yaml.safe_load(stream)
            point = kml.newpoint(name=site['site'])
            point.description = site['name']
            point.coords = [(site['loc']['lon'], site['loc']['lat'])]
        
    kml.save(target + "/radio-mapping.kml")

if __name__ == '__main__':
    main()
