from pydantic import BaseModel, Field #agrega basemodel pydantic

#*********
#modelo de validacion pydantic # se crea el modelo #agregamos validaciones perzonalizadas
#*********
class crear_usuario(BaseModel):
    id:int = Field(...,gt=0, description="identificador de usuario")
    nombre:str =Field(..., min_length=3,max_length=50,example="juanita")
    edad:int = Field (..., ge=1,le=123,description="edad valida entre 1 y 123")