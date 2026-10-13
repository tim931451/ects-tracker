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

GESAMT_ECTS = 180          # ECTS für den Bachelorabschluss
ZULASSUNG_BA_ECTS = 140    # ECTS für die Zulassung zur Bachelorarbeit


def berechne_stand(bisher: dict[str, int], module: list[dict]) -> dict:
    """Addiert die Module zum bisherigen Stand und vergleicht mit den Minima.

    bisher: ECTS pro Modulgruppe, die schon erreicht sind
    module: Liste von Dicts mit name, ects, gruppe (gruppe darf None sein)
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
    }
