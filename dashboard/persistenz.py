"""Persistenz des Studiengangs in einer JSON-Datei.

Die Umwandlung liegt vollstaendig in dieser Klasse, damit die fachlichen
Klassen nicht wissen muessen, in welcher Form sie abgelegt werden (siehe
Phase 2, Kapitel 2.2). Datumswerte werden als Zeichenkette nach ISO 8601
abgelegt, Aufzaehlungswerte ueber ihren zugewiesenen Wert.
"""

import json
from datetime import date
from pathlib import Path

from dashboard.fachlogik.aufzaehlungen import Pruefungsart
from dashboard.fachlogik.modul import Modul
from dashboard.fachlogik.studiengang import Studiengang


class JsonSpeicher:
    """Liest und schreibt den gesamten Objektbaum als JSON-Datei."""

    def __init__(self, pfad: Path):
        self._pfad = Path(pfad)

    @property
    def pfad(self) -> Path:
        return self._pfad

    # --- oeffentliche Schnittstelle --------------------------------------
    def laden(self) -> Studiengang | None:
        """Liest die Datei ein; None, wenn noch keine Datei vorhanden ist."""
        if not self._pfad.exists():
            return None
        with open(self._pfad, encoding="utf-8") as datei:
            daten = json.load(datei)
        return self._aus_dict(daten)

    def speichern(self, studiengang: Studiengang) -> None:
        """Schreibt den Studiengang vollstaendig in die Datei."""
        with open(self._pfad, "w", encoding="utf-8") as datei:
            json.dump(self._als_dict(studiengang), datei,
                      ensure_ascii=False, indent=2)

    # --- Umwandlung in die Speicherform ----------------------------------
    def _als_dict(self, studiengang: Studiengang) -> dict:
        return {
            "bezeichnung": studiengang.bezeichnung,
            "startdatum": studiengang.startdatum.isoformat(),
            "ziel_dauer_jahre": studiengang.ziel_dauer_jahre,
            "ziel_note": studiengang.ziel_note,
            "semester": [
                {
                    "nummer": semester.nummer,
                    "beginn": semester.beginn.isoformat(),
                    "ende": semester.ende.isoformat(),
                    "module": [
                        {
                            "kuerzel": modul.kuerzel,
                            "titel": modul.titel,
                            "ects": modul.ects,
                            "pruefungen": [
                                {
                                    # Enum wird ueber seinen Wert abgelegt
                                    "art": pruefung.art.value,
                                    "versuch": pruefung.versuch,
                                    "datum": pruefung.datum.isoformat(),
                                    "note": pruefung.note,
                                }
                                for pruefung in modul.pruefungen
                            ],
                        }
                        for modul in semester.module
                    ],
                }
                for semester in studiengang.semester
            ],
        }

    # --- Umwandlung zurueck in Objekte -----------------------------------
    def _aus_dict(self, daten: dict) -> Studiengang:
        """Erzeugt die Objekte von aussen nach innen.

        Die Reihenfolge Studiengang, Semester, Modul, Pruefungsleistung stellt
        sicher, dass jedes Teil unmittelbar seinem Ganzen zugeordnet wird.
        """
        studiengang = Studiengang(
            bezeichnung=daten["bezeichnung"],
            startdatum=date.fromisoformat(daten["startdatum"]),
            ziel_dauer_jahre=daten.get("ziel_dauer_jahre", 3),
            ziel_note=daten.get("ziel_note", 2.0),
        )
        for semester_daten in daten.get("semester", []):
            semester = studiengang.semester_anlegen(semester_daten["nummer"])
            for modul_daten in semester_daten.get("module", []):
                modul = Modul(modul_daten["kuerzel"], modul_daten["titel"],
                              modul_daten["ects"])
                semester.modul_zuordnen(modul)
                for pruefung_daten in modul_daten.get("pruefungen", []):
                    modul.pruefung_eintragen(
                        Pruefungsart(pruefung_daten["art"]),
                        date.fromisoformat(pruefung_daten["datum"]),
                        pruefung_daten["note"],
                    )
        return studiengang
