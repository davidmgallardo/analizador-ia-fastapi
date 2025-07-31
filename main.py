from fastapi import FastAPI, Request
import google.generativeai as genai
import requests

app = FastAPI()

# Configura tu clave de API de Gemini
genai.configure(api_key="AIzaSyCDk77qutgA8jnKBAKTNhNpHh_A2z-yYbE")

@app.post("/analiza")
async def analiza(data: dict):
    url = data.get("url", "")
    
    if not url:
        return {"error": "No se proporcionó ninguna URL"}

    try:
        # Descargar imagen desde la URL
        response = requests.get(url)
        if response.status_code != 200:
            return {"error": f"No se pudo descargar la imagen. Código: {response.status_code}"}

        image_data = response.content

        # Enviar imagen a Gemini Vision para análisis
        model = genai.GenerativeModel("gemini-pro-vision")
        result = model.generate_content(
            [image_data, "Describe con detalle lo que ves en esta imagen. ¿Hay personas, objetos o situaciones relevantes?"]
        )

        return {"response": result.text.strip()}

    except Exception as e:
        return {"error": f"Ocurrió un error al procesar la imagen: {str(e)}"}
