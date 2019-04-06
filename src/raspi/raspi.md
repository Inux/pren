#Raspberry

## Python
## Python Abhängigkeiten
Alle Python Abhängigkeiten müssen im requirements.txt angegeben werden!
Somit können diese einfach installiert werden (siehe setup.sh).

## PYTHONPATH
Um es zu vereinfachen die entwickelten Pakete zu nutzen sollte der PYTHONPATH gesetzt werden (Umgebungsvariable)

### Windows
PYTHONPATH=%cd%/..;$cd%/../..;%cd%/acoustic;%cd%/config;%cd%/controlflow;%cd%/lib;%cd%/linedetector;%cd%/movement;%cd%/numberdetector;%cd%/pb;%cd%/webapp

### Mac / Linux
```
CURRENT_LOC=pwd
PARENT_LOC=$(pwd)"/.."
PARENT_PARENT_LOC=$(pwd)"/../.."
PYTHONPATH=$CURRENT_LOC/acoustic:$CURRENT_LOC/config:$CURRENT_LOC/controlflow:$CURRENT_LOC/lib:$CURRENT_LOC/linedetector:$CURRENT_LOC/movement:$CURRENT_LOC/numberdetector:$CURRENT_LOC/pb:$CURRENT_LOC/webapp:$PARENT_LOC:$PARENT_PARENT_LOC:$CURRENT_LOC:$PYTHONPATH
```

### Raspberry
Auf dem Raspberry wird die Umgebungsvariable durch das run_master.sh oder run_slave.sh Skript gesetzt.
