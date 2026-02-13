#importaciones
from fastapi import FastAPI
import asyncio

#Intancia del objeto/servidor
app = FastAPI()

#Endspoints (ubucacion de los recursos/rutas)
@app.get("/")
async def holamundo():
    return {"mensaje":"Hola mundo FastAPI"}

@app.get("/bienvenido")
async def bienvenido():
    await asyncio.sleep(5)
    return {
        "mensaje":"Hola mundo FastAPI",
        "estatus":"200"
        }
#Endspoints con parametros obligatorios
@app.get("/saludo/{nombre}")
async def saludar(nombre: str):
    return {"mensaje": f"Hola {nombre}"}

#Endspoints con parametros opcionales
from typing import Optional

@app.get("/usuario/")
async def obtener_usuario(edad: Optional[int] = None):
    if edad:
        return {"mensaje": f"Tienes {edad} años"}
    return {"mensaje": "No enviaste edad"}
