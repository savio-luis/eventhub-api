from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.dependencies import usuario_atual
from app.models.models import Inscricao, Evento, Usuario
from app.schemas.schemas import InscricaoCreate, InscricaoUpdate, InscricaoResponse

router = APIRouter()

@router.post("/", response_model=InscricaoResponse, status_code=201)
def realizar_inscricao(dados: InscricaoCreate, db: Session = Depends(get_db), atual: Usuario = Depends(usuario_atual)):
    evento = db.query(Evento).filter(Evento.id == dados.evento_id).first()
    if not evento: raise HTTPException(404, "Evento não encontrado.")
    if evento.status != "ativo": raise HTTPException(400, "Evento cancelado não aceita inscrições.")
    existente = db.query(Inscricao).filter_by(usuario_id=atual.id, evento_id=evento.id, status="ativa").first()
    if existente: raise HTTPException(409, "Participante já inscrito neste evento.")
    total = db.query(Inscricao).filter_by(evento_id=evento.id, status="ativa").count()
    if total >= evento.capacidade: raise HTTPException(400, "O evento atingiu a capacidade máxima.")
    inscricao = Inscricao(usuario_id=atual.id, evento_id=evento.id, status="ativa")
    db.add(inscricao); db.commit(); db.refresh(inscricao)
    return inscricao

@router.get("/", response_model=list[InscricaoResponse])
def listar_inscricoes(db: Session = Depends(get_db), atual: Usuario = Depends(usuario_atual)):
    q = db.query(Inscricao)
    if atual.perfil == "participante": q = q.filter(Inscricao.usuario_id == atual.id)
    elif atual.perfil == "organizador":
        q = q.join(Evento).filter(Evento.organizador_id == atual.id)
    return q.order_by(Inscricao.id).all()

@router.get("/{inscricao_id}", response_model=InscricaoResponse)
def buscar_inscricao(inscricao_id: int, db: Session = Depends(get_db), atual: Usuario = Depends(usuario_atual)):
    item = db.query(Inscricao).filter(Inscricao.id == inscricao_id).first()
    if not item: raise HTTPException(404, "Inscrição não encontrada.")
    if atual.perfil == "participante" and item.usuario_id != atual.id: raise HTTPException(403, "Sem permissão.")
    if atual.perfil == "organizador" and item.evento.organizador_id != atual.id: raise HTTPException(403, "Sem permissão.")
    return item

@router.patch("/{inscricao_id}", response_model=InscricaoResponse)
def atualizar_inscricao(inscricao_id: int, dados: InscricaoUpdate, db: Session = Depends(get_db), atual: Usuario = Depends(usuario_atual)):
    item = db.query(Inscricao).filter(Inscricao.id == inscricao_id).first()
    if not item: raise HTTPException(404, "Inscrição não encontrada.")
    if atual.perfil != "admin" and item.usuario_id != atual.id: raise HTTPException(403, "Somente o participante ou administrador pode alterar.")
    if dados.status == "ativa":
        if item.evento.status != "ativo": raise HTTPException(400, "Evento cancelado.")
        ativos = db.query(Inscricao).filter(Inscricao.evento_id == item.evento_id, Inscricao.status == "ativa", Inscricao.id != item.id).count()
        if ativos >= item.evento.capacidade: raise HTTPException(400, "Evento sem vagas.")
    item.status = dados.status
    db.commit(); db.refresh(item)
    return item

@router.delete("/{inscricao_id}", status_code=204)
def cancelar_inscricao(inscricao_id: int, db: Session = Depends(get_db), atual: Usuario = Depends(usuario_atual)):
    item = db.query(Inscricao).filter(Inscricao.id == inscricao_id).first()
    if not item: raise HTTPException(404, "Inscrição não encontrada.")
    if atual.perfil != "admin" and item.usuario_id != atual.id: raise HTTPException(403, "Sem permissão.")
    item.status = "cancelada"; db.commit()
