"""Einstiegspunkt des Prototyps.

Die Klasse erzeugt Ansicht, Speicher und Steuerung, verbindet sie miteinander
und startet den Ablauf. Weil die drei Objekte hier entstehen und an die
Lebensdauer der Application gebunden sind, sind sie im Klassendiagramm als
Kompositionen modelliert; die Steuerung selbst haelt nur Assoziationen.
"""

from datetime import date
from pathlib import Path

from dashboard.darstellung import DashboardAnsicht
from dashboard.fachlogik.studiengang import Studiengang
from dashboard.persistenz import JsonSpeicher
from dashboard.steuerung import StudienDashboard

# Vorgabewerte fuer den ersten Programmstart ohne vorhandene Datendatei.
STANDARD_BEZEICHNUNG = "B.Sc. Cyber Security (Fernstudium)"
STANDARD_STARTDATUM = date(2024, 10, 1)


class Application:
    """Startet den Dashboard-Prototyp."""

    def __init__(self, pfad: Path = Path("studium.json")):
        self._pfad = Path(pfad)

    def main(self) -> None:
        """Erzeugt die Komponenten und uebergibt die Kontrolle an die Steuerung."""
        ansicht, speicher, dashboard = self._komponenten_erzeugen()
        dashboard.starten()

    def _komponenten_erzeugen(self):
        """Erzeugt Ansicht, Speicher und Steuerung und verknuepft sie.

        Liegt noch keine Datendatei vor, wird ein leerer Studiengang mit den
        Zielwerten aus der Konzeptionsphase angelegt und sofort gespeichert.
        """
        ansicht = DashboardAnsicht()
        speicher = JsonSpeicher(self._pfad)

        studiengang = speicher.laden()
        if studiengang is None:
            studiengang = Studiengang(
                bezeichnung=STANDARD_BEZEICHNUNG,
                startdatum=STANDARD_STARTDATUM,
                ziel_dauer_jahre=3,
                ziel_note=2.0,
            )
            speicher.speichern(studiengang)

        dashboard = StudienDashboard(studiengang, speicher, ansicht)
        return ansicht, speicher, dashboard
