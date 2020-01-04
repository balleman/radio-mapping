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
    sites = dict()
                
    site_path = "../data/site"
    for (dirpath, dirnames, filenames) in os.walk(site_path):
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
                sites[site['site']] = site
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
    
    fld_svc = kml.newfolder(name="Services")
    service_path = "../data/service"
    for (dirpath, dirnames, filenames) in os.walk(service_path):
        for dirname in dirnames:
            if dirpath in folders:
                fld = folders[dirpath].newfolder(name=dirname)
            else:
                fld = fld_svc.newfolder(name=dirname)
            folders[os.path.join(dirpath, dirname)] = fld 
        for name in filenames:
            filename = os.path.join(dirpath, name)
            if (filename.endswith(".yaml")):
                stream = open(filename, 'r')
                svc = yaml.safe_load(stream)
                fld = folders[dirpath]
                if "type" not in svc:
                    point = fld.newpoint(name=svc['service'])
                    point.description = svc['service']
                    if "callsign" in svc:
                        site = sites[svc['site']]
                        point.coords = [(site['loc']['lon'], site['loc']['lat'])]
                        point.description += "<br />Callsign: " + svc['callsign']
                        point.style.iconstyle.icon.href = "http://maps.google.com/mapfiles/kml/shapes/target.png"
                        point.style.iconstyle.scale = 2                                      
                elif svc['type'] == "link":
                    line = fld.newlinestring(name=svc['service'])
                    site0 = sites[svc['site']]
                    site1 = sites[svc['dest']]
                    line.coords = [(site0['loc']['lon'], site0['loc']['lat']), (site1['loc']['lon'], site1['loc']['lat'])]
                    line.extrude = 1
                    line.style.linestyle.width = 3
                    line.style.linestyle.color = simplekml.Color.yellow
                    
        
    kml.save(target + "/radio-mapping.kml")

if __name__ == '__main__':
    main()
