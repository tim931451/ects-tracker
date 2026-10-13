# ECTS-Tracker

Projektarbeit AI Operations HS 2026, Teilaufgabe 1 (DevOps lokal). Eine FastAPI-Schnittstelle, die aus den bisher erreichten ECTS pro Modulgruppe und einer Liste weiterer Module den Stand gegen die Mindestanforderungen des Curriculums BSc Business AI berechnet.

**Eingabe** bisher erreichte ECTS pro Modulgruppe und eine Liste von Modulen mit Name, ECTS und optional Modulgruppe.
**Ausgabe** Total, Restbedarf bis zum Abschluss (180 ECTS) und bis zur Zulassung zur Bachelorarbeit (140 ECTS), Stand und Restbedarf pro Modulgruppe sowie die Module, deren Gruppe nicht bekannt ist.

## Lokal starten (macOS)

```
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn Code.main:app --reload
```

Danach im Browser http://127.0.0.1:8000/docs öffnen, beim Endpunkt `POST /ects-stand` auf "Try it out" klicken und den Inhalt von `beispiel_anfrage.json` einfügen.

## Aufbau

- `Code/logik.py` Business-Logik, unabhängig von der API
- `Code/main.py` FastAPI-App mit Ein- und Ausgabeschema
- `requirements.txt` mit festen Versionen, nach dem lokalen Test mit `pip freeze` erzeugt (die Versionen aus dem Beispielprojekt, etwa pydantic 2.9.2, liessen sich unter Python 3.14 nicht installieren)
- `beispiel_anfrage.json` Beispielanfrage mit dem Stand aus dem Transcript of Records vom 13.08.2026 und den belegten Modulen des HS 2026

## Hinweise

Die Minima pro Modulgruppe stammen aus dem Transcript of Records vom 13.08.2026. Die Zuordnung der HS-2026-Module zu den Modulgruppen stammt aus der Modulübersicht BSc Business Artificial Intelligence, Curriculum 2025. Module ohne bekannte Gruppe zählen zum Total und werden in `nicht_zugeordnet` ausgewiesen.
