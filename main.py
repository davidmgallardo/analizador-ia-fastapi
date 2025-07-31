from fastapi import FastAPI
import google.generativeai as genai
import requests
from PIL import Image
import io

app = FastAPI()

@app.post("/analiza-ia")
async def analiza(data: dict):
    url = data.get("url", "")
    api_key = data.get("api-key", "")

    if not url:
        return {"error": "No se proporcionó ninguna URL"}
    
    if not api_key:
        return {"error": "No se proporcionó ninguna API Key"}

    try:
        # Configura Gemini con la API key
        genai.configure(api_key=api_key)

        # Descargar la imagen
        response = requests.get(url)
        if response.status_code != 200:
            return {"error": f"No se pudo descargar la imagen. Código: {response.status_code}"}

        # Convertir bytes a objeto de imagen compatible con Gemini
        image = Image.open(io.BytesIO(response.content))

        # Enviar a Gemini Vision
        model = genai.GenerativeModel("gemini-2.0-flash")
        result = model.generate_content(
            [image, "Describe con detalle lo que ves en esta imagen. ¿Hay personas, objetos o situaciones relevantes?"]
        )

        return {"response": result.text.strip()}

    except Exception as e:
        return {"error": f"Ocurrió un error al procesar la imagen: {str(e)}"}
