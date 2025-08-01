from fastapi import FastAPI
import google.generativeai as genai
import requests
from PIL import Image
import io
import paho.mqtt.publish as publish

app = FastAPI()

@app.post("/analiza-ia")
async def analiza(data: dict):
    url = data.get("url", "")
    api_key = data.get("api_key", "")

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
            [image, "Analiza cuidadosamente esta imagen capturada por una cámara de seguridad. Ignora detalles irrelevantes como el césped, las paredes, objetos pequeños o el mobiliario. Concéntrate exclusivamente en las personas que aparecen: ¿Cuántas hay? ¿Qué están haciendo exactamente? ¿Dónde están ubicadas en la escena? ¿Qué ropa llevan puesta (colores, tipo de prenda)? ¿Llevan objetos o mochilas? ¿Están mirando a cámara, encapuchadas o cubriendo su rostro? ¿Presentan comportamientos o posturas que puedan parecer sospechosas o inusuales (por ejemplo: mirar constantemente alrededor, moverse con sigilo, esconder algo, forzar entradas, etc.)? Sé preciso y conciso en la descripción de cada persona y su comportamiento. El objetivo es evaluar si hay actividad sospechosa en la escena."]
        )

        resultado_texto = result.text.strip()

        # Publicar resultado por MQTT
        publish.single(
            topic="frigate/ia/resultado",
            payload=resultado_texto,
            hostname="192.168.68.84",   # Cambia por la IP de tu broker MQTT
            port=1883,
            auth={
                "username": "mosquitto",      # Opcional si tu broker lo requiere
                "password": "nYxte2-gYvc@x-goqs1*"
            }
        )

        return resultado_texto

    except Exception as e:
        return {"error": f"Ocurrió un error al procesar la imagen: {str(e)}"}
