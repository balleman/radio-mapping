#!/usr/bin/python

import yaml
import os
import simplekml
from polycircles import polycircles

def main():
    target = "../target"
    if (not os.path.isdir(target)):
        os.mkdir("../target")
    
    kml = simplekml.Kml(open=1)
    kml.document.name = "Radio Mapping"
    
    fld_phy = kml.newfolder(name="Physical Sites")
    folders = dict()
    sites = dict()
    miles_to_meters = 1609.344
                
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
                if "aliases" in site:
                    for alias in site['aliases']:
                        sites[alias] = site
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
                svcs = yaml.safe_load_all(stream)
                for svc in svcs:
                    fld = folders[dirpath]
                    if "type" not in svc:
                        fld_this = fld.newfolder(name=svc['service'])
                        point = fld_this.newpoint(name=svc['service'])
                        point.description = svc['service']
                        site = sites[svc['site']]
                        point.coords = [(site['loc']['lon'], site['loc']['lat'])]
                        point.style.iconstyle.icon.href = "http://maps.google.com/mapfiles/kml/shapes/target.png"
                        point.style.iconstyle.scale = 2                        
                        if "callsign" in svc:
                            point.description += "<br />Callsign: " + svc['callsign']
                        if "p25" in svc:
                            p25 = svc['p25']
                            if "nac" in p25:
                                point.description += "<br />P25 NAC: " + str(p25['nac'])
                            if "rfss" in p25:
                                point.description += "<br />P25 RFSS: " + str(p25['rfss'])
                            if "site" in p25:
                                point.description += "<br />P25 Site: " + str(p25['site'])
                        if "range" in svc:
                            polycircle = polycircles.Polycircle(latitude=site['loc']['lat'],
                                                               longitude=site['loc']['lon'],
                                                               radius=svc['range']*miles_to_meters,
                                                               number_of_vertices=36)
                            polygon = fld_this.newpolygon(name=svc['service'] + " Range",
                                                          outerboundaryis=polycircle.to_kml())
                            if "color" not in svc:
                                polygon.style.polystyle.color = simplekml.Color.changealphaint(100, simplekml.Color.green)
                            elif svc["color"] == "blue":
                                polygon.style.polystyle.color = simplekml.Color.changealphaint(100, simplekml.Color.blue)
                            elif svc["color"] == "red":
                                polygon.style.polystyle.color = simplekml.Color.changealphaint(100, simplekml.Color.red)
                        if "adjacent" in svc:
                            fld_adj = fld_this.newfolder(name="Adjacent Sites")
                            for adj in svc['adjacent']:
                                line = fld_adj.newlinestring(name=svc['service'] + "-" + adj)
                                site0 = site
                                site1 = sites[adj]
                                line.coords = [(site0['loc']['lon'], site0['loc']['lat']), (site1['loc']['lon'], site1['loc']['lat'])]
                                line.extrude = 1
                                line.style.linestyle.color = simplekml.Color.beige
                                
                                                            
                    elif svc['type'] == "link":
                        line = fld.newlinestring(name=svc['service'])
                        site0 = sites[svc['site']]
                        site1 = sites[svc['dest']]
                        line.coords = [(site0['loc']['lon'], site0['loc']['lat']), (site1['loc']['lon'], site1['loc']['lat'])]
                        line.extrude = 1
                        if "class" not in svc or svc["class"] == "major":
                            line.style.linestyle.width = 3
                        elif svc["class"] == "minor":
                            line.style.linestyle.width = 1
                        line.style.linestyle.color = simplekml.Color.yellow
                    
        
    kml.save(target + "/radio-mapping.kml")

if __name__ == '__main__':
    main()
