# radio-mapping
Repository of radio site mapping and date with associated transforms.

# Disclaimer
DO NOT RELY ON THIS DATA FOR ANY PURPOSE!  This is a hobbyist project based on public data that may not be current and a good deal of guesswork.

# Building
* git clone https://github.com/balleman/radio-mapping.git
* cd radio-mapping/src
* ./build.py
* load radio-mapping/target/radio-mapping.kmz into Google Earth as a Network Link (allows for refreshing)

# Covered Systems
* PA-STARNET
  ![PA-STARNET P25 Map](/img/pastarnet-p25.jpg?raw=true "PA-STARNET P25 Map")
  ![PA-STARNET Sites Map](/img/pastarnet-sites.jpg?raw=true "PA-STARNET Sites Map")

# Legend
## Sites
* Red Circle Bubble
  * Tower
* Cyan Circle Bubble
  * Tank
* Small Circle
  * Pole
* Small Square
  * Building
* Large Square
  * Regional Operations Center (ROC)
* Huge Square
  * Network Operations Center (NOC)
## Services
### Points
* Target
  * Broadcast Service
### Lines
* Black
  * OPRS Microwave Link
* Green
  * PTC (Turnpike) Microwave Link
* Purple
  * GPU Microwave Link
* Gray
  * OPRS T1 Link
* Blue (thin)
  * OPRS 56k Link
* Light Orange
  * Cumberland County Microwave Link
* Dark Orange
  * ISM Microwave Link
* Yellow Highlight
  * DS3 Capacity or better
* Red Highlight
  * Spread Spectrum
* White (thin)
  * P25 Neighbor Site
### Circles
#### OpenSky
* Purple
  * 800MHz
#### P25
* Green
  * VHF (~ 150 MHz)
* Blue
  * UHF (~ 400 MHz)
* Orange
  * 700 MHz
* Red
  * 800 MHz
