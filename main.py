from fastapi import FastAPI, Request

app = FastAPI()

@app.post("/analiza")
async def analiza(data: dict):
    url = data.get("url", "")
    return {"response": f"Imagen recibida: {url}"}
