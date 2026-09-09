"""Startskript des Dashboard-Prototyps.

Aufruf im Projektverzeichnis:
    python main.py
Optional kann eine abweichende Datendatei angegeben werden:
    python main.py meine_daten.json
"""

import sys
from pathlib import Path

from dashboard.application import Application

if __name__ == "__main__":
    pfad = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("studium.json")
    Application(pfad).main()
