from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# conexión a SQLite (archivo .db en la raíz del proyecto)
DATABASE_URL = "sqlite:///./galeria.db"

# si estás usando SQLite necesitas este connect_args
engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)

# session para conectarse a la base de datos
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# clase base para tus modelos
Base = declarative_base()
