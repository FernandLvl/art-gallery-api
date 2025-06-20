# app/business/crud.py

from app.data.models import ObraDeArte
from app.data.schemas import ObraCrear, OfertaCrear
from sqlalchemy.orm import Session, joinedload
from app.data.models import Subasta, ObraDeArte
from app.data.models import Oferta, Subasta
from sqlalchemy.orm import Session
from datetime import datetime
from fastapi import HTTPException

def crear_obra(db: Session, datos: ObraCrear, artista_id: int):
    obra = ObraDeArte(
        titulo=datos.titulo,
        descripcion=datos.descripcion,
        imagen_url=datos.imagen_url,
        artista_id=artista_id,
        en_subasta=False
    )
    db.add(obra)
    db.commit()
    db.refresh(obra)
    return obra

def obtener_feed_obras(db: Session):
    # joinedload permite traer al artista junto con la obra
    obras = db.query(ObraDeArte)\
        .options(joinedload(ObraDeArte.artista))\
        .order_by(ObraDeArte.fecha_subida.desc())\
        .all()

    return obras

def crear_obra_con_imagen(db: Session, titulo: str, descripcion: str, imagen_url: str, artista_id: int):
    obra = ObraDeArte(
        titulo=titulo,
        descripcion=descripcion,
        imagen_url=imagen_url,
        fecha_subida=datetime.utcnow(),
        artista_id=artista_id,
        en_subasta=False
    )
    db.add(obra)
    db.commit()
    db.refresh(obra)
    return obra

def obtener_obras_por_artista(db: Session, artista_id: int):
    obras = db.query(ObraDeArte)\
        .filter(ObraDeArte.artista_id == artista_id)\
        .order_by(ObraDeArte.fecha_subida.desc())\
        .all()
    return obras

def iniciar_subasta(db: Session, artista_id: int, datos):
    obra = db.query(ObraDeArte).filter(ObraDeArte.id == datos.obra_id).first()

    if not obra:
        raise HTTPException(status_code=404, detail="La obra no existe")

    if obra.artista_id != artista_id:
        raise HTTPException(status_code=403, detail="No puedes subastar obras que no son tuyas")

    if obra.en_subasta:
        raise HTTPException(status_code=400, detail="Esta obra ya está en subasta")

    if datos.fecha_fin <= datos.fecha_inicio:
        raise HTTPException(status_code=400, detail="La fecha de fin debe ser posterior a la de inicio")

    # crear subasta
    subasta = Subasta(
        obra_id=obra.id,
        precio_inicio=datos.precio_inicio,
        precio_actual=datos.precio_inicio,
        fecha_inicio=datos.fecha_inicio,
        fecha_fin=datos.fecha_fin,
        estado="activa"
    )

    # actualizar obra
    obra.en_subasta = True
    db.add(subasta)
    db.commit()
    db.refresh(subasta)
    return subasta

def obtener_subastas_activas(db: Session):
    subastas = db.query(Subasta)\
        .options(
            joinedload(Subasta.obra).joinedload(ObraDeArte.artista)
        )\
        .filter(Subasta.estado == "activa")\
        .order_by(Subasta.fecha_inicio.desc())\
        .all()
    return subastas

def hacer_oferta(db: Session, usuario_id: int, datos: OfertaCrear):
    subasta = db.query(Subasta).filter(Subasta.id == datos.subasta_id).first()

    if not subasta:
        raise HTTPException(status_code=404, detail="La subasta no existe")

    if subasta.estado != "activa":
        raise HTTPException(status_code=400, detail="La subasta no está activa")

    ahora = datetime.utcnow()
    if subasta.fecha_fin < ahora or subasta.fecha_inicio > ahora:
        raise HTTPException(status_code=400, detail="La subasta no está vigente en este momento")

    if datos.cantidad <= subasta.precio_actual:
        raise HTTPException(status_code=400, detail="La oferta debe ser mayor al precio actual")

    # crear oferta
    nueva_oferta = Oferta(
        subasta_id=subasta.id,
        usuario_id=usuario_id,
        cantidad=datos.cantidad
    )

    # actualizar subasta
    subasta.precio_actual = datos.cantidad

    db.add(nueva_oferta)
    db.commit()
    db.refresh(nueva_oferta)
    return nueva_oferta

def obtener_detalle_subasta(db: Session, subasta_id: int):
    subasta = db.query(Subasta).join(Subasta.obra).join(ObraDeArte.artista).filter(Subasta.id == subasta_id).first()

    if not subasta:
        raise HTTPException(status_code=404, detail="Subasta no encontrada")

    # cargar ofertas
    ofertas = db.query(Oferta).filter(Oferta.subasta_id == subasta_id).order_by(Oferta.fecha.desc()).all()

    return {
        "id": subasta.id,
        "precio_inicio": subasta.precio_inicio,
        "precio_actual": subasta.precio_actual,
        "fecha_inicio": subasta.fecha_inicio,
        "fecha_fin": subasta.fecha_fin,
        "estado": subasta.estado,

        "titulo": subasta.obra.titulo,
        "descripcion": subasta.obra.descripcion,
        "imagen_url": subasta.obra.imagen_url,
        "artista_nombre": subasta.obra.artista.nombre,

        "ofertas": ofertas
    }

def obtener_ofertas_usuario(db: Session, usuario_id: int):
    return db.query(Oferta)\
        .join(Oferta.subasta)\
        .join(Subasta.obra)\
        .join(ObraDeArte.artista)\
        .filter(Oferta.usuario_id == usuario_id)\
        .order_by(Oferta.fecha.desc())\
        .all()