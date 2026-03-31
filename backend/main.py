from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.recomendador import recomendar_destinos
from backend.auth import router as auth_router
from backend.database import crear_base_datos
from backend.uso import obtener_uso, incrementar_uso

import sqlite3
import os

# 👉 Ruta DB
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "..", "travel_ai.db")

app = FastAPI(title="Travel AI API")

# 👉 Crear base de datos al iniciar (usuarios + uso)
crear_base_datos()

# 👉 Rutas de autenticación
app.include_router(auth_router)

# 👉 CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 👉 Endpoint base
@app.get("/")
def inicio():
    return {"mensaje": "API de viajes con IA funcionando"}


# 🔥 FUNCIÓN PARA OBTENER PLAN DEL USUARIO
def obtener_plan(email):
    conexion = sqlite3.connect(DB_PATH)
    cursor = conexion.cursor()

    cursor.execute("SELECT plan FROM usuarios WHERE email=?", (email,))
    resultado = cursor.fetchone()

    conexion.close()

    # 👉 Si no existe usuario → lo tratamos como FREE
    if resultado:
        return resultado[0]
    return "free"


# 👉 Endpoint SaaS con control de uso
@app.get("/recomendar")
def recomendar(presupuesto: int, tipo: str, email: str):

    # 👉 Validación básica
    if not email:
        return {"error": "Email requerido"}

    plan = obtener_plan(email)

    # 👉 PLAN FREE
    if plan == "free":
        try:
            uso_actual = obtener_uso(email)
        except Exception:
            uso_actual = 0  # fallback seguro

        if uso_actual >= 3:
            return {
                "error": "Has alcanzado el límite FREE (3 consultas). Pásate a PRO 🚀"
            }

        # 👉 Incrementar uso
        try:
            incrementar_uso(email)
        except Exception:
            pass  # evitar caída si falla

        resultados = recomendar_destinos(presupuesto, tipo)

        return {
            "plan": "free",
            "consultas_usadas": uso_actual + 1,
            "recomendaciones": resultados
        }

    # 👉 PLAN PRO
    resultados = recomendar_destinos(presupuesto, tipo)

    return {
        "plan": "pro",
        "recomendaciones": resultados
    }


# 👉 PARA EJECUCIÓN LOCAL (opcional)
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=True)