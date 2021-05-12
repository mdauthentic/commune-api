from rethinkdb import RethinkDB

# rethink config
RDB_HOST = "localhost"
RDB_PORT = 28015
LYCEES_DB = "test"
TABLE_NAME_LYCEES = "lycees"
TABLE_NAME_POSTAUX = "postaux"

r = RethinkDB()
connect_db = r.connect(host=RDB_HOST, port=RDB_PORT)


def get_db():
    db = r.connect(host=RDB_HOST, port=RDB_PORT)
    try:
        yield db
    finally:
        db.close()
