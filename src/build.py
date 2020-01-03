#!/usr/bin/python

import yaml
import os
from lxml import etree
from pykml.factory import KML_ElementMaker as KML
from pykml.factory import ATOM_ElementMaker as ATOM
from pykml.factory import GX_ElementMaker as GX
from youtube_dl.extractor import streamable

def main():
    target = "../target"
    if (not os.path.isdir(target)):
        os.mkdir("../target")
    
    kml = KML.kml()
                
    sites = "../data/site"
    for (dirpath, dirnames, filenames) in os.walk(sites):
        for name in filenames:
            filename = os.path.join(dirpath, name)
            stream = open(filename, 'r')
            site = yaml.safe_load(stream)
            placemark = KML.Placemark(
                KML.name(site['site']),
                KML.description(site['name']),
                KML.Point(
                    KML.coordinates("{lon},{lat}".format(lon=site['loc']['lon'], lat=site['loc']['lat']))
                    )
                )
            kml.append(placemark)
        
    doc = KML.kml(
        etree.Comment(' required when using gx-prefixed elements '),
        KML.Placemark(
            KML.name('gx:altitudeMode Example'),
            KML.Point(
                KML.coordinates("-77, 40")
            )
        ),
    )
    etree.ElementTree(kml).write(target + "/radio-mapping.kml", pretty_print=True)

if __name__ == '__main__':
    main()
