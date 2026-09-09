"""Textausgabe des Dashboards auf der Kommandozeile.

Die Klasse enthaelt keine fachlichen Berechnungen. Sie liest ausschliesslich
Eigenschaften des Studiengangs und formatiert sie. Verwendet werden nur
ASCII-Zeichen, damit die Darstellung unabhaengig von der eingestellten
Codepage der Konsole identisch bleibt (siehe Phase 1, Kapitel 2).
"""

import os

from dashboard.fachlogik.studiengang import GESAMT_ECTS, Studiengang

MONATSNAMEN_FORMAT = "%m/%Y"


class DashboardAnsicht:
    """Erzeugt die Bildschirmausgabe und nimmt Eingaben entgegen."""

    def __init__(self, breite: int = 80):
        self._breite = breite

    # --- Hilfsmittel der Darstellung -------------------------------------
    def _balken(self, anteil: float, laenge: int = 32) -> str:
        """Erzeugt einen Fortschrittsbalken aus ASCII-Zeichen.

        Der Anteil wird auf 0 bis 1 begrenzt, damit ein Wert ueber 100 Prozent
        den Balken nicht ueberlaufen laesst.
        """
        anteil = max(0.0, min(1.0, anteil))
        gefuellt = round(anteil * laenge)
        return "[" + "#" * gefuellt + "-" * (laenge - gefuellt) + "]"

    def _zahl(self, wert: float, stellen: int = 1) -> str:
        """Formatiert eine Zahl mit deutschem Dezimalkomma."""
        return f"{wert:.{stellen}f}".replace(".", ",")

    def _trennlinie(self) -> None:
        print("  " + "-" * (self._breite - 4))

    def bildschirm_leeren(self) -> None:
        """Leert die Konsole; cls unter Windows, clear unter Linux und macOS."""
        os.system("cls" if os.name == "nt" else "clear")

    # --- oeffentliche Schnittstelle --------------------------------------
    def zeige(self, studiengang: Studiengang) -> None:
        """Gibt das vollstaendige Dashboard aus."""
        self.bildschirm_leeren()
        self._kopf(studiengang)
        self._trennlinie()
        self._ziel_studiendauer(studiengang)
        self._trennlinie()
        self._ziel_notendurchschnitt(studiengang)
        self._trennlinie()
        self._menuezeile()

    def frage(self, text: str) -> str:
        """Nimmt eine Eingabe entgegen und entfernt umgebende Leerzeichen."""
        return input(text).strip()

    def meldung(self, text: str) -> None:
        """Gibt eine Rueckmeldung aus und wartet auf eine Bestaetigung."""
        print("\n  " + text)
        input("  Weiter mit Enter ...")

    # --- einzelne Bloecke -------------------------------------------------
    def _kopf(self, studiengang: Studiengang) -> None:
        from datetime import date
        print()
        print(f"  STUDIEN-DASHBOARD   {studiengang.bezeichnung}")
        print(f"  Stand: {date.today().strftime('%d.%m.%Y')}   "
              f"Studienbeginn: {studiengang.startdatum.strftime('%d.%m.%Y')}   "
              f"Monat {studiengang.verstrichene_monate} von {studiengang.gesamtmonate}")

    def _ziel_studiendauer(self, studiengang: Studiengang) -> None:
        print(f"  ZIEL 1  ABSCHLUSS IN {studiengang.ziel_dauer_jahre} JAHREN  "
              f"(bis {studiengang.zieldatum.strftime('%d.%m.%Y')})")
        print(f"    Zeit        {self._balken(studiengang.zeit_fortschritt)}  "
              f"{studiengang.zeit_fortschritt:>4.0%}  "
              f"{studiengang.verstrichene_monate}/{studiengang.gesamtmonate} Mon.")
        print(f"    ECTS        {self._balken(studiengang.ects_fortschritt)}  "
              f"{studiengang.ects_fortschritt:>4.0%}  "
              f"{studiengang.erreichte_ects}/{GESAMT_ECTS} CP")

        abweichung = studiengang.ects_abweichung
        vorzeichen = "+" if abweichung >= 0 else "-"
        print(f"    Abweichung  {vorzeichen}{abs(abweichung)} CP gegenueber Soll "
              f"({studiengang.ects_soll} CP)")

        prognose = studiengang.prognose_abschlussdatum
        if prognose is None:
            print("    Prognose    noch keine Leistungen erfasst")
        else:
            verzug = studiengang.prognose_verzug_monate
            zusatz = (f"({verzug} Monate nach dem Ziel)" if verzug
                      else "(im Rahmen des Ziels)")
            print(f"    Prognose    Abschluss {prognose.strftime(MONATSNAMEN_FORMAT)}  {zusatz}")

    def _ziel_notendurchschnitt(self, studiengang: Studiengang) -> None:
        print(f"  ZIEL 2  NOTENDURCHSCHNITT {self._zahl(studiengang.ziel_note)}")
        durchschnitt = studiengang.notendurchschnitt
        if durchschnitt is None:
            print("    Aktuell     noch keine Note erfasst")
            print("    Abweichung  -")
            print("    Prognose    -")
            return

        print(f"    Aktuell     {self._zahl(durchschnitt, 2)}")
        abweichung = studiengang.noten_abweichung
        if abweichung <= 0:
            print(f"    Abweichung  {self._zahl(abs(abweichung), 2)} besser als das Ziel")
        else:
            print(f"    Abweichung  {self._zahl(abweichung, 2)} schlechter als das Ziel")
        print(f"    Prognose    Abschluss mit {self._zahl(studiengang.prognose_notendurchschnitt, 2)}"
              f" bei gleichbleibender Leistung")

    def _menuezeile(self) -> None:
        print("  [1] Modul anlegen   [2] Note eintragen   [q] Ende")
