from fastapi import FastAPI
import google.generativeai as genai
import requests

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
        # Configura Gemini con la API key recibida
        genai.configure(api_key=api_key)

        # Descargar la imagen
        response = requests.get(url)
        if response.status_code != 200:
            return {"error": f"No se pudo descargar la imagen. Código: {response.status_code}"}

        image_data = response.content

        # Analizar con Gemini
        model = genai.GenerativeModel("gemini-pro-vision")
        result = model.generate_content(
            [image_data, "Describe con detalle lo que ves en esta imagen. ¿Hay personas, objetos o situaciones relevantes?"]
        )

        return {"response": result.text.strip()}

    except Exception as e:
        return {"error": f"Ocurrió un error al procesar la imagen: {str(e)}"}
