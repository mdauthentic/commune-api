<h1 align="center">
    Commune API
</h1>

`Commune API` provides two categories of information, first one is about all high schools in France and the other is postal codes for all communities/cities in France and oversea territories.

## Data Sources

The raw data is downloaded from [Data.gouv](https://data.gouv.fr) on the following links;

- [Lycees](https://www.data.gouv.fr/fr/datasets/lycees-donnees-generales/)
- [Codes Postaux](https://www.data.gouv.fr/fr/datasets/codes-postaux/#_)

## Tech Stack

- Python3.9
- FastAPI
- Unicorn
- RethinkDB

## API Endpoints

Something


## Installation

Make sure you have [`python3.9`](https://docs.python-guide.org/starting/installation/) above installed and on your `PATH` before you continue to the next step.

```bash
git clone https://github.com/mdauthentic/commune-api.git`
cd commune-api
python3 -m venv my-env
source my-env/bin/activate  
pip3 install -r requirements.txt
uvicorn app.main:app --reload
```