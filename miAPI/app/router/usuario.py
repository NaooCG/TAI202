from fastapi import FastAPI, status, HTTPException, Depends, APIRouter
from app.models.usuario import crear_usuario, UsuarioUpdate
from app.data.database import usuarios
from app.security.auth import verificar_peticion

from sqlalchemy.orm import Session
from app.data.db import get_db
from app.data.usuario import usuario as dbUsuario

#simplifica no declarar cada endponit 
router=APIRouter(
    prefix="/v1/usuarios",
    tags=["HTTP CRUD"]
)

#Endpoints
#ver todos GET
@router.get("/")
async def consulta(db:Session=Depends(get_db)): #aggrego

    queryUsuarios=db.query(dbUsuario).all() #agrego

    return {
        "total":len(queryUsuarios), #remplazo usuarios por queryUsuarios
        "usuarios":queryUsuarios, #remplazo usuarios por queryUsuarios
        "status":"200"
    }
#ver usuario por id GET
@router.get("/{id}")
async def consulta_usuario_por_id(id: int, db: Session = Depends(get_db)):
    usuario_db = db.query(dbUsuario).filter(dbUsuario.id == id).first()
    if not usuario_db:
        raise HTTPException(status_code=404, detail="usuario no encontrado")

    return {
        "usuario": usuario_db,
        "status": "200"
    }
#crear usuario POST
@router.post("/", status_code=status.HTTP_201_CREATED)
async def agregar_usuario(usuarioP: crear_usuario, db: Session = Depends(get_db)):
    nuevoU = dbUsuario(
        nombre=usuarioP.nombre, 
        edad=usuarioP.edad)
    
    db.add(nuevoU)
    db.commit()
    db.refresh(nuevoU)

    return {
        "mensaje": "usuario agregado",
        "usuario": nuevoU 
    }

#actualizar usuario PUT
@router.put("/{id}", status_code=status.HTTP_200_OK)
async def actualizar_usuario(id: int, usuarioP: crear_usuario, db: Session = Depends(get_db)):
    usuario_db = db.query(dbUsuario).filter(dbUsuario.id == id).first()
    
    if not usuario_db:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    usuario_db.nombre = usuarioP.nombre
    usuario_db.edad = usuarioP.edad
    
    db.commit()
    db.refresh(usuario_db)
    
    return {
        "mensaje": "usuario actualizado",
        "usuario": usuario_db,
        "status": "200"      
    }

#patch actulizar parcialmente 
@router.patch("/{usuario_id}", status_code=status.HTTP_200_OK)
async def actualizar_usuario_parcial(usuario_id: int, usuario: UsuarioUpdate, db: Session = Depends(get_db)):
    usuario_db = db.query(dbUsuario).filter(dbUsuario.id == usuario_id).first()
    
    if not usuario_db:
        raise HTTPException(
            status_code=404, 
            detail="usuario no encontrado"
        )
    
    update_data = usuario.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(usuario_db, key, value)
        
    db.commit()
    db.refresh(usuario_db)
    
    return {
        "mensaje": "usuario actualizado",
        "datos": usuario_db,
        "status": "200"
    }

#eliminar usuario DELETE
@router.delete("/{usuario_id}", status_code=status.HTTP_200_OK)
async def eliminar_usuario(usuario_id: int, usuarioAuth: str = Depends(verificar_peticion), db: Session = Depends(get_db)): 
    usuario_db = db.query(dbUsuario).filter(dbUsuario.id == usuario_id).first()
    
    if not usuario_db:
        raise HTTPException(
            status_code=404, 
            detail="usuario no encontrado"
        )
    
    db.delete(usuario_db)
    db.commit()
    
    return {
        "mensaje": f"usuario con ID {usuario_id} eliminado por {usuarioAuth}",
        "status": "200"      
    }
