from typing import List, Optional
from fastapi import APIRouter, status, HTTPException, Depends
from rethinkdb import RethinkDB
from rethinkdb.net import Connection
from rethinkdb.ast import Table
from database import db as dbinit
from schemas import LyceeBase


router = APIRouter(prefix="/v1/lycees", tags=["Lycees"])

base: RethinkDB = dbinit.r
tbl: Table = base.db(dbinit.LYCEES_DB).table(dbinit.TABLE_NAME_LYCEES)


@router.get("/", response_model=List[LyceeBase])
def all(db: Connection = Depends(dbinit.get_db)):
    search = tbl.run(db)
    return list(search)