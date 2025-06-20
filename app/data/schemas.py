from pydantic import BaseModel, EmailStr, Field
from enum import Enum
from typing import Optional
from datetime import datetime

class RolEnum(str, Enum):
    artista = "artista"
    observador = "observador"

class UsuarioCrear(BaseModel):
    nombre: str
    email: EmailStr
    password: str
    rol: RolEnum

class UsuarioRespuesta(BaseModel):
    id: int
    nombre: str
    email: EmailStr
    rol: RolEnum

    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str



class ObraCrear(BaseModel):
    titulo: str
    descripcion: Optional[str] = None
    imagen_url: str  # la ruta relativa o URL de la imagen

class ObraRespuesta(BaseModel):
    id: int
    titulo: str
    descripcion: Optional[str]
    imagen_url: Optional[str]
    fecha_subida: datetime
    artista_id: int
    en_subasta: bool

    class Config:
        orm_mode = True


class ObraFeed(BaseModel):
    id: int
    titulo: str
    descripcion: Optional[str]
    imagen_url: Optional[str]
    fecha_subida: datetime
    artista_nombre: str  # agregamos esto como campo calculado
    en_subasta: bool

    class Config:
        orm_mode = True



class SubastaCrear(BaseModel):
    obra_id: int
    precio_inicio: float = Field(..., gt=0)
    fecha_inicio: datetime
    fecha_fin: datetime

class SubastaRespuesta(BaseModel):
    id: int
    obra_id: int
    precio_inicio: float
    precio_actual: float
    fecha_inicio: datetime
    fecha_fin: datetime
    estado: str

    class Config:
        orm_mode = True


class SubastaFeed(BaseModel):
    id: int
    precio_inicio: float
    precio_actual: float
    fecha_inicio: datetime
    fecha_fin: datetime
    estado: str

    obra_id: int
    titulo: str
    imagen_url: Optional[str]
    artista_nombre: str

    class Config:
        orm_mode = True



class OfertaCrear(BaseModel):
    subasta_id: int
    cantidad: float = Field(..., gt=0)

class OfertaRespuesta(BaseModel):
    id: int
    subasta_id: int
    usuario_id: int
    cantidad: float
    fecha: datetime

    class Config:
        orm_mode = True


class OfertaSimple(BaseModel):
    cantidad: float
    fecha: datetime
    usuario_id: int

    class Config:
        orm_mode = True

class SubastaDetalle(BaseModel):
    id: int
    precio_inicio: float
    precio_actual: float
    fecha_inicio: datetime
    fecha_fin: datetime
    estado: str

    titulo: str
    descripcion: str
    imagen_url: Optional[str]
    artista_nombre: str

    ofertas: list[OfertaSimple]

    class Config:
        orm_mode = True


class MisOfertasRespuesta(BaseModel):
    cantidad: float
    fecha: datetime
    subasta_id: int
    precio_actual: float
    titulo: str
    imagen_url: Optional[str]
    artista_nombre: str

    class Config:
        orm_mode = True
