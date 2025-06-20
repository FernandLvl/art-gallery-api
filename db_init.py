from app.data.database import Base, engine
from app.data import models
import os

print("Creando la base de datos SQLite con las tablas...")
Base.metadata.create_all(bind=engine)
print("¡Base de datos creada con éxito! galeria.db")
os.makedirs("static/uploads", exist_ok=True)