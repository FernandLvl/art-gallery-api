# app/main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.services.auth_routes import router as api_router
from app.services import obras_routes
from app.services import subastas_routes
from app.services import ofertas_routes
from fastapi.staticfiles import StaticFiles

app = FastAPI()
print("🌟 Servidor backend inicializado correctamente")
app.include_router(obras_routes.router)
app.include_router(subastas_routes.router)
app.include_router(ofertas_routes.router)
app.mount("/static", StaticFiles(directory="static"), name="static")

# habilitar CORS por si usas frontend local o desde archivo
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # luego puedes limitar si quieres
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# incluir rutas
app.include_router(api_router)
