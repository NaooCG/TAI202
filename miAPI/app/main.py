#importaciones
from fastapi import FastAPI
from fastapi import FastAPI, status, HTTPException
import asyncio
from typing import Optional

#Instancia del servidor
app = FastAPI(
title="Mi Primer API",
description="Naomi Carrillo",
version="1.0.0"
)

#TB ficticia
usuarios=[
    {"id":1,"nombre":"Fany","edad":21},
    {"id":2,"nombre":"Aly","edad":21},
    {"id":3,"nombre":"Dulce","edad":21},
]

#Intancia del objeto/servidor
app = FastAPI()

#Endspoints (ubucacion de los recursos/rutas)
#Endpoints
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
@app.get("/v1/ParametroOb/{id}", tags=["Parametro obligatorio"])
async def consultauno(id:int):
    return {"mensaje": "Usuario encontrado", 
            "usuario":id,
            "status":"200"
            }

@app.get("/v1/ParametroOp/", tags=["Parametro opcional"])
async def consultatodos(id:Optional[int]=None):
    if id is not None: 
        for usuariok in usuarios:
            if usuariok["id"] == id:
                return {"mensaje":"Usuario encontrado","usuario":usuariok,"status":"200"}
        return {"mensaje":"Usuario no encontrado","status":"200"}
    else:
        return {"mensaje":"No se proporciono un id","status":"200"}
    
@app.get("/v1/usuarios/", tags=["CRUD HTTP"])
async def consulta():
    return {
        "total":len(usuarios),
        "usuarios":usuarios,
        "status":"200"
    }

@app.post("/v1/usuarios/", tags=["CRUD HTTP"])
async def agregar_usuario(usuario: dict):
    for usr in usuarios:
        if usr["id"] == usuario.get("id"):
            raise HTTPException(
                status_code= 400, 
                detail="El id ya existe"
                )
    usuarios.append(usuario)
    return {
        "mensaje":"usuario agregado",
        "usuario":usuario,
        "status":"200"      
    }

@app.put("/v1/usuarios/{id}", tags=["CRUD HTTP"])
async def actualizar_usuario(id:int, usuario: dict):
    for index, usr in enumerate(usuarios):
        if usr["id"] == id:
            usuario["id"] = id
            usuarios[index] = usuario
            return {
                "mensaje":"usuario actualizado",
                "usuario":usuario,
                "status":"200"      
            }
    raise HTTPException(
        status_code= 404, 
        detail="usuario no encontrado"
        )

@app.get("/usuario/")
async def obtener_usuario(edad: Optional[int] = None):
    if edad:
        return {"mensaje": f"Tienes {edad} años"}
@app.delete("/v1/usuarios/", tags=["CRUD HTTP"])
async def eliminar_usuario(id:int): 
    for index, usr in enumerate(usuarios):
        if usr["id"] == id:
            del usuarios[index]
            return {
                "mensaje":"usuario eliminado",
                "status":"200"      
            }
    raise HTTPException(
        status_code= 404, 
        detail="usuario no encontrado"
        )