from fastapi import FastAPI
from .routers import lycees, codepostaux
from .services import datadrop


app = FastAPI(
    title="French Commune API", 
    docs_url="/v1", 
    redoc_url="/", 
    version="v1.0"
)


@app.on_event("startup")
def load_data():
    datadrop.db_startup()
    datadrop.postaux_load_tbl()
    datadrop.lycees_load_tbl()


@app.on_event("shutdown")
def destroy_session():
    pass


app.include_router(lycees.router)
app.include_router(codepostaux.router)
