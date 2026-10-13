from typing import Literal, Optional

from fastapi import FastAPI
from pydantic import BaseModel, Field, model_validator

from Code.logik import berechne_stand


class Termin(BaseModel):
    tag: Literal["Mo", "Di", "Mi", "Do", "Fr", "Sa", "So"]
    von: str = Field(pattern=r"^([01]\d|2[0-3]):[0-5]\d$")   # Format HH:MM
    bis: str = Field(pattern=r"^([01]\d|2[0-3]):[0-5]\d$")

    @model_validator(mode="after")
    def von_vor_bis(self):
        if self.von >= self.bis:
            raise ValueError("von muss vor bis liegen")
        return self


class Modul(BaseModel):
    name: str
    ects: int = Field(gt=0)
    gruppe: Optional[str] = None   # leer lassen, wenn die Modulgruppe nicht bekannt ist
    termine: list[Termin] = []     # wöchentliche Unterrichtszeiten, optional


class StandRequest(BaseModel):
    bisher: dict[str, int] = {}    # bereits erreichte ECTS pro Modulgruppe
    module: list[Modul] = []       # Module, die dazukommen sollen


class GruppenStand(BaseModel):
    gruppe: str
    ist: int
    minimum: int
    restbedarf: int
    erfuellt: bool


class Konflikt(BaseModel):
    tag: str
    modul_a: str
    modul_b: str
    von: str
    bis: str


class StandResponse(BaseModel):
    total_ects: int
    rest_bis_abschluss: int
    zulassung_bachelorarbeit: bool
    rest_bis_zulassung: int
    gruppen: list[GruppenStand]
    nicht_zugeordnet: list[str]
    konflikte: list[Konflikt]


app = FastAPI(title="ECTS-Tracker", version="1.2")


@app.get("/")
async def info():
    """Kurzinfo zum Dienst, damit ein Aufruf der Basis-URL nicht ins Leere läuft."""
    return {"dienst": "ECTS-Tracker", "version": "1.2", "doku": "/docs", "endpunkt": "POST /ects-stand"}


@app.post("/ects-stand", response_model=StandResponse)
async def ects_stand(req: StandRequest):
    return berechne_stand(req.bisher, [m.model_dump() for m in req.module])
