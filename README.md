<h1 align="center">
    Commune API
</h1>

`Commune API` provides two categories of information, first one is about all high schools in France and the other is postal codes for all communities/cities in France and oversea territories.

## Data Sources

The raw data is downloaded from [data.gouv](https://data.gouv.fr) on the following links;

- [Lycees](https://www.data.gouv.fr/fr/datasets/lycees-donnees-generales/)
- [Codes Postaux](https://www.data.gouv.fr/fr/datasets/codes-postaux/#_)

## Tech Stack

- `Python3.9`
- `FastAPI`
- `Unicorn`
- `RethinkDB`

## API Endpoints

The list of endpoints avaliable are as follows:

### High Schools (Lycees)

#### All High Schools Endpoint

List all high schools in France (paginated at 100 per page)

```http
GET /v1/lycees/
```

#### Search

Search for high school using parameters like `num_siret, code_postal, nom_etablissement and statut`. E.g. `GET /v1/lycees/search?num_siret=12345678`
           
```http
GET /v1/lycees/q?search_field=searach_param
```

#### High Schools in Postal Code

You can get the list of high schools in a given postal code using the endpoint below

```http
GET /v1/lycees/{code_postal}
```

### Postal Code (Codes Postaux)

#### All Communities Endpoint

List all communities in France (paginated at 100 per page)

```http
GET /v1/postaux/
```

#### Search

Search for communities using parameters like `codePostal, nomCommune`. E.g. `GET /v1/postaux/search?codePostal=12345678`
           
```http
GET /v1/postaux/q?search_field=searach_param
```


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