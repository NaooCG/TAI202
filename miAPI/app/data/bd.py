from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

#1, definimos la URL dde conexion
DATABASE_URL= os.getenv(
    "DATABASE_URL",
    "postgresql://admin:123456@postgres:5432/DB_miapi"
)

#2. creamos el motor conexion
engine= create_engine(DATABASE_URL)

#3. preparamos el gestionador de sessiones
SessionLocal=sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

#4. base declarativa del modelo
Base=declarative_base()

#5. obtener sesiones de cada peticion
def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()