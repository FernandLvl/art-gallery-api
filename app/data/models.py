from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Enum, Float, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from app.data.database import Base
import enum

# enumeración para el rol del usuario
class RolEnum(str, enum.Enum):
    artista = "artista"
    observador = "observador"

# enumeración para el estado de la subasta
class EstadoSubastaEnum(str, enum.Enum):
    activa = "activa"
    cerrada = "cerrada"

# tabla usuario
class Usuario(Base):
    __tablename__ = "usuario"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    rol = Column(Enum(RolEnum), nullable=False)

    obras = relationship("ObraDeArte", back_populates="artista", cascade="all, delete")
    ofertas = relationship("Oferta", back_populates="usuario", cascade="all, delete")

# tabla obra_de_arte
class ObraDeArte(Base):
    __tablename__ = "obra_de_arte"

    id = Column(Integer, primary_key=True, autoincrement=True)
    titulo = Column(String(150), nullable=False)
    descripcion = Column(Text)
    imagen_url = Column(String(255))
    fecha_subida = Column(DateTime, default=datetime.utcnow)
    artista_id = Column(Integer, ForeignKey("usuario.id", ondelete="CASCADE", onupdate="CASCADE"), nullable=False)
    en_subasta = Column(Boolean, default=False)

    artista = relationship("Usuario", back_populates="obras")
    subasta = relationship("Subasta", back_populates="obra", uselist=False, cascade="all, delete")

# tabla subasta
class Subasta(Base):
    __tablename__ = "subasta"

    id = Column(Integer, primary_key=True, autoincrement=True)
    obra_id = Column(Integer, ForeignKey("obra_de_arte.id", ondelete="CASCADE", onupdate="CASCADE"), nullable=False, unique=True)
    precio_inicio = Column(Float, nullable=False)
    precio_actual = Column(Float, nullable=False)
    fecha_inicio = Column(DateTime, nullable=False)
    fecha_fin = Column(DateTime, nullable=False)
    estado = Column(Enum(EstadoSubastaEnum), default=EstadoSubastaEnum.activa, nullable=False)

    obra = relationship("ObraDeArte", back_populates="subasta")
    ofertas = relationship("Oferta", back_populates="subasta", cascade="all, delete")

# tabla oferta
class Oferta(Base):
    __tablename__ = "oferta"

    id = Column(Integer, primary_key=True, autoincrement=True)
    subasta_id = Column(Integer, ForeignKey("subasta.id", ondelete="CASCADE", onupdate="CASCADE"), nullable=False)
    usuario_id = Column(Integer, ForeignKey("usuario.id", ondelete="CASCADE", onupdate="CASCADE"), nullable=False)
    cantidad = Column(Float, nullable=False)
    fecha = Column(DateTime, default=datetime.utcnow)

    subasta = relationship("Subasta", back_populates="ofertas")
    usuario = relationship("Usuario", back_populates="ofertas")
