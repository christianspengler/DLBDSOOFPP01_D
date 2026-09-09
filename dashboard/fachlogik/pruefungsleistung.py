"""Fachliche Klasse Pruefungsleistung."""

from datetime import date

from dashboard.fachlogik.aufzaehlungen import Pruefungsart

# Ab dieser Note gilt eine Pruefungsleistung als nicht mehr bestanden.
SCHLECHTESTE_BESTANDENE_NOTE = 4.0


class Pruefungsleistung:
    """Ein einzelner Pruefungsversuch zu einem Modul.

    Eine Pruefungsleistung wird ausschliesslich vom zugehoerigen Modul erzeugt
    (Komposition). Der Versuchszaehler wird dabei vom Modul vergeben.
    """

    def __init__(self, art: Pruefungsart, versuch: int, datum: date, note: float):
        self._art = art
        self._versuch = versuch
        self._datum = datum
        self._note = note

    @property
    def art(self) -> Pruefungsart:
        return self._art

    @property
    def versuch(self) -> int:
        return self._versuch

    @property
    def datum(self) -> date:
        return self._datum

    @property
    def note(self) -> float:
        return self._note

    @property
    def ist_bestanden(self) -> bool:
        """Bestanden, solange die Note nicht schlechter als 4,0 ist."""
        return self._note is not None and self._note <= SCHLECHTESTE_BESTANDENE_NOTE

    def __repr__(self) -> str:
        return (f"Pruefungsleistung({self._art.value}, Versuch {self._versuch}, "
                f"{self._datum}, Note {self._note})")
