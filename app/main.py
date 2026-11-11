from fastapi import FastAPI

app = FastAPI(title="Meu Porteiro")

@app.get("/saude")
def saude():
    return {"status": "ok"}