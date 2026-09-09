"""Aufzaehlungstypen der fachlichen Klassen.

Beide Typen begrenzen den Wertebereich der zugehoerigen Attribute. Ein
unbekannter Wert loest beim Erzeugen einen ValueError aus, wodurch fehlerhafte
Eingaben frueh auffallen. Der zugewiesene Zeichenkettenwert wird zugleich fuer
die Speicherung in der JSON-Datei und fuer die Anzeige verwendet.
"""

from enum import Enum


class Status(Enum):
    """Bearbeitungsstand eines Moduls.

    Der Status wird nicht gespeichert, sondern in Modul.status aus den
    zugeordneten Pruefungsleistungen abgeleitet (siehe Phase 2, Kapitel 1.2).
    """

    OFFEN = "offen"
    IN_BEARBEITUNG = "in Bearbeitung"
    BESTANDEN = "bestanden"


class Pruefungsart(Enum):
    """Form einer Pruefungsleistung.

    Die Werte entsprechen den Pruefungsformen des Studienablaufplans
    B.Sc. Cyber Security. Weitere Formen lassen sich ergaenzen, ohne dass
    bestehende Klassen zu aendern sind.
    """

    KLAUSUR = "Klausur"
    PORTFOLIO = "Portfolio"
    PROJEKTBERICHT = "Projektbericht"
    ADVANCED_WORKBOOK = "Advanced Workbook"
    FALLSTUDIE = "Fallstudie"
    HAUSARBEIT = "Hausarbeit"
    SEMINARARBEIT = "Seminararbeit"
    PROJEKTPRAESENTATION = "Projektpraesentation"
    PRAXISREFLEXION = "Praxisreflexion"
    BACHELORARBEIT = "Bachelorarbeit"
    KOLLOQUIUM = "Kolloquium"
