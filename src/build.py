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
                if not 'type' in site:
                    point.style.iconstyle.icon.href = "http://maps.google.com/mapfiles/kml/paddle/ylw-stars.png"
                elif site['type'] == 'tower':
                    point.style.iconstyle.icon.href = "http://maps.google.com/mapfiles/kml/paddle/red-circle.png"
                elif site['type'] == 'pole':
                    point.style.iconstyle.icon.href = "http://maps.google.com/mapfiles/kml/shapes/placemark_circle.png"
                else:
                    point.style.iconstyle.icon.href = "http://maps.google.com/mapfiles/kml/paddle/ylw-stars.png"
        
    kml.save(target + "/radio-mapping.kml")

if __name__ == '__main__':
    main()
