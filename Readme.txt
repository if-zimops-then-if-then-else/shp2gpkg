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

1. Gewünschte Dateien im Ordner "data" platzieren:
   2. .PAR Datei
   3. .SOG Datei
   4. .TTC Datei
   5. .dbf Datei
   6. .prj Datei
   7. .shp Datei
   8. .shx Datei
2. Application.bat ausführen
3. Dateien im Ordner "data" austauschen

Hinweis: Es kann immer nur ein Geopackage gleichzeitig erstellt werden! Es können zwar mehrere Geopackages im Hauptordner liegen,
allerdings dürfen im "data"-Ordner nicht mehr als 1 Datei von jedem Typ liegen!