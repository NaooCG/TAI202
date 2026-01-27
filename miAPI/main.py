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