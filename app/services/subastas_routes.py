# app/services/subastas_routes.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.dependencies import get_db, get_current_user
from app.data.models import Usuario
from app.data.schemas import SubastaCrear, SubastaDetalle, SubastaRespuesta
from app.business.crud import iniciar_subasta, obtener_detalle_subasta
from app.data.schemas import SubastaFeed
from app.business.crud import obtener_subastas_activas

router = APIRouter()

@router.get("/subastas", response_model=list[SubastaFeed])
def listar_subastas_activas(db: Session = Depends(get_db)):
    subastas = obtener_subastas_activas(db)

    resultado = []
    for s in subastas:
        resultado.append({
            "id": s.id,
            "precio_inicio": s.precio_inicio,
            "precio_actual": s.precio_actual,
            "fecha_inicio": s.fecha_inicio,
            "fecha_fin": s.fecha_fin,
            "estado": s.estado,

            "obra_id": s.obra.id,
            "titulo": s.obra.titulo,
            "imagen_url": s.obra.imagen_url,
            "artista_nombre": s.obra.artista.nombre
        })

    return resultado

@router.post("/subastas/iniciar", response_model=SubastaRespuesta)
def crear_subasta(
    datos: SubastaCrear,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(get_current_user)
):
    if usuario.rol != "artista":
        raise HTTPException(status_code=403, detail="Solo los artistas pueden iniciar subastas")

    return iniciar_subasta(db, usuario.id, datos)

@router.get("/explorar-subastas", response_model=list[SubastaFeed])
def explorar_subastas(db: Session = Depends(get_db)):
    subastas = obtener_subastas_activas(db)

    resultado = []
    for s in subastas:
        resultado.append({
            "id": s.id,
            "precio_inicio": s.precio_inicio,
            "precio_actual": s.precio_actual,
            "fecha_inicio": s.fecha_inicio,
            "fecha_fin": s.fecha_fin,
            "estado": s.estado,

            "obra_id": s.obra.id,
            "titulo": s.obra.titulo,
            "imagen_url": s.obra.imagen_url,
            "artista_nombre": s.obra.artista.nombre
        })

    return resultado

@router.get("/subasta/{id}", response_model=SubastaDetalle)
def ver_subasta(id: int, db: Session = Depends(get_db)):
    return obtener_detalle_subasta(db, id)
