"""Fachliche Klasse Semester."""

from datetime import date

from dashboard.fachlogik.modul import Modul


class Semester:
    """Ein Semester des Studiengangs mit den ihm zugeordneten Modulen.

    Zwischen Semester und Modul besteht eine Aggregation: Das Modul wird nicht
    vom Semester erzeugt, sondern uebergeben, und existiert nach einer
    Umplanung unabhaengig vom Semester weiter.
    """

    def __init__(self, nummer: int, beginn: date, ende: date):
        self._nummer = nummer
        self._beginn = beginn
        self._ende = ende
        self._module: list[Modul] = []

    @property
    def nummer(self) -> int:
        return self._nummer

    @property
    def beginn(self) -> date:
        return self._beginn

    @property
    def ende(self) -> date:
        return self._ende

    @property
    def module(self) -> tuple:
        return tuple(self._module)

    @property
    def ects_erreicht(self) -> int:
        """Summe der ECTS aller bestandenen Module dieses Semesters."""
        return sum(m.ects for m in self._module if m.ist_bestanden)

    @property
    def ist_abgeschlossen(self) -> bool:
        """Abgeschlossen, wenn Module zugeordnet und alle bestanden sind."""
        return bool(self._module) and all(m.ist_bestanden for m in self._module)

    def modul_zuordnen(self, modul: Modul) -> None:
        """Ordnet ein bereits bestehendes Modul diesem Semester zu."""
        if modul not in self._module:
            self._module.append(modul)

    def modul_suchen(self, kuerzel: str) -> Modul | None:
        """Liefert das Modul mit dem angegebenen Kuerzel oder None."""
        for modul in self._module:
            if modul.kuerzel.upper() == kuerzel.upper():
                return modul
        return None

    def __repr__(self) -> str:
        return f"Semester({self._nummer}, {len(self._module)} Module)"
