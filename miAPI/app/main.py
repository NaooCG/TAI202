#importaciones
from fastapi import FastAPI
from app.router import usuario, misc
from app.data.db import engine
from app.data import usuario as usuarioDB

#Creación de tablas
usuarioDB.Base.metadata.create_all(bind=engine)

#Instancia del servidor
app = FastAPI(
title="Mi Primer API",
description="Naomi Carrillo",
version="1.0.0"
)

app.include_router(usuario.router)
app.include_router(misc.misc)