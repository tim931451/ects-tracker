# ECTS-Tracker

Projektarbeit AI Operations HS 2026, Teilaufgaben 1 (DevOps lokal) und 2 (DevOps Cloud). Eine FastAPI-Schnittstelle, die aus den bisher erreichten ECTS pro Modulgruppe und einer Liste weiterer Module den Stand gegen die Mindestanforderungen des Curriculums BSc Business AI berechnet.

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

## Cloud (render.com)

Das Repository ist als Web Service auf render.com deployt: https://ects-tracker.onrender.com/docs

- Branch: `main`
- Build Command: `pip install -r requirements.txt`
- Start Command: `uvicorn Code.main:app --host 0.0.0.0 --port $PORT`

Änderungen werden lokal in VS Code gemacht, committet und auf GitHub gepusht. Danach baut render.com den Web Service automatisch neu (Auto-Deploy bei jedem Commit auf main, sonst über Manual Deploy). Der Free Plan legt den Dienst nach Inaktivität schlafen, der erste Aufruf dauert dann rund eine Minute. Ein Aufruf aus Python steht in `Code/test_API.ipynb`.

## Erweiterung Version 1.2: Konfliktwarnung bei Terminüberschneidungen

Jedes Modul kann optional wöchentliche Termine mitgeben (`tag` als Mo bis So, `von` und `bis` im Format HH:MM). Die API prüft alle Termine paarweise und gibt unter `konflikte` jede Überschneidung mit Tag, beiden Modulen und dem überlappenden Zeitfenster aus. Direkt aneinander anschliessende Termine gelten nicht als Konflikt. Ungültige Eingaben (unbekannter Tag, falsches Zeitformat, `von` nach `bis`) beantwortet die API mit Status 422. Anfragen ohne Termine funktionieren wie bisher.

- `beispiel_anfrage.json` Stundenplan HS 2026, ohne Konflikt
- `beispiel_konflikt.json` dieselbe Anfrage mit einem zusätzlichen Beispielmodul am Freitagvormittag, das sich mit Maschinelles Lernen und wissensbasierte Systeme überschneidet

## Aufbau

- `Code/logik.py` Business-Logik, unabhängig von der API
- `Code/main.py` FastAPI-App mit Ein- und Ausgabeschema, Endpunkte `GET /` (Kurzinfo) und `POST /ects-stand`
- `Code/test_API.ipynb` Aufruf der API auf render.com mit der Beispielanfrage
- `requirements.txt` mit festen Versionen, nach dem lokalen Test mit `pip freeze` erzeugt (die Versionen aus dem Beispielprojekt, etwa pydantic 2.9.2, liessen sich unter Python 3.14 nicht installieren)
- `beispiel_anfrage.json` Beispielanfrage mit dem Stand aus dem Transcript of Records vom 13.08.2026 und den belegten Modulen des HS 2026

## Hinweise

Die Minima pro Modulgruppe stammen aus dem Transcript of Records vom 13.08.2026. Die Zuordnung der HS-2026-Module zu den Modulgruppen stammt aus der Modulübersicht BSc Business Artificial Intelligence, Curriculum 2025. Module ohne bekannte Gruppe zählen zum Total und werden in `nicht_zugeordnet` ausgewiesen.
