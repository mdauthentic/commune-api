from rethinkdb import RethinkDB
from ..config import parse_config


# rethink config
RDB_HOST = "db"
RDB_PORT = parse_config()["rethinkdb"]["port"]
LYCEES_DB = parse_config()["rethinkdb"]["db"]
TABLE_NAME_LYCEES = parse_config()["lycees"]["table"]
TABLE_NAME_POSTAUX = parse_config()["postaux"]["table"]

r = RethinkDB()
connect_db = r.connect(host=RDB_HOST, port=RDB_PORT)


def get_db():
    db = r.connect(host=RDB_HOST, port=RDB_PORT)
    try:
        yield db
    finally:
        db.close()
