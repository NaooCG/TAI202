from fastapi import FastAPI, status, HTTPException, Depends, APIRouter
from app.models.usuario import crear_usuario
from app.data.database import usuarios
from app.security.auth import verificar_peticion

#simplifica no declarar cada endponit 
router=APIRouter(
    prefix="/v1/usaurios",
    tags=["HTTP CRUD"]
)

#Endpoints
@router.get("/")
async def consulta():
    return {
        "total":len(usuarios),
        "usuarios":usuarios,
        "status":"200"
    }

@router.post("/", status_code=status.HTTP_201_CREATED)
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

@router.put("/{id}", status_code=status.HTTP_200_OK)
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
#edito eliminar usuario y se agrea para que desde verificar_peticion decida si lo deja pasar o no
@router.delete("/{id}", status_code=status.HTTP_200_OK)
async def eliminar_usuario(id:int, usuarioAuth:str=Depends(verificar_peticion)): 
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