# Studien-Dashboard

Prototyp eines Dashboards zur Überwachung des eigenen Studienfortschritts.
Portfolio im Kurs *Objektorientierte und funktionale Programmierung mit Python*
(DLBDSOOFPP01_D), IU Internationale Hochschule.

## Überwachte Ziele

1. Abschluss des Studiums innerhalb von drei Jahren (180 ECTS in 36 Monaten)
2. Abschluss mit einem Notendurchschnitt von 2,0 oder besser

Zu beiden Zielen zeigt das Dashboard den Ist-Wert, die Abweichung vom
notwendigen Zwischenstand und eine Prognose des Zielzustands.

## Schnellstart

```
python main.py
```

Es werden ausschließlich Module der Python-Standardbibliothek verwendet, eine
Installation zusätzlicher Pakete ist nicht erforderlich. Voraussetzung ist
Python 3.10 oder neuer (entwickelt und getestet mit 3.13).

## Bedienung

| Eingabe | Wirkung |
|---------|---------|
| `1`     | Modul anlegen (Semester, Kürzel, Titel, ECTS) |
| `2`     | Note eintragen (Kürzel, Prüfungsart, Datum, Note) |
| `q`     | Programm beenden |

## Aufbau des Quellcodes

```
main.py                             Startskript
dashboard/application.py            erzeugt und verbindet die Komponenten
dashboard/steuerung.py              StudienDashboard: Ablauf und Menü
dashboard/darstellung.py            DashboardAnsicht: Textausgabe und Eingaben
dashboard/persistenz.py             JsonSpeicher: Lesen und Schreiben der Datei
dashboard/fachlogik/                fachliche Klassen und Aufzählungstypen
tests/test_dashboard.py             automatisierte Tests
daten_erzeugen.py                   Hilfsskript: erzeugt die Datendateien
studium.json                        alle Module des Studienablaufplans
beispieldaten.json                  dieselben Module mit Beispielnoten
```

Die Struktur folgt der Gesamtarchitektur aus Phase 2: Die fachlichen Klassen
kennen weder Bildschirmausgabe noch Datei, die Abhängigkeiten verlaufen
ausschließlich von außen nach innen.

## Tests

```
python -m unittest discover -s tests -v
```

Geprüft werden die Datumsrechnung, der abgeleitete Modulstatus, die nach ECTS
gewichtete Durchschnittsberechnung sowie der vollständige Weg vom Objektbaum in
die JSON-Datei und zurück.

## Daten

Alle Daten liegen im Klartext als JSON vor. Mitgeliefert werden zwei Dateien:

* `studium.json` enthält alle 34 Module des Studienablaufplans B.Sc. Cyber
  Security (sechs Semester, 180 ECTS), noch ohne Noten. Diese Datei wird beim
  Start ohne Argument verwendet und ist für den eigenen Gebrauch gedacht: Noten
  werden über den Menüpunkt `2` eingetragen.
* `beispieldaten.json` enthält dieselben Module mit fünf Beispielnoten, damit
  das Dashboard sofort einen gefüllten Stand zeigt:

  ```
  python main.py beispieldaten.json
  ```

Beide Dateien lassen sich mit `python daten_erzeugen.py` neu erzeugen. Der
Studienbeginn ist dort als Konstante `STUDIENBEGINN` hinterlegt und an den
eigenen Studienvertrag anzupassen. Wird `studium.json` gelöscht, legt der
Prototyp beim nächsten Start einen leeren Studiengang an.
