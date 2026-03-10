#importaciones
from fastapi import FastAPI, status, HTTPException, Depends
import asyncio
from typing import Optional
from pydantic import BaseModel, Field
from fastapi.security import HTTPBasic, HTTPAuthorizationCredentials,HTTPBasicCredentials
import secrets 

usuarios= [
    {"id": 1, "nombre":"Fanny","edad":20},
    {"id": 2, "nombre":"Aurora","edad":24},
    {"id": 3, "nombre":"Felipe","edad":28}
]

security = HTTPBasic()

usuario = "admin"
contraseña = "rest123"

class Usuario (BaseModel):
    nombre: str=Field (...,min_length=6, description="nombre")


class crear_reserva(BaseModel):
    id:int = Field (...,gt=0, description="Indentificacion de usaurio")
    nombre:str=Field(..., min_length=6,max_length=50,example="juanita")

@app.post("/v1/reserva",)














