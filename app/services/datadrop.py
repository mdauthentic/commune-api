from typing import Any, Dict, List
import logging
from rethinkdb import RethinkDB
import urllib3
import json
from urllib3.exceptions import HTTPError


DB_NAME = "test"
TBL_NAME = "lycees"


def api_request() -> List[Dict[str, Any]]:
    """Request data from REST API endpoints"""
    http = urllib3.PoolManager()
    get_url = (
        "https://www.data.gouv.fr/fr/datasets/r/7a0d991f-23c0-4021-a23a-b0c7f051c51d"
    )

    logging.info(f"Attempting to get data {get_url}...")
    try:
        response = http.request(
            "GET",
            get_url,
            headers={"User-Agent": "Mozilla/5.0"},
            retries=urllib3.util.Retry(3),
        )
        data = json.loads(response.data.decode("utf8"))
    except HTTPError as err:
        logging.error(f"HTTP error occured for {get_url}", err)
    except urllib3.exceptions.MaxRetryError as err:
        logging.error(f"API unavailable at {get_url}", err)

    results = [data[i]["fields"] for i in range(len(data))]

    return results


def data_dump_db():
    r = RethinkDB()
    logging.info(f"Establishing database connection...")
    with r.connect(db=DB_NAME) as conn:
        json_result = api_request()
        r.table(TBL_NAME).insert(json_result).run(conn)
        logging.info(f"Data successfully imported into database")
