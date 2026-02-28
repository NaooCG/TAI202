from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Literal, List, Optional

#Instancia del servidor
app = FastAPI(
title="Mi Primer API",
description="Naomi Carrillo",
version="1.0.0"
)

#TB ficticia
libros = [
    {
        "nombre": "El Psicoanalista",
        "autor": "John Katzenbach",
        "anio": 2002,
        "paginas": 432,
        "estado": "disponible"
    },
    {
        "nombre": "Jaque al psicoanalista",
        "autor": "John Katzenbach",
        "anio": 2018,
        "paginas": 400,
        "estado": "disponible"
    },
    {
        "nombre": "El niño con el pijama de rayas",
        "autor": "John Boyne",
        "anio": 2006,
        "paginas": 264,
        "estado": "prestado"
    }
]

prestamos = [
    {
        "nombre_libro": "El niño con el pijama de rayas",
        "usuario": {
            "nombre": "Nao Carrillo",
            "correo": "nao@gmail.com"
        }
    }
]

#*********
#modelo de validacion pydantic # se crea el modelo #agregamos validaciones perzonalizadas
#*********
class Usuario(BaseModel):
    nombre: str = Field(..., min_length=2, description="nombre del usuario")
    correo: EmailStr = Field(..., description="correo electronico")

class Libro(BaseModel):
    nombre: str = Field(..., min_length=2, max_length=100) 
    anio: int = Field(..., gt=1450, le=datetime.now().year)
    paginas: int = Field(..., gt=1)
    estado: Literal["disponible", "prestado"] = Field(default="disponible")

class Prestamo(BaseModel):
    nombre_libro: str = Field(..., min_length=2, max_length=100)
    usuario: Usuario

#Endpoints
@app.post("/v1/libros/", tags=["Libros"], status_code=status.HTTP_201_CREATED)
async def agregar_libro(libro: Libro): 
    if not libro.nombre or len(libro.nombre) < 2 or len(libro.nombre) > 100:
        raise HTTPException(
            status_code= 400, 
            detail="faltan datos o el nombre del libro no es valido"
        )
    libros.append(libro.model_dump()) 
    return {
        "mensaje": "libro registrado",
        "libro": libro,
        "status": "201" 
    }

@app.get("/v1/libros/", tags=["Libros"])
async def consulta_libros_disponibles():
    libros_disponibles = [lib for lib in libros if lib["estado"] == "disponible"]
    return {
        "total": len(libros_disponibles),
        "libros": libros_disponibles,
        "status": "200"
    }

@app.get("/v1/libros/{nombre}", tags=["Libros"])
async def buscar_libro(nombre: str):
    for lib in libros:
        if lib["nombre"].lower() == nombre.lower():
            return {
                "mensaje": "libro encontrado",
                "libro": lib,
                "status": "200"
            }
    raise HTTPException(
        status_code= 404, 
        detail="libro no encontrado"
    )

@app.post("/v1/prestamos/", tags=["Prestamos"], status_code=status.HTTP_201_CREATED)
async def agregar_prestamo(prestamo: Prestamo):
    for lib in libros:
        if lib["nombre"].lower() == prestamo.nombre_libro.lower():
            if lib["estado"] == "prestado":
                raise HTTPException(
                    status_code= 409, 
                    detail="el libro esta prestado"
                )
            
            lib["estado"] = "prestado"
            prestamos.append(prestamo.model_dump())
            return {
                "mensaje": "prestamo registrado",
                "prestamo": prestamo,
                "status": "201"
            }
            
    raise HTTPException(
        status_code= 404, 
        detail="libro no encontrado"
    )

@app.put("/v1/prestamos/devolver/{nombre}", tags=["Prestamos"])
async def devolver_libro(nombre: str):
    for lib in libros:
        if lib["nombre"].lower() == nombre.lower():
            lib["estado"] = "disponible"
            return {
                "mensaje": "libro devuelto",
                "status": "200"
            }
            
    raise HTTPException(
        status_code= 404, 
        detail="libro no encontrado"
    )

@app.delete("/v1/prestamos/{nombre}", tags=["Prestamos"])
async def eliminar_prestamo(nombre: str): 
    for index, prest in enumerate(prestamos):
        if prest["nombre_libro"].lower() == nombre.lower():
            del prestamos[index]
            return {
                "mensaje": "registro de prestamo eliminado",
                "status": "200"      
            }
            
    raise HTTPException(
        status_code= 409, 
        detail="el registro de prestamo ya no existe" 
    )