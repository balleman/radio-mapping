#!/usr/bin/python

import yaml
import os
import simplekml

def main():
    target = "../target"
    if (not os.path.isdir(target)):
        os.mkdir("../target")
    
    kml = simplekml.Kml(open=1)
    kml.document.name = "Radio Mapping"
    
    fld_phy = kml.newfolder(name="Physical Sites")
    folders = dict()
                
    sites = "../data/site"
    for (dirpath, dirnames, filenames) in os.walk(sites):
        for dirname in dirnames:
            if dirpath in folders:
                fld = folders[dirpath].newfolder(name=dirname)
            else:
                fld = fld_phy.newfolder(name=dirname)
            folders[os.path.join(dirpath, dirname)] = fld 
        for name in filenames:
            filename = os.path.join(dirpath, name)
            if (filename.endswith(".yaml")):
                stream = open(filename, 'r')
                site = yaml.safe_load(stream)
                fld = folders[dirpath]
                point = fld.newpoint(name=site['site'])
                point.description = site['name']
                point.coords = [(site['loc']['lon'], site['loc']['lat'])]
        
    kml.save(target + "/radio-mapping.kml")

if __name__ == '__main__':
    main()
