from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.database import Base, engine
from app.api.v1.router import api_router
from app.models import models  # registra os modelos no metadata

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="EventHub API",
    description="API REST para gestão de eventos acadêmicos. Autenticação Bearer JWT e controle de acesso por perfil.",
    version="2.0.0",
    contact={"name": "Equipe EventHub"}
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(api_router, prefix="/api/v1")

@app.get("/", tags=["Sistema"])
def root():
    return {"message": "EventHub API funcionando", "version": app.version, "docs": "/docs"}

@app.get("/health", tags=["Sistema"])
def health():
    return {"status": "ok"}
