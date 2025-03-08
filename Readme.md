README für Application.bat:

Ordnerstruktur:

````
shp2gpkMerge
│
│   Application.bat
│   main.py
│   Readme.md
│   requirements.txt
│
├───data
│       xy.PAR
│       (yx.PRM)
│       yx.SOG
│       yx.TTC
│       yx.dbf
│       yx.prj
│       yx.shp
│       yx.shx
│
└───dist
        main.exe
````

Benutzung:
````
1. Gewünschte Dateien im Ordner "data" platzieren:
  1.1. .PAR Datei
  1.2. .SOG Datei
  1.3. .TTC Datei
  1.4. .dbf Datei
  1.5. .prj Datei
  1.6. .shp Datei
  1.7. .shx Datei
2. Application.bat ausführen
3. Dateien im Ordner "data" austauschen
````
Hinweis: Es kann immer nur ein Geopackage gleichzeitig erstellt werden! Es können zwar mehrere Geopackages im Hauptordner liegen,
allerdings dürfen im "data"-Ordner nicht mehr als 1 Datei von jedem Typ liegen!
