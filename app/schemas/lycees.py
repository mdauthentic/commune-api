from typing import List
from pydantic import BaseModel


class Geo(BaseModel):
    type: str
    coordinates: List[int]


class LyceeBase(BaseModel):
    code_uai: str = None
    code_postal: int = None
    nature_uai: str = None
    statut: str = None
    code_academie: str = None
    num_siret: int = None
    ministere_tutelle: str = None
    libelle: str = None
    telephone: str = None
    sigle_uai: str = None
    nom_etablissement: str = None
    dep: int = None
    code_insee: int = None
    academie: str = None
    date_maj: str = None
    adresse_postale: str = None
    geo: List[float] = []
    patronyme: str = None
    contrat_etablissement: str = None

    class Config:
        orm_mode = True

