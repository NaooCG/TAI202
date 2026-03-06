#importaciones
from fastapi import FastAPI, status, HTTPException, Depends #agrego
import asyncio
from typing import Optional
from pydantic import BaseModel, Field #agrega basemodel pydantic
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm#primer impor OAuth
import secrets #se agrego
from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext

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

#*********
#Configuraciones OAuth2
#*********
SECRET_KEY = "miAPIJWT"
ALGORITHM = "HS256"

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
users_db = {
    "NaoCG": {
        "username": "NaoCG",
        "hashed_password": pwd_context.hash("123456")
    }
}

#*********
#generacion de tokens (incluir limite max 30 minutos) OAuth2
#*********
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def crear_token(data: dict):
    para_codificar = data.copy()
    expiracion = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    para_codificar.update({"exp": expiracion})
    token_jwt = jwt.encode(para_codificar, SECRET_KEY, algorithm=ALGORITHM)
    return token_jwt

#*********
#validacion de tokens 
#*********
async def obtener_usuario(token: str = Depends(oauth2_scheme)):
    excepcion_credenciales = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="token invalido o expirado",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise excepcion_credenciales
        return username
    except JWTError:
        raise excepcion_credenciales

#Endpoints
#*********
#tokens 
#*********
@app.post("/token", tags=["autenticacion"])
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = users_db.get(form_data.username)
    if not user or not pwd_context.verify(form_data.password, user["hashed_password"]):
        raise HTTPException(status_code=400, detail="contraseña o usuario incorrecto ")
    access_token = crear_token(data={"sub": user["username"]})
    return {"access_token": access_token, "token_type": "bearer"}




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
    usuarios.append(usuario.model_dump())
    return {
        "mensaje":"usuario agregado",
        "usuario":usuario 
    }

#*********
#metodos editados 
#*********
@app.put("/v1/usuarios/{id}", tags=["HTTP CRUD"])
async def actualizar_usuario(id: int, usuario: dict, usuarioAuth: str = Depends(obtener_usuario)):
    for index, usr in enumerate(usuarios):
        if usr["id"] == id:
            usuario["id"] = id
            usuarios[index] = usuario
            return {
                "mensaje":f"usuario actualizado por {usuarioAuth}",
                "usuario":usuario,
                "status":"200"      
            }
    raise HTTPException(
        status_code= 404, 
        detail="usuario no encontrado"
        )

@app.delete("/v1/usuarios/", tags=["HTTP CRUD"])
async def eliminar_usuario(id: int, usuarioAuth: str = Depends(obtener_usuario)): 
    for index, usr in enumerate(usuarios):
        if usr["id"] == id:
            del usuarios[index]
            return {
                "mensaje":f"usuario eliminado por {usuarioAuth}",
                "status":"200"      
            }
    raise HTTPException(
        status_code= 404, 
        detail="usuario no encontrado"
        )