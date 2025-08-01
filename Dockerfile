FROM python:3.11-slim

WORKDIR /app

# Instala FastAPI, Uvicorn y Google Gemini client
RUN pip install fastapi uvicorn google-generativeai requests pillow paho-mqtt

COPY main.py .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "5000"]
