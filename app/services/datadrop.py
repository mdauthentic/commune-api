from typing import Any, Dict, List
import logging
from rethinkdb import RethinkDB
import urllib3
import json
from urllib3.exceptions import HTTPError


DB_NAME = "test"
TBL_NAME = "lycees"


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


def lycees_clean(data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    return [data[i]["fields"] for i in range(len(data))]


def postal_codes(data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    return data


def data_dump_db(json_result: List[Dict[str, Any]]) -> None:
    r = RethinkDB()
    logging.info(f"Establishing database connection...")
    with r.connect(db=DB_NAME) as conn:
        r.table(TBL_NAME).insert(json_result).run(conn)
        logging.info(f"Data successfully imported into database")
