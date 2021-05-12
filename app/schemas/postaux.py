from pydantic import BaseModel


class CodesBase(BaseModel):
    codePostal: str
    codeCommune: str
    nomCommune: str
    libelleAcheminement: str


class CodesPostaux(CodesBase):
    class Config:
        orm_mode = True