#importaciones
from fastapi import FastAPI, status, HTTPException
import asyncio
from typing import Optional
from pydantic import BaseModel, Field #agrega basemodel pydantic

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

#*********
#modelo de validacion pydantic # se crea el modelo #agregamos validaciones perzonalizadas
#*********
class crear_usuario(BaseModel):
    id:int = Field(...,gt=0, description="identificador de usuario")
    nombre:str =Field(..., min_length=3,max_length=50,example="juanita")
    edad:int = Field (..., ge=1,le=123,description="edad valida entre 1 y 123")

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
                return {"mensaje":"Usuario encontrado",
                        "usuario":usuariok}
        return {"mensaje":"usuario no encontrado","status":"200"}
    else:
        return {"mensaje":"No se proporciono un id","status":"200"}
    
@app.get("/v1/usuarios/", tags=["HTTP CRUD"])
async def consulta():
    return {
        "total":len(usuarios),
        "usuarios":usuarios,
        "status":"200"
    }

@app.post("/v1/usuarios/", tags=["HTTP CRUD"], status_code=status.HTTP_201_CREATED)
async def agregar_usuario(usuario:crear_usuario): #SE USA EL MODELO
    for usr in usuarios:
        if usr["id"] == usuario.id: #cambia porque ya no usamos dict
            raise HTTPException(
                status_code= 400, 
                detail="El id ya existe"
                )
    usuarios.append(usuario)
    return {
        "mensaje":"usuario agregado",
        "usuario":usuario 
    }

@app.put("/v1/usuarios/{id}", tags=["HTTP CRUD"])
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

@app.delete("/v1/usuarios/", tags=["HTTP CRUD"])
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