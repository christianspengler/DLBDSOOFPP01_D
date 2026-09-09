"""Erzeugt die Datendateien aus dem Studienablaufplan B.Sc. Cyber Security.

Das Skript ist ein Hilfsmittel und nicht Teil des Prototyps. Es legt zwei
Dateien an:

    studium.json        alle Module des Ablaufplans, noch ohne Noten
    beispieldaten.json  dieselben Module mit Beispielnoten zur Vorfuehrung

Aufruf im Projektverzeichnis:
    python daten_erzeugen.py
"""

from datetime import date
from pathlib import Path

from dashboard.fachlogik.aufzaehlungen import Pruefungsart as P
from dashboard.fachlogik.modul import Modul
from dashboard.fachlogik.studiengang import Studiengang
from dashboard.persistenz import JsonSpeicher

# Studienbeginn: bitte an den eigenen Studienvertrag anpassen.
STUDIENBEGINN = date(2026, 4, 1)
BEZEICHNUNG = "B.Sc. Cyber Security (Fernstudium)"

# Studienablaufplan im Vollzeitmodell: sechs Semester zu je 30 ECTS.
# (Semester, Kuerzel, Titel, ECTS, vorgesehene Pruefungsform)
ABLAUFPLAN = [
    # 1. Semester
    (1, "DLBIBRVS01", "Betriebssysteme, Rechnernetze und verteilte Systeme", 5, P.KLAUSUR),
    (1, "DLBISIC01", "Einfuehrung in Datenschutz und IT-Sicherheit", 5, P.KLAUSUR),
    (1, "DLBDSIPWP01_D", "Einfuehrung in die Programmierung mit Python", 5, P.KLAUSUR),
    (1, "DLBWIRITT01", "Einfuehrung in das wissenschaftliche Arbeiten fuer IT und Technik", 5, P.ADVANCED_WORKBOOK),
    (1, "DLBDSOOFPP01_D", "Projekt: Objektorientierte und funktionale Programmierung mit Python", 5, P.PORTFOLIO),
    (1, "WPC01", "Wahlpflichtbereich C: Praktikum oder Modul zur Auswahl", 5, None),
    # 2. Semester
    (2, "DLBCSEINF01_D", "Einfuehrung in die Netzwerkforensik", 5, P.KLAUSUR),
    (2, "IMT101", "Mathematik Grundlagen I", 5, P.KLAUSUR),
    (2, "DLBDSSPDS01_D", "Statistik - Wahrscheinlichkeit und deskriptive Statistik", 5, P.KLAUSUR),
    (2, "IREN01", "Requirements Engineering", 5, P.KLAUSUR),
    (2, "DLBDBAPM01", "Projekt: Agiles Projektmanagement", 5, P.PROJEKTBERICHT),
    (2, "WPC02", "Wahlpflichtbereich C: Praktikum oder Modul zur Auswahl", 5, None),
    # 3. Semester
    (3, "DLBCSESPB01_D", "Grundzuege des System-Pentestings", 5, P.KLAUSUR),
    (3, "DLBITIML01", "Theoretische Informatik und Mathematische Logik", 5, P.KLAUSUR),
    (3, "DLBCSEESE01_D", "Social Engineering und Insider Threats", 5, P.FALLSTUDIE),
    (3, "DLBCSEEISC01_D", "Technische und betriebliche IT-Sicherheitskonzeptionen", 5, P.KLAUSUR),
    (3, "DLBCSEESE02_D", "Projekt: Social Engineering", 5, P.PROJEKTPRAESENTATION),
    (3, "WPC03", "Wahlpflichtbereich C: Praktikum oder Modul zur Auswahl", 5, None),
    # 4. Semester
    (4, "DLBCSEDCSW01_D", "DevSecOps und gaengige Software-Schwachstellen", 5, P.HAUSARBEIT),
    (4, "DLBISIC02-01", "Kryptografische Verfahren", 5, P.FALLSTUDIE),
    (4, "DLBCSEHSF01_D", "Host- und Softwareforensik", 5, P.KLAUSUR),
    (4, "DLBCSSCTCS01_D", "Seminar: Aktuelle Themen in Computer Science", 5, P.SEMINARARBEIT),
    (4, "DLBCSEEISC02_D", "Projekt: Einsatz und Konfiguration von SIEM-Systemen", 5, P.PROJEKTBERICHT),
    (4, "WPC04", "Wahlpflichtbereich C: Praktikum oder Modul zur Auswahl", 5, None),
    # 5. Semester
    (5, "DLBCSEEFT01_D", "Threat Modeling", 5, P.KLAUSUR),
    (5, "DLBCSEISS01_D", "Standards der Informationssicherheit", 5, P.FALLSTUDIE),
    (5, "WPA01", "Wahlpflichtbereich A (z. B. Cloud Computing)", 10, None),
    (5, "DLBCSEEFT02_D", "Projekt: Threat Modeling", 5, P.PROJEKTBERICHT),
    (5, "WPC05", "Wahlpflichtbereich C: Praktikum oder Modul zur Auswahl", 5, None),
    # 6. Semester
    (6, "WPB01", "Wahlpflichtbereich B (z. B. Security Controls in the Cloud)", 10, None),
    (6, "DLBMINPAPCC01", "Projekt: Allgemeine Programmierung mit C/C++", 5, P.PORTFOLIO),
    (6, "WPC06", "Wahlpflichtbereich C: Praktikum oder Modul zur Auswahl", 5, None),
    (6, "BBAK01", "Bachelorarbeit", 9, P.BACHELORARBEIT),
    (6, "BBAK02", "Kolloquium", 1, P.KOLLOQUIUM),
]

# Beispielnoten zur Vorfuehrung: Kuerzel -> (Pruefungsdatum, Note)
BEISPIELNOTEN = {
    "DLBIBRVS01": (date(2026, 6, 12), 2.0),
    "DLBISIC01": (date(2026, 6, 26), 1.7),
    "DLBDSIPWP01_D": (date(2026, 7, 10), 1.3),
    "DLBWIRITT01": (date(2026, 7, 24), 2.3),
    "DLBCSEINF01_D": (date(2026, 8, 21), 2.0),
}


def studiengang_aufbauen(mit_noten: bool) -> Studiengang:
    """Legt alle Module des Ablaufplans an, wahlweise mit Beispielnoten."""
    studiengang = Studiengang(BEZEICHNUNG, STUDIENBEGINN, ziel_dauer_jahre=3, ziel_note=2.0)
    for nummer, kuerzel, titel, ects, art in ABLAUFPLAN:
        semester = studiengang.semester_anlegen(nummer)
        modul = Modul(kuerzel, titel, ects)
        semester.modul_zuordnen(modul)
        if mit_noten and kuerzel in BEISPIELNOTEN and art is not None:
            datum, note = BEISPIELNOTEN[kuerzel]
            modul.pruefung_eintragen(art, datum, note)
    return studiengang


if __name__ == "__main__":
    leer = studiengang_aufbauen(mit_noten=False)
    JsonSpeicher(Path("studium.json")).speichern(leer)
    print(f"studium.json       : {len(ABLAUFPLAN)} Module, "
          f"{sum(z[3] for z in ABLAUFPLAN)} ECTS, noch keine Noten")

    beispiel = studiengang_aufbauen(mit_noten=True)
    JsonSpeicher(Path("beispieldaten.json")).speichern(beispiel)
    print(f"beispieldaten.json : {beispiel.erreichte_ects} ECTS erreicht, "
          f"Durchschnitt {beispiel.notendurchschnitt:.2f}")
