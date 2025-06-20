# app/services/ofertas_routes.py

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.dependencies import get_db, get_current_user
from app.data.models import Usuario
from app.business.crud import hacer_oferta, obtener_ofertas_usuario
from app.data.schemas import MisOfertasRespuesta, OfertaCrear, OfertaRespuesta
from fastapi import HTTPException

router = APIRouter()

@router.post("/ofertas/hacer", response_model=OfertaRespuesta)
def crear_oferta(
    datos: OfertaCrear,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(get_current_user)
):
    if usuario.rol != "observador":
        raise HTTPException(status_code=403, detail="Solo los observadores pueden hacer ofertas")

    return hacer_oferta(db, usuario.id, datos)

@router.get("/mis-ofertas", response_model=list[MisOfertasRespuesta])
def listar_mis_ofertas(
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(get_current_user)
):
    if usuario.rol != "observador":
        raise HTTPException(status_code=403, detail="Solo los observadores pueden ver sus ofertas")

    ofertas = obtener_ofertas_usuario(db, usuario.id)

    respuesta = []
    for o in ofertas:
        respuesta.append({
            "cantidad": o.cantidad,
            "fecha": o.fecha,
            "subasta_id": o.subasta.id,
            "precio_actual": o.subasta.precio_actual,
            "titulo": o.subasta.obra.titulo,
            "imagen_url": o.subasta.obra.imagen_url,
            "artista_nombre": o.subasta.obra.artista.nombre
        })

    return respuesta