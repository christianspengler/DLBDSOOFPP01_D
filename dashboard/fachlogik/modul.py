"""Fachliche Klasse Modul."""

from datetime import date

from dashboard.fachlogik.aufzaehlungen import Pruefungsart, Status
from dashboard.fachlogik.pruefungsleistung import Pruefungsleistung


class Modul:
    """Ein Modul des Studiengangs mit seinen Pruefungsleistungen.

    Zwischen Modul und Pruefungsleistung besteht eine Komposition: Das Modul
    erzeugt seine Pruefungsleistungen selbst und gibt die interne Liste nicht
    nach aussen, sondern nur als unveraenderliches Tupel zurueck. Diese
    Zuständigkeit ist eine Konvention und keine technische Absicherung, da
    Python den Zugriff auf _pruefungen nicht verhindern kann.
    """

    def __init__(self, kuerzel: str, titel: str, ects: int):
        self._kuerzel = kuerzel
        self._titel = titel
        self._ects = ects
        self._pruefungen: list[Pruefungsleistung] = []

    # --- lesende Eigenschaften -------------------------------------------
    @property
    def kuerzel(self) -> str:
        return self._kuerzel

    @property
    def titel(self) -> str:
        return self._titel

    @property
    def ects(self) -> int:
        return self._ects

    @property
    def pruefungen(self) -> tuple:
        """Unveraenderliche Sicht auf die Pruefungsleistungen des Moduls."""
        return tuple(self._pruefungen)

    # --- abgeleitete Groessen --------------------------------------------
    @property
    def modulnote(self) -> float | None:
        """Beste bestandene Note; None, solange kein Versuch bestanden ist."""
        bestanden = [p.note for p in self._pruefungen if p.ist_bestanden]
        return min(bestanden) if bestanden else None

    @property
    def status(self) -> Status:
        """Bearbeitungsstand, abgeleitet aus den Pruefungsleistungen.

        Der Status wird bewusst nicht gespeichert, damit die Information nur an
        einer Stelle gefuehrt wird (Rueckmeldung aus Phase 1).
        """
        if not self._pruefungen:
            return Status.OFFEN
        if any(p.ist_bestanden for p in self._pruefungen):
            return Status.BESTANDEN
        return Status.IN_BEARBEITUNG

    @property
    def ist_bestanden(self) -> bool:
        return self.status is Status.BESTANDEN

    # --- veraendernde Operation ------------------------------------------
    def pruefung_eintragen(self, art: Pruefungsart, datum: date, note: float) -> Pruefungsleistung:
        """Legt einen weiteren Pruefungsversuch an und vergibt die Versuchsnummer."""
        versuch = len(self._pruefungen) + 1
        pruefung = Pruefungsleistung(art, versuch, datum, note)
        self._pruefungen.append(pruefung)
        return pruefung

    def __repr__(self) -> str:
        return f"Modul({self._kuerzel}, {self._ects} CP, {self.status.value})"
