from fastapi import FastAPI
from routers import lycees, codepostaux


app = FastAPI(
    title="French Commune API", 
    docs_url="/v1", 
    redoc_url="/", 
    version="v1.0"
)


app.include_router(lycees.router)
app.include_router(codepostaux.router)
