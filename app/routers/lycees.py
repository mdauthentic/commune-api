from typing import List, Optional
from fastapi import APIRouter, status, HTTPException, Depends
from rethinkdb import RethinkDB
from rethinkdb.net import Connection
from rethinkdb.ast import Table
from database import db as dbinit
from schemas import lycees


router = APIRouter(prefix="/v1/lycees", tags=["Lycees"])

base: RethinkDB = dbinit.r
tbl: Table = base.db(dbinit.LYCEES_DB).table(dbinit.TABLE_NAME_LYCEES)


@router.get("/", response_model=List[lycees.LyceeBase])
def all(db: Connection = Depends(dbinit.get_db), skip: int = 0, limit: int = 100):
    search = tbl.run(db)
    result_list = list(search)[skip : skip + limit]
    return result_list


@router.get("/q", response_model=List[lycees.LyceeBase])
def search(
    num_siret: Optional[int] = None,
    code_postal: Optional[int] = None,
    nom_etablissement: Optional[str] = None,
    statut: Optional[str] = None,
    db: Connection = Depends(dbinit.get_db)
):

    if code_postal and nom_etablissement:
        search = tbl.filter(
            lambda lycee: (lycee["code_postal"] == f"{code_postal}")
            & (
                lycee["nom_etablissement"]
                .downcase()
                .match(f"{nom_etablissement}".lower())
            )
        ).run(db)
        result_list = list(search)
        if not result_list:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Invalid paramter: {num_siret}",
            )
        return result_list
    elif num_siret:
        search = tbl.filter({'num_siret': num_siret}).run(db)
        result_list = list(search)
        if not result_list:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Invalid paramter: {num_siret}",
            )
        return result_list
    elif code_postal:
        search = tbl.filter({'code_postal': f"{code_postal}"}).run(db)
        result_list = list(search)
        if not result_list:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Invalid paramter: {code_postal}",
            )
        return result_list
    elif nom_etablissement:
        search = tbl.filter(
            base.row['nom_etablissement'].match(f"{nom_etablissement}")).run(db)
        result_list = list(search)
        if not result_list:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Invalid paramter: {nom_etablissement}",
            )
        return result_list
    elif statut:
        search = tbl.filter(base.row["statut"].match(f"{statut}")).run(db)
        result_list = list(search)
        if not result_list:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Invalid paramter: {statut}",
            )
        return result_list
    else:
        raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="You must provide a valid search parameter",
            )


@router.get("/{code_postal}", response_model=List[lycees.LyceeBase])
def by_postal_code(code_postal: int, db: Connection = Depends(dbinit.get_db)):
    search = tbl.filter({'code_postal': f"{code_postal}"}).run(db)
    result_list = list(search)
    if not search:
        raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Invalid paramter: {code_postal}",
            )
    return result_list
