from pydantic import BaseModel, Field #agrega basemodel pydantic
from typing import Optional

#*********
#modelo de validacion pydantic # se crea el modelo #agregamos validaciones perzonalizadas
#*********
class crear_usuario(BaseModel):
    nombre:str =Field(..., min_length=3,max_length=50,example="juanita")
    edad:int = Field (..., ge=1,le=123,description="edad valida entre 1 y 123")

#*********
# modelo para actualizar parcialmente
#*********
class UsuarioUpdate(BaseModel):
    # Usamos Optional y None, pero mantenemos tus mismas validaciones
    nombre: Optional[str] = Field(None, min_length=3, max_length=50, example="juanita")
    edad: Optional[int] = Field(None, ge=1, le=123, description="edad valida entre 1 y 123")