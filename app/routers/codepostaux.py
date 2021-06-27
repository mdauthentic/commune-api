from typing import List, Optional
from fastapi import APIRouter, status, HTTPException, Depends
from rethinkdb import RethinkDB
from rethinkdb.net import Connection
from rethinkdb.ast import Table
from ..database import db as dbinit
from ..schemas import postaux


router = APIRouter(prefix="/v1/postaux", tags=["Codes Postaux"])

base: RethinkDB = dbinit.r
tbl: Table = base.db(dbinit.LYCEES_DB).table(dbinit.TABLE_NAME_POSTAUX)


@router.get("/", response_model=List[postaux.CodesPostaux])
def all(db: Connection = Depends(dbinit.get_db)):
    search = tbl.run(db)
    return list(search)


@router.get("/q", response_model=List[postaux.CodesPostaux])
def search(db: Connection = Depends(dbinit.get_db),
           codePostal: Optional[str] = None,
           nomCommune: Optional[str] = None):

    if codePostal and nomCommune:
        search = tbl.filter(
            lambda lycee: (lycee["codePostal"] == f"{codePostal}")
            & (
                lycee["nomCommune"]
                .downcase()
                .match(f"{nomCommune}".lower())
            )
        ).run(db)
        result_list = list(search)
        if not result_list:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Data not found. Try with another search parameter(s)",
            )
        return result_list
    elif codePostal:
        search = tbl.filter(
            base.row["codePostal"].match(f"{codePostal}")).run(db)
        result_list = list(search)
        if not result_list:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Data cannot be retrieved for '{codePostal}'",
            )
        return result_list
    elif nomCommune:
        search = tbl.filter(
            base.row["nomCommune"].match(f"{nomCommune}")).run(db)
        result_list = list(search)
        if not result_list:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Data cannot be retrieved for '{nomCommune}'",
            )
        return result_list
    else:
        raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="You must provide a search parameter",
            )
