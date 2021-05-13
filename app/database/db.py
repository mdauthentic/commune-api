import configparser
from rethinkdb import RethinkDB

config = configparser.ConfigParser()
config.read("../db.ini")

# rethink config
RDB_HOST = config["rethinkdb"]["host"]
RDB_PORT = config["rethinkdb"]["port"]
LYCEES_DB = config["rethinkdb"]["db"]
TABLE_NAME_LYCEES = config["lycees"]["table"]
TABLE_NAME_POSTAUX = config["postaux"]["table"]

r = RethinkDB()
connect_db = r.connect(host=RDB_HOST, port=RDB_PORT)


def get_db():
    db = r.connect(host=RDB_HOST, port=RDB_PORT)
    try:
        yield db
    finally:
        db.close()
