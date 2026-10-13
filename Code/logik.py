"""Business-Logik des ECTS-Trackers.

Rechnet aus bisher erreichten ECTS pro Modulgruppe und einer Liste geplanter
oder abgeschlossener Module den Stand gegen die Mindestanforderungen des
Curriculums BSc Business AI aus.
"""

# Mindest-ECTS pro Modulgruppe laut Transcript of Records (Stand 13.08.2026)
MINIMA = {
    "Künstliche Intelligenz": 48,
    "Wirtschaftsinformatik": 24,
    "Wirtschaft": 24,
    "Anwendung und Praxis": 48,
}

TAGE = ["Mo", "Di", "Mi", "Do", "Fr", "Sa", "So"]

GESAMT_ECTS = 180          # ECTS für den Bachelorabschluss
ZULASSUNG_BA_ECTS = 140    # ECTS für die Zulassung zur Bachelorarbeit


def berechne_stand(bisher: dict[str, int], module: list[dict]) -> dict:
    """Addiert die Module zum bisherigen Stand und vergleicht mit den Minima.

    bisher: ECTS pro Modulgruppe, die schon erreicht sind
    module: Liste von Dicts mit name, ects, gruppe (gruppe darf None sein)
            und optional termine (Liste von Dicts mit tag, von, bis)
    """
    stand = {gruppe: bisher.get(gruppe, 0) for gruppe in MINIMA}
    nicht_zugeordnet = []

    for modul in module:
        gruppe = modul.get("gruppe")
        if gruppe in stand:
            stand[gruppe] += modul["ects"]
        else:
            # Module ohne bekannte Gruppe zählen zum Total, nicht zu einer Gruppe
            nicht_zugeordnet.append(modul["name"])

    total = sum(bisher.values()) + sum(m["ects"] for m in module)

    gruppen = []
    for gruppe, minimum in MINIMA.items():
        ist = stand[gruppe]
        gruppen.append({
            "gruppe": gruppe,
            "ist": ist,
            "minimum": minimum,
            "restbedarf": max(minimum - ist, 0),
            "erfuellt": ist >= minimum,
        })

    return {
        "total_ects": total,
        "rest_bis_abschluss": max(GESAMT_ECTS - total, 0),
        "zulassung_bachelorarbeit": total >= ZULASSUNG_BA_ECTS,
        "rest_bis_zulassung": max(ZULASSUNG_BA_ECTS - total, 0),
        "gruppen": gruppen,
        "nicht_zugeordnet": nicht_zugeordnet,
        "konflikte": finde_konflikte(module),
    }


def _minuten(zeit: str) -> int:
    """Wandelt "HH:MM" in Minuten seit Mitternacht um."""
    stunden, minuten = zeit.split(":")
    return int(stunden) * 60 + int(minuten)


def _als_zeit(minuten: int) -> str:
    return f"{minuten // 60:02d}:{minuten % 60:02d}"


def finde_konflikte(module: list[dict]) -> list[dict]:
    """Sucht Terminüberschneidungen zwischen den Modulen (Erweiterung Version 1.2).

    Jedes Modul kann eine Liste von Wochenterminen haben (tag, von, bis).
    Zwei Termine überschneiden sich, wenn sie am selben Tag liegen und der
    eine beginnt, bevor der andere endet. Direkt aneinander anschliessende
    Termine (12:00 bis 12:00) gelten nicht als Konflikt.
    """
    termine = []
    for modul in module:
        for termin in modul.get("termine") or []:
            termine.append((modul["name"], termin["tag"],
                            _minuten(termin["von"]), _minuten(termin["bis"])))

    konflikte = []
    for i, (name_a, tag_a, von_a, bis_a) in enumerate(termine):
        for name_b, tag_b, von_b, bis_b in termine[i + 1:]:
            if name_a == name_b or tag_a != tag_b:
                continue
            if von_a < bis_b and von_b < bis_a:
                konflikte.append({
                    "tag": tag_a,
                    "modul_a": name_a,
                    "modul_b": name_b,
                    "von": _als_zeit(max(von_a, von_b)),
                    "bis": _als_zeit(min(bis_a, bis_b)),
                })

    konflikte.sort(key=lambda k: (TAGE.index(k["tag"]), k["von"]))
    return konflikte
