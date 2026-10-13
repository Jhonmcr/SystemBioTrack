# Importamos la librería principal de FastAPI
from fastapi import FastAPI

# Inicializamos la aplicación
app = FastAPI(
    title="SystemBioTrack API",
    description="Backend para el sistema de control de asistencia biométrica",
    version="1.0.0"
)

# Ruta raíz de prueba
@app.get("/")
def home():
    return {"status": "ok", "message": "API de SystemBioTrack ejecutándose correctamente"}