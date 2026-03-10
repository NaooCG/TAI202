#importaciones
from fastapi import FastAPI, status, HTTPException, Depends
import asyncio
from typing import Optional
from pydantic import BaseModel, Field
from fastapi.security import HTTPBasic, HTTPAuthorizationCredentials,HTTPBasicCredentials
import secrets 
from typing import Literal, List, Optional
from datetime import datetime, timedelta

app = FastAPI(
title="exam",
description="Naomi Carrillo",
version="1.0.0"
)

reserva= [
    {"id": 1, "nombre":"Fanny","edad":20},
    {"id": 2, "nombre":"Aurora","edad":24},
    {"id": 3, "nombre":"Felipe","edad":28}
]

security = HTTPBasic()

usuario = "admin"
contraseña = "rest123"



class crear_reserva (BaseModel):
    mesa: str=Field (...,min_length=6, description="mesa")

class Usuario(BaseModel):
    id:int = Field (...,gt=0, description="Indentificacion de usaurio")
    nombre:str=Field(..., min_length=6,max_length=50,example="juanita")
    fecha_hora: datetime = Field(...)
    num_personas: int = Field(..., min_length=1, max_length=10)
    confirmada: bool = Field(default=False)


@app.post("/v1/reserva/", tags=["reserva"], status_code=status.HTTP_201_CREATED)
async def agregar_reserva(reserva: crear_reserva): 
    if not reserva.nombre or len(reserva.nombre) < 6 or len(reserva.nombre) > 100:
        raise HTTPException(
            status_code= 400, 
            detail="faltan datos o el nombre "
        )
    reserva.append(reserva.model_dump()) 
    return {
        "mensaje": "registrado",
        "reserva": reserva,
        "status": "201" 
    }

@app.get("/v1/reserva/lista", tags=["reserva"])
async def consulta_reserva():
    reservas_dis=[res for res in reserva if res["estado"]]
    return{
        "total": len(reservas_dis),
        "reservas": reservas_dis,
        "status": "200"
    }

@app.get("/v1/reservas/{id}/consulta", tags=["reservas"])
async def consultar_reserva(id: int):
    for r in reserva:
        if r["id"] == id:
            return {"status": 200, "data": r}

    raise HTTPException(
        status_code=404,
        detail=f"reserva con id {id} no encontrada"
    )

@app.delete("/v1/reservas/{id}/cancelar", tags=["Reservas"])
async def cancelar_reserva(id: int, usuario_auth: str = Depends(verificar_credenciales)):
    for idx, r in enumerate(reserva):
        if r["id"] == id:
            eliminada = reserva[idx]
            del reserva[idx]
            return {
                "mensaje": "reserva eliminada",
                "usuario_autorizado": usuario_auth,
                "data": eliminada,
                "status": 200
            }

    raise HTTPException(
        status_code=404,
        detail=f"reserva eliminada"
    )
