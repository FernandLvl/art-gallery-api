# app/services/routes.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from app.data.database import SessionLocal
from app.data.models import Usuario
from app.data.schemas import UsuarioCrear, UsuarioRespuesta, Token
from app.auth import auth

router = APIRouter()

# dependencia para obtener la sesión de BD
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# registrar usuario
@router.post("/register", response_model=UsuarioRespuesta)
def registrar(usuario: UsuarioCrear, db: Session = Depends(get_db)):
    ya_existe = db.query(Usuario).filter(Usuario.email == usuario.email).first()
    if ya_existe:
        raise HTTPException(status_code=400, detail="El correo ya está registrado")
    
    usuario_db = Usuario(
        nombre=usuario.nombre,
        email=usuario.email,
        password=auth.hashear_password(usuario.password),
        rol=usuario.rol
    )
    db.add(usuario_db)
    db.commit()
    db.refresh(usuario_db)
    return usuario_db

# login
@router.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(Usuario.email == form_data.username).first()
    if not usuario or not auth.verificar_password(form_data.password, usuario.password):
        raise HTTPException(status_code=401, detail="Credenciales inválidas")
    
    token = auth.crear_token_acceso({"sub": usuario.email})
    return {"access_token": token, "token_type": "bearer"}

# obtener usuario actual
@router.get("/me", response_model=UsuarioRespuesta)
def leer_usuario_actual(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    payload = auth.decodificar_token(token)
    if payload is None:
        raise HTTPException(status_code=401, detail="Token inválido o expirado")
    
    email = payload.get("sub")
    usuario = db.query(Usuario).filter(Usuario.email == email).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    return usuario
