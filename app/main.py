from fastapi import FastAPI

from app.routers import condominio

app = FastAPI(title="Meu Porteiro")

app.include_router(condominio.router)


@app.get("/saude")
def saude():
    return {"status": "ok"}