from typing import Any, Dict, List
import logging
from rethinkdb import RethinkDB
import urllib3
import json
from urllib3.exceptions import HTTPError
from ..config import parse_config


def api_request(data_url: str) -> List[Dict[str, Any]]:
    """Request data from REST API endpoints
    Due to known issues @ https://github.com/rethinkdb/rethinkdb/issues/5521
    it is important to first download the data and load into the db
    instead of uploading using RethinkDB `r.http` function
    """
    http = urllib3.PoolManager()

    logging.info(f"Attempting to get data {data_url}...")
    try:
        response = http.request(
            "GET",
            data_url,
            headers={"User-Agent": "Mozilla/5.0"},
            retries=urllib3.util.Retry(3),
        )
        data = json.loads(response.data.decode("utf8"))
    except HTTPError as err:
        logging.error(f"HTTP error occured for {data_url}", err)
    except urllib3.exceptions.MaxRetryError as err:
        logging.error(f"API unavailable at {data_url}", err)

    return data


def db_startup():
    config = parse_config()
    db_name = config["rethinkdb"]["db"]
    db_port = config["rethinkdb"]["port"]
    tbl_list = [config["lycees"]["table"], config["postaux"]["table"]]

    r = RethinkDB()

    logging.info(f"Establishing database connection...")
    with r.connect(host="db", port=db_port) as conn:
        if db_name not in r.db_list().run(conn):
            r.db_create(db_name).run(conn)
            logging.info(f"{db_name} database created...")

        for tbl in tbl_list:
            if tbl not in r.table_list().run(conn):
                r.table_create(tbl).run(conn)
                logging.info(f"{tbl} table created")
    
    logging.info("Database initialized.")


def json_to_db(json_result: List[Dict[str, Any]], tbl_name: str) -> None:
    """Insert documents into database table"""
    config = parse_config()
    db_name = config["rethinkdb"]["db"]
    db_port = config["rethinkdb"]["port"]

    r = RethinkDB()
    with r.connect(host="db", port=db_port, db=db_name) as conn:
        r.table(tbl_name).insert(json_result).run(conn, durability="soft")

