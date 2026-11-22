from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.dependencies import usuario_atual
from app.models.models import Evento, Usuario
from app.schemas.schemas import EventoCreate, EventoUpdate, EventoResponse

router = APIRouter()

def validar_data(data):
    valor = data if data.tzinfo else data.replace(tzinfo=timezone.utc)
    if valor <= datetime.now(timezone.utc):
        raise HTTPException(400, "A data do evento deve ser no futuro.")

@router.post("/", response_model=EventoResponse, status_code=201)
def criar_evento(dados: EventoCreate, db: Session = Depends(get_db), atual: Usuario = Depends(usuario_atual)):
    if atual.perfil not in ("admin", "organizador"): raise HTTPException(403, "Apenas organizadores podem criar eventos.")
    validar_data(dados.data_evento)
    evento = Evento(**dados.model_dump(), organizador_id=atual.id)
    db.add(evento); db.commit(); db.refresh(evento)
    return evento

@router.get("/", response_model=list[EventoResponse])
def listar_eventos(db: Session = Depends(get_db)):
    return db.query(Evento).order_by(Evento.data_evento).all()

@router.get("/{evento_id}", response_model=EventoResponse)
def buscar_evento(evento_id: int, db: Session = Depends(get_db)):
    evento = db.query(Evento).filter(Evento.id == evento_id).first()
    if not evento: raise HTTPException(404, "Evento não encontrado.")
    return evento

@router.put("/{evento_id}", response_model=EventoResponse)
def atualizar_evento(evento_id: int, dados: EventoUpdate, db: Session = Depends(get_db), atual: Usuario = Depends(usuario_atual)):
    evento = db.query(Evento).filter(Evento.id == evento_id).first()
    if not evento: raise HTTPException(404, "Evento não encontrado.")
    if atual.perfil != "admin" and (atual.perfil != "organizador" or evento.organizador_id != atual.id):
        raise HTTPException(403, "Sem permissão para alterar este evento.")
    alteracoes = dados.model_dump(exclude_unset=True)
    if "data_evento" in alteracoes: validar_data(alteracoes["data_evento"])
    for k,v in alteracoes.items(): setattr(evento,k,v)
    db.commit(); db.refresh(evento)
    return evento

@router.delete("/{evento_id}", status_code=204)
def excluir_evento(evento_id: int, db: Session = Depends(get_db), atual: Usuario = Depends(usuario_atual)):
    evento = db.query(Evento).filter(Evento.id == evento_id).first()
    if not evento: raise HTTPException(404, "Evento não encontrado.")
    if atual.perfil != "admin" and (atual.perfil != "organizador" or evento.organizador_id != atual.id):
        raise HTTPException(403, "Sem permissão para excluir este evento.")
    db.delete(evento); db.commit()
