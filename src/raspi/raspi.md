#Raspberry

## Python
## PYTHONPATH
Um es zu vereinfachen die entwickelten Pakete zu nutzen sollte der PYTHONPATH gesetzt werden (Umgebungsvariable)

### Windows
PYTHONPATH=%cd%/acoustic;%cd%/config;%cd%/controlflow;%cd%/lib;%cd%/linedetector;%cd%/movement;%cd%/numberdetector;%cd%/pb;%cd%/webapp

### Mac / Linux
```
CURRENT_LOC=pwd
PYTHONPATH=$CURRENT_LOC/acoustic:$CURRENT_LOC/config:$CURRENT_LOC/controlflow:$CURRENT_LOC/lib:$CURRENT_LOC/linedetector:$CURRENT_LOC/movement:$CURRENT_LOC/numberdetector:$CURRENT_LOC/pb:$CURRENT_LOC/webapp
```

### Raspberry
Auf dem Raspberry wird die Umgebungsvariable durch das run.sh Skript gesetzt.