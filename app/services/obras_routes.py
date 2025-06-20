# app/services/obras_routes.py

import os
import uuid

from fastapi import APIRouter, Depends, HTTPException
from fastapi import UploadFile, File, Form, HTTPException, Depends
from sqlalchemy.orm import Session
from app.core.dependencies import get_db, get_current_user
from app.data.schemas import ObraCrear, ObraRespuesta
from app.data.models import Usuario
from app.business import crud
from app.business.crud import obtener_feed_obras
from app.data.schemas import ObraFeed
from app.business.crud import crear_obra_con_imagen
from app.business.crud import obtener_obras_por_artista

router = APIRouter()

UPLOAD_DIR = "static/uploads"

@router.get("/obras", response_model=list[ObraFeed])
def listar_feed_obras(db: Session = Depends(get_db)):
    obras = obtener_feed_obras(db)

    # mapeamos las obras a dicts con artista_nombre
    resultado = []
    for o in obras:
        resultado.append({
            "id": o.id,
            "titulo": o.titulo,
            "descripcion": o.descripcion,
            "imagen_url": o.imagen_url,
            "fecha_subida": o.fecha_subida,
            "artista_nombre": o.artista.nombre,
            "en_subasta": o.en_subasta
        })

    return resultado

@router.post("/obras/subir", response_model=ObraRespuesta)
def subir_obra(
    titulo: str = Form(...),
    descripcion: str = Form(""),
    imagen: UploadFile = File(...),
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(get_current_user)
):
    if usuario.rol != "artista":
        raise HTTPException(status_code=403, detail="Solo los artistas pueden subir obras")

    # generar nombre único para la imagen
    ext = os.path.splitext(imagen.filename)[1]
    nombre_archivo = f"{uuid.uuid4().hex}{ext}"
    ruta_guardado = os.path.join(UPLOAD_DIR, nombre_archivo)

    # guardar imagen en disco
    with open(ruta_guardado, "wb") as buffer:
        buffer.write(imagen.file.read())

    imagen_url = f"/static/uploads/{nombre_archivo}"

    # guardar obra en la base de datos
    obra = crear_obra_con_imagen(db, titulo, descripcion, imagen_url, usuario.id)

    return obra

@router.get("/mis-obras", response_model=list[ObraFeed])
def listar_mis_obras(db: Session = Depends(get_db), usuario: Usuario = Depends(get_current_user)):
    if usuario.rol != "artista":
        raise HTTPException(status_code=403, detail="Solo los artistas pueden ver sus obras")

    obras = obtener_obras_por_artista(db, usuario.id)

    resultado = []
    for o in obras:
        resultado.append({
            "id": o.id,
            "titulo": o.titulo,
            "descripcion": o.descripcion,
            "imagen_url": o.imagen_url,
            "fecha_subida": o.fecha_subida,
            "artista_nombre": usuario.nombre,
            "en_subasta": o.en_subasta
        })

    return resultado