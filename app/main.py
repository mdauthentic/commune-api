from fastapi import FastAPI
from routers import lycees, codepostaux
from services import datadrop


app = FastAPI(
    title="French Commune API", 
    docs_url="/v1", 
    redoc_url="/", 
    version="v1.0"
)


@app.on_event("startup")
def load_data():
    datadrop.api_request()

@app.on_event("shutdown")
def destroy_session():
    pass


app.include_router(lycees.router)
app.include_router(codepostaux.router)
