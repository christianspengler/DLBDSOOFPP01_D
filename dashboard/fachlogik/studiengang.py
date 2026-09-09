"""Fachliche Klasse Studiengang.

Der Studiengang ist die oberste fachliche Klasse. Nur hier liegen alle Daten
vor, die zur Aggregation der beiden Zielkennzahlen noetig sind, weshalb die
Berechnung von Fortschritt, Abweichung und Prognose hier angesiedelt ist
(Information-Expert-Prinzip, siehe Phase 1, Kapitel 3.2).
"""

from datetime import date

from dashboard.fachlogik.modul import Modul
from dashboard.fachlogik.semester import Semester

# Fuer den Abschluss erforderliche Leistungspunkte des Bachelorstudiengangs.
GESAMT_ECTS = 180
# Dauer eines Semesters in Monaten.
MONATE_JE_SEMESTER = 6


def monate_addieren(start: date, monate: int) -> date:
    """Addiert Monate auf ein Datum, ohne externe Bibliothek.

    timedelta kennt keine Monate, deshalb wird ueber Jahr und Monat gerechnet.
    Ein zu hoher Tag (z. B. der 31. im Februar) wird auf den Monatsletzten
    zurueckgesetzt.
    """
    monat_gesamt = start.month - 1 + monate
    jahr = start.year + monat_gesamt // 12
    monat = monat_gesamt % 12 + 1
    tag = start.day
    while True:
        try:
            return date(jahr, monat, tag)
        except ValueError:
            tag -= 1


def monate_zwischen(start: date, stichtag: date) -> int:
    """Vollstaendig verstrichene Monate zwischen zwei Datumsangaben."""
    monate = (stichtag.year - start.year) * 12 + (stichtag.month - start.month)
    if stichtag.day < start.day:
        monate -= 1
    return max(0, monate)


class Studiengang:
    """Studiengang mit Semestern, Zielwerten und den daraus abgeleiteten Kennzahlen."""

    def __init__(self, bezeichnung: str, startdatum: date,
                 ziel_dauer_jahre: int = 3, ziel_note: float = 2.0):
        self._bezeichnung = bezeichnung
        self._startdatum = startdatum
        self._ziel_dauer_jahre = ziel_dauer_jahre
        self._ziel_note = ziel_note
        self._semester: list[Semester] = []

    # --- lesende Eigenschaften -------------------------------------------
    @property
    def bezeichnung(self) -> str:
        return self._bezeichnung

    @property
    def startdatum(self) -> date:
        return self._startdatum

    @property
    def ziel_dauer_jahre(self) -> int:
        return self._ziel_dauer_jahre

    @property
    def ziel_note(self) -> float:
        return self._ziel_note

    @property
    def semester(self) -> tuple:
        return tuple(self._semester)

    @property
    def zieldatum(self) -> date:
        """Spaetestes Abschlussdatum, das Ziel 1 noch erfuellt."""
        return monate_addieren(self._startdatum, self._ziel_dauer_jahre * 12)

    # --- Kennzahlen zu Ziel 1: Abschluss in drei Jahren -------------------
    @property
    def gesamtmonate(self) -> int:
        return self._ziel_dauer_jahre * 12

    @property
    def verstrichene_monate(self) -> int:
        return monate_zwischen(self._startdatum, date.today())

    @property
    def zeit_fortschritt(self) -> float:
        """Anteil der verstrichenen Zeit an der angestrebten Studiendauer."""
        return self.verstrichene_monate / self.gesamtmonate

    @property
    def erreichte_ects(self) -> int:
        return sum(s.ects_erreicht for s in self._semester)

    @property
    def ects_fortschritt(self) -> float:
        return self.erreichte_ects / GESAMT_ECTS

    @property
    def ects_soll(self) -> int:
        """ECTS, die zum heutigen Tag erreicht sein muessten."""
        return round(GESAMT_ECTS * self.zeit_fortschritt)

    @property
    def ects_abweichung(self) -> int:
        """Differenz zwischen erreichten und erforderlichen ECTS.

        Ein negativer Wert bedeutet einen Rueckstand gegenueber dem Soll.
        """
        return self.erreichte_ects - self.ects_soll

    @property
    def prognose_abschlussdatum(self) -> date | None:
        """Abschlussdatum bei gleichbleibendem Tempo; None ohne Leistungen."""
        monate = self.verstrichene_monate
        if self.erreichte_ects == 0 or monate == 0:
            return None
        ects_pro_monat = self.erreichte_ects / monate
        benoetigte_monate = round(GESAMT_ECTS / ects_pro_monat)
        return monate_addieren(self._startdatum, benoetigte_monate)

    @property
    def prognose_verzug_monate(self) -> int | None:
        """Monate, um die die Prognose das Zieldatum ueberschreitet."""
        prognose = self.prognose_abschlussdatum
        if prognose is None:
            return None
        return monate_zwischen(self.zieldatum, prognose) if prognose > self.zieldatum else 0

    # --- Kennzahlen zu Ziel 2: Notendurchschnitt 2,0 ----------------------
    @property
    def bewertete_module(self) -> list:
        """Alle Module, zu denen bereits eine bestandene Note vorliegt."""
        module = []
        for semester in self._semester:
            for modul in semester.module:
                if modul.modulnote is not None:
                    module.append(modul)
        return module

    @property
    def notendurchschnitt(self) -> float | None:
        """Nach ECTS gewichteter Durchschnitt; None ohne bewertete Module.

        Die Gewichtung ist noetig, weil Module mit mehr Leistungspunkten
        staerker in die Abschlussnote eingehen als ein einfacher Mittelwert
        abbilden wuerde.
        """
        module = self.bewertete_module
        summe_ects = sum(m.ects for m in module)
        if summe_ects == 0:
            return None
        summe_punkte = sum(m.modulnote * m.ects for m in module)
        return summe_punkte / summe_ects

    @property
    def noten_abweichung(self) -> float | None:
        """Abstand zum Zielwert; negativ bedeutet besser als das Ziel."""
        durchschnitt = self.notendurchschnitt
        if durchschnitt is None:
            return None
        return durchschnitt - self._ziel_note

    @property
    def prognose_notendurchschnitt(self) -> float | None:
        """Erwarteter Abschlussdurchschnitt bei gleichbleibender Leistung."""
        return self.notendurchschnitt

    # --- veraendernde Operationen ----------------------------------------
    def semester_anlegen(self, nummer: int) -> Semester:
        """Legt ein Semester an (Komposition) oder liefert das vorhandene.

        Beginn und Ende ergeben sich aus dem Studienbeginn, sodass keine
        weiteren Eingaben noetig sind.
        """
        vorhanden = self.semester_suchen(nummer)
        if vorhanden is not None:
            return vorhanden
        beginn = monate_addieren(self._startdatum, (nummer - 1) * MONATE_JE_SEMESTER)
        ende = monate_addieren(beginn, MONATE_JE_SEMESTER)
        semester = Semester(nummer, beginn, ende)
        self._semester.append(semester)
        self._semester.sort(key=lambda s: s.nummer)
        return semester

    def semester_suchen(self, nummer: int) -> Semester | None:
        for semester in self._semester:
            if semester.nummer == nummer:
                return semester
        return None

    def modul_suchen(self, kuerzel: str) -> Modul | None:
        """Sucht ein Modul ueber alle Semester hinweg."""
        for semester in self._semester:
            modul = semester.modul_suchen(kuerzel)
            if modul is not None:
                return modul
        return None

    def __repr__(self) -> str:
        return f"Studiengang({self._bezeichnung}, {len(self._semester)} Semester)"
