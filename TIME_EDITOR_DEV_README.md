# Readme Time Editor Q-GIS Plugin

## Übersetzungen 

Die TS-Datei wird über `update_translations.sh` erzeugt, die Kompilierung in 
eine `.qm` Datei erfolgt mit `pb_tool translate`. Alle neuen Dateien oder 
Pfad-Änderungen müssen in die Datei `time_editor.pro` eingetragen werden.

## TODOS

### GENERAL 

- Umgang mit Datum, '??' insbesondere negative Werte
- Überführung in Panel?
- Spatial integrity check 
- First Setup Wizard?

### Einzelaspekte 

- Warne wenn Time-Expand mehrere Poygone mit unterschiedlichen Time-spans geht
- Warne, wenn Time-Expand über die Grenze geht (z.B. eines adjacents polygon)
- Soll eine Funktion existieren, die Grenzanpassungen auf andere betroffene Polygone überträgt
    (sehr kompliziert)?

## UI Widgets 

### Core 

#### Zu erledigen

- Leiste/Input/Dropdown Widget zur automatischen Anwendung eines Filters auf die Attribut Tabelle
- Button um Aktiven Filter zu entfernen?

#### Implementiert 

- Split Action (über Menü und Shortcut) -> Abfrage eines Wertes um mehrere Features zu duplizieren, die Zeitwerte anzupassen und die neuen Features zum Editieren auszuwählen
- Life-Span Expand eines (oder mehrerer?) Feature -> Auswahl (dropdown start/end) und neuer zeitwert, vorher/nacher betroffenes polygon Attributwert wird ebenfalls angepasst
- Funktion zum Verifzieren des Gesamten Layers 


### Bonus 

- Stats

## Use Cases 

### Bekannte Geometrie, unbekannter Anfang Ende 

Über eine Karte, Zeichnung o.ä. kann eine Gemarkung angepasst werden. Häufig wird es dafür kein konkretes Datum geben, man wird auf educated guesses angewiesen sein. Generell sollte 
jedoch ein Komplettes Datum erforderlich sein. Unbekannte Tages und Monatsangaben können 
mit ?? ersetzt werden, z.B. 1954-??-??

# Anpassung des Lebenszeitraums einer Geometrie (z.B. Anhand Erlass, Modernerer Zeichnung o.ä.)


## QGIS Usage 

Am besten eine Label Rule anlegen, um sicher zu gehen, dass man das richtige Feature 
zum Editieren erwischt: 
~~~js
gemarkung + '(' + life_start + ' => ' + life_end + ')'
~~~