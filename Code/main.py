from typing import Optional

from fastapi import FastAPI
from pydantic import BaseModel, Field

from Code.logik import berechne_stand


class Modul(BaseModel):
    name: str
    ects: int = Field(gt=0)
    gruppe: Optional[str] = None   # leer lassen, wenn die Modulgruppe nicht bekannt ist


class StandRequest(BaseModel):
    bisher: dict[str, int] = {}    # bereits erreichte ECTS pro Modulgruppe
    module: list[Modul] = []       # Module, die dazukommen sollen


class GruppenStand(BaseModel):
    gruppe: str
    ist: int
    minimum: int
    restbedarf: int
    erfuellt: bool


class StandResponse(BaseModel):
    total_ects: int
    rest_bis_abschluss: int
    zulassung_bachelorarbeit: bool
    rest_bis_zulassung: int
    gruppen: list[GruppenStand]
    nicht_zugeordnet: list[str]


app = FastAPI(title="ECTS-Tracker")


@app.post("/ects-stand", response_model=StandResponse)
async def ects_stand(req: StandRequest):
    return berechne_stand(req.bisher, [m.model_dump() for m in req.module])
