#!/usr/bin/python

import yaml
import os
import simplekml
from polycircles import polycircles

def get_color_def(color, default):
    if not color:
        return get_color(default)
    else:
        return get_color(color)

def get_color(color):
    if color == "green":
        return simplekml.Color.green
    elif color == "blue":
        return simplekml.Color.blue
    elif color == "red":
        return  simplekml.Color.red
    elif color == "dkred":
        return simplekml.Color.darkred
    elif color == "orange":
        return simplekml.Color.orange
    elif color == "dkorange":
        return simplekml.Color.darkorange
    elif color == "pink":
        return simplekml.Color.deeppink
    elif color == "yellow":
        return simplekml.Color.yellow
    elif color == "black":
        return simplekml.Color.black
    elif color == "gray":
        return simplekml.Color.gray
    elif color == "purple":
        return simplekml.Color.purple
    elif color == "brown":
        return simplekml.Color.saddlebrown
    else:
        return simplekml.Color.beige

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
        for dirname in sorted(dirnames):
            if dirpath in folders:
                fld = folders[dirpath].newfolder(name=dirname)
            else:
                fld = fld_phy.newfolder(name=dirname)
            folders[os.path.join(dirpath, dirname)] = fld 
        for name in sorted(filenames):
            filename = os.path.join(dirpath, name)
            #print(filename)
            if (filename.endswith(".yaml")):
                stream = open(filename, 'r')
                site = yaml.safe_load(stream)
                fld = folders[dirpath]
                point = fld.newpoint(name=site['site'])
                point.description = site['name']
                point.coords = [(site['loc']['lon'], site['loc']['lat'])]
                sites[site['site']] = site
                if "aliases" in site:
                    for alias in site['aliases']:
                        sites[alias] = site
                        point.description += "<br />Alias: " + alias
                if "asrn" in site:
                    point.description += "<br />ASRN: " + str(site['asrn'])
                if not 'type' in site:
                    point.style.iconstyle.icon.href = "http://maps.google.com/mapfiles/kml/paddle/ylw-stars.png"
                elif site['type'] == 'tower':
                    point.style.iconstyle.icon.href = "http://maps.google.com/mapfiles/kml/paddle/red-circle.png"
                elif site['type'] == 'pole':
                    point.style.iconstyle.icon.href = "http://maps.google.com/mapfiles/kml/shapes/placemark_circle.png"
                elif site['type'] == "building":
                    point.style.iconstyle.icon.href = "http://maps.google.com/mapfiles/kml/shapes/placemark_square.png"
                elif site['type'] == "tank":
                    point.style.iconstyle.icon.href = "http://maps.google.com/mapfiles/kml/paddle/ltblu-circle.png"
                else:
                    point.style.iconstyle.icon.href = "http://maps.google.com/mapfiles/kml/paddle/ylw-stars.png"
    
    fld_svc = kml.newfolder(name="Services")
    service_path = "../data/service"
    for (dirpath, dirnames, filenames) in os.walk(service_path):
        for dirname in sorted(dirnames):
            if dirpath in folders:
                fld = folders[dirpath].newfolder(name=dirname)
            else:
                fld = fld_svc.newfolder(name=dirname)
            folders[os.path.join(dirpath, dirname)] = fld 
        for name in sorted(filenames):
            filename = os.path.join(dirpath, name)
            fld = folders[dirpath]
            if filename.endswith("/folder.yaml"):
                stream = open(filename, 'r')
                fldopts = yaml.safe_load(stream)
                if "hidden" in fldopts:
                    if fldopts['hidden']:
                        fld.visibility = 0
            elif filename.endswith(".yaml"):
                #print(filename)
                stream = open(filename, 'r')
                svcs = yaml.safe_load_all(stream)
                for svc in svcs:                    
                    if "type" not in svc:
                        fld_this = fld.newfolder(name=svc['service'])
                        point = fld_this.newpoint(name=svc['service'])
                        point.description = svc['service']
                        site = sites[svc['site']]
                        point.coords = [(site['loc']['lon'], site['loc']['lat'])]
                        point.style.iconstyle.icon.href = "http://maps.google.com/mapfiles/kml/shapes/target.png"
                        point.style.iconstyle.scale = 2                        
                        if "callsign" in svc:
                            point.description += "<br />Callsign: " + str(svc['callsign'])
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
                                polygon.style.polystyle.color = simplekml.Color.changealphaint(100, get_color("green"))
                            else:
                                polygon.style.polystyle.color = simplekml.Color.changealphaint(100,get_color_def(svc["color"], "green"))
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
                            line.style.linestyle.width = 4
                        elif svc["class"] == "minor":
                            line.style.linestyle.width = 1
                        if "color" not in svc:
                            line.style.linestyle.color = get_color("yellow")
                        else:
                            line.style.linestyle.color = get_color(svc["color"])
                        if "highlight" in svc:
                            line1 = fld.newlinestring(name=svc['service']+"_hl")
                            line1.coords = [(site0['loc']['lon'], site0['loc']['lat']), (site1['loc']['lon'], site1['loc']['lat'])]
                            line1.extrude = 1
                            line1.style.linestyle.width = 6
                            line1.style.linestyle.color = simplekml.Color.changealphaint(150, get_color(svc['highlight']))
                            line.style.linestyle.width = 2
                    elif svc['type'] == "noc":
                        fld_this = fld.newfolder(name=svc['service'])
                        point = fld_this.newpoint(name=svc['service'])
                        point.description = svc['service']
                        site = sites[svc['site']]
                        point.coords = [(site['loc']['lon'], site['loc']['lat'])]
                        point.style.iconstyle.icon.href = "http://maps.google.com/mapfiles/kml/shapes/square.png"
                        point.style.iconstyle.scale = 3      
                    elif svc['type'] == "roc":
                        fld_this = fld.newfolder(name=svc['service'])
                        point = fld_this.newpoint(name=svc['service'])
                        point.description = svc['service']
                        site = sites[svc['site']]
                        point.coords = [(site['loc']['lon'], site['loc']['lat'])]
                        point.style.iconstyle.icon.href = "http://maps.google.com/mapfiles/kml/shapes/square.png"
                        point.style.iconstyle.scale = 2
                        
    for folder in folders.values():
        if folder.visibility == 0:
            for geo in folder.allgeometries:
                geo.visibility = 0
            
                        
    kml.savekmz(target + "/radio-mapping.kmz", format=False)

if __name__ == '__main__':
    main()
