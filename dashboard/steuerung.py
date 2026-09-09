"""Steuerung des Programmablaufs.

Die Klasse verbindet Fachlogik, Darstellung und Persistenz: Sie laesst die
Ansicht zeichnen, nimmt die Menueauswahl entgegen, ruft die fachlichen
Operationen auf und speichert nach jeder Aenderung. Ansicht und Speicher
werden ihr uebergeben und nicht selbst erzeugt (Assoziation, siehe Phase 2).
"""

from datetime import date, datetime

from dashboard.darstellung import DashboardAnsicht
from dashboard.fachlogik.aufzaehlungen import Pruefungsart
from dashboard.fachlogik.modul import Modul
from dashboard.fachlogik.studiengang import Studiengang
from dashboard.persistenz import JsonSpeicher

# Zulaessiger Notenbereich an der IU.
BESTE_NOTE = 1.0
SCHLECHTESTE_NOTE = 5.0


class StudienDashboard:
    """Menuegesteuerter Ablauf des Dashboards."""

    def __init__(self, studiengang: Studiengang, speicher: JsonSpeicher,
                 ansicht: DashboardAnsicht):
        self._studiengang = studiengang
        self._speicher = speicher
        self._ansicht = ansicht

    # --- Hauptschleife ----------------------------------------------------
    def starten(self) -> None:
        """Zeigt das Dashboard und verarbeitet Eingaben, bis q gewaehlt wird."""
        while True:
            self._ansicht.zeige(self._studiengang)
            try:
                auswahl = self._ansicht.frage("  Auswahl: ").lower()
            except (EOFError, KeyboardInterrupt):
                print()
                return

            if auswahl == "q":
                self._ansicht.meldung("Programm beendet.")
                return
            if auswahl == "1":
                self._modul_anlegen_dialog()
            elif auswahl == "2":
                self._note_eintragen_dialog()
            else:
                self._ansicht.meldung("Ungueltige Eingabe.")

    # --- Dialoge: Eingaben einsammeln und weiterreichen --------------------
    def _modul_anlegen_dialog(self) -> None:
        """Erfragt die Angaben zu einem Modul und legt es an."""
        print()
        semester_nr = self._zahl_erfragen("  Semester (Nummer): ", 1, 20)
        if semester_nr is None:
            return
        kuerzel = self._ansicht.frage("  Modulkuerzel (z. B. DLBCSL01): ")
        if not kuerzel:
            self._ansicht.meldung("Abgebrochen: kein Kuerzel angegeben.")
            return
        titel = self._ansicht.frage("  Modultitel: ")
        ects = self._zahl_erfragen("  ECTS-Punkte: ", 1, 30)
        if ects is None:
            return

        self._modul_anlegen(semester_nr, kuerzel, titel, ects)

    def _note_eintragen_dialog(self) -> None:
        """Erfragt die Angaben zu einer Pruefungsleistung und traegt sie ein."""
        print()
        kuerzel = self._ansicht.frage("  Modulkuerzel: ")
        if not self._studiengang.modul_suchen(kuerzel):
            self._ansicht.meldung(f"Kein Modul mit dem Kuerzel {kuerzel} gefunden.")
            return

        art = self._pruefungsart_erfragen()
        if art is None:
            return
        datum = self._datum_erfragen()
        if datum is None:
            return
        note = self._note_erfragen()
        if note is None:
            return

        self._note_eintragen(kuerzel, art, datum, note)

    # --- fachliche Operationen der Steuerung ------------------------------
    def _modul_anlegen(self, semester_nr: int, kuerzel: str, titel: str, ects: int) -> None:
        """Legt das Modul an und ordnet es dem angegebenen Semester zu."""
        if self._studiengang.modul_suchen(kuerzel) is not None:
            self._ansicht.meldung(f"Das Modul {kuerzel} ist bereits erfasst.")
            return

        semester = self._studiengang.semester_anlegen(semester_nr)
        semester.modul_zuordnen(Modul(kuerzel.upper(), titel, ects))
        self._speichern()
        self._ansicht.meldung(f"Modul {kuerzel.upper()} im {semester_nr}. Semester angelegt.")

    def _note_eintragen(self, kuerzel: str, art: Pruefungsart, datum: date, note: float) -> None:
        """Traegt eine Pruefungsleistung am betroffenen Modul ein."""
        modul = self._studiengang.modul_suchen(kuerzel)
        if modul is None:
            self._ansicht.meldung(f"Kein Modul mit dem Kuerzel {kuerzel} gefunden.")
            return

        pruefung = modul.pruefung_eintragen(art, datum, note)
        self._speichern()
        self._ansicht.meldung(
            f"Versuch {pruefung.versuch} fuer {modul.kuerzel} eingetragen "
            f"(Note {note}, {modul.status.value})."
        )

    def _speichern(self) -> None:
        """Schreibt den aktuellen Stand in die Datei."""
        self._speicher.speichern(self._studiengang)

    # --- Eingabepruefungen ------------------------------------------------
    def _zahl_erfragen(self, text: str, kleinste: int, groesste: int) -> int | None:
        eingabe = self._ansicht.frage(text)
        try:
            wert = int(eingabe)
        except ValueError:
            self._ansicht.meldung("Abgebrochen: Es wurde keine ganze Zahl eingegeben.")
            return None
        if not kleinste <= wert <= groesste:
            self._ansicht.meldung(f"Abgebrochen: Zulaessig sind Werte von {kleinste} bis {groesste}.")
            return None
        return wert

    def _note_erfragen(self) -> float | None:
        eingabe = self._ansicht.frage("  Note (1,0 bis 5,0): ").replace(",", ".")
        try:
            note = float(eingabe)
        except ValueError:
            self._ansicht.meldung("Abgebrochen: Die Note konnte nicht gelesen werden.")
            return None
        if not BESTE_NOTE <= note <= SCHLECHTESTE_NOTE:
            self._ansicht.meldung("Abgebrochen: Zulaessig sind Noten von 1,0 bis 5,0.")
            return None
        return note

    def _datum_erfragen(self) -> date | None:
        eingabe = self._ansicht.frage("  Pruefungsdatum (TT.MM.JJJJ, leer = heute): ")
        if not eingabe:
            return date.today()
        try:
            return datetime.strptime(eingabe, "%d.%m.%Y").date()
        except ValueError:
            self._ansicht.meldung("Abgebrochen: Das Datum konnte nicht gelesen werden.")
            return None

    def _pruefungsart_erfragen(self) -> Pruefungsart | None:
        arten = list(Pruefungsart)
        print("  Pruefungsart:")
        for nummer, art in enumerate(arten, start=1):
            print(f"    [{nummer}] {art.value}")
        eingabe = self._ansicht.frage("  Auswahl: ")
        try:
            return arten[int(eingabe) - 1]
        except (ValueError, IndexError):
            self._ansicht.meldung("Abgebrochen: Keine gueltige Pruefungsart gewaehlt.")
            return None
