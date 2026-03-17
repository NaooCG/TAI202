#importaciones
from fastapi import FastAPI
from app.router import usuario, misc

#Instancia del servidor
app = FastAPI(
title="Mi Primer API",
description="Naomi Carrillo",
version="1.0.0"
)

app.include_router(usuario.router)
app.include_router(misc.misc)