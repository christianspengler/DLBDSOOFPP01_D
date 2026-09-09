"""Fachliche Klassen des Studien-Dashboards."""

from dashboard.fachlogik.aufzaehlungen import Pruefungsart, Status
from dashboard.fachlogik.modul import Modul
from dashboard.fachlogik.pruefungsleistung import Pruefungsleistung
from dashboard.fachlogik.semester import Semester
from dashboard.fachlogik.studiengang import Studiengang

__all__ = ["Pruefungsart", "Status", "Modul", "Pruefungsleistung", "Semester", "Studiengang"]
