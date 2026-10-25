"""
SUMMARY:
Módulo de configuración y conexión a la base de datos PostgreSQL para SystemBioTrack.
Define el motor de conexión SQLAlchemy (Engine_Db), el generador de sesiones
transaccionales (Session_Local) y la clase base declarativa (Base) para el mapeo
de los modelos ORM de asistencia y biométrico.
"""

import os
from typing import Generator
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker, Session

# -------------------------------------------------------------------------
# Variables de entorno y configuración de conexión (Formato: Ejemplo_Variable)
# -------------------------------------------------------------------------
Db_User: str = os.getenv("DB_USER", "postgres")
Db_Password: str = os.getenv("DB_PASSWORD","tu_password_aqui")  # <-- Coloca aquí tu contraseña real de PostgreSQL
Db_Host: str = os.getenv("DB_HOST", "localhost")
Db_Port: str = os.getenv("DB_PORT", "5432")
Db_Name: str = os.getenv("DB_NAME", "asistencia_db")

# Cadena de conexión para SQLAlchemy
Database_Url: str = f"postgresql://{Db_User}:{Db_Password}@{Db_Host}:{Db_Port}/{Db_Name}"

# -------------------------------------------------------------------------
# Creación del motor y fábrica de sesiones
# -------------------------------------------------------------------------
# Motor de conexión a PostgreSQL
Engine_Db = create_engine(Database_Url)

# Fábrica para instanciar sesiones de base de datos
Session_Local = sessionmaker(autocommit=False, autoflush=False, bind=Engine_Db)

# Clase base declarativa para los modelos ORM
Base = declarative_base()


# -------------------------------------------------------------------------
# Inyector de dependencias para FastAPI
# -------------------------------------------------------------------------
def get_db() -> Generator[Session, None, None]:
    """
    SUMMARY:
    Generador de dependencias para FastAPI que provee una sesión de base de datos
    por petición HTTP y asegura su cierre al terminar la operación.
    """
    Db_Session: Session = Session_Local()
    try:
        yield Db_Session
    finally:
        Db_Session.close()