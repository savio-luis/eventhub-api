import uuid
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.dependencies import usuario_atual
from app.models.models import Certificado, Inscricao, Usuario
from app.schemas.schemas import CertificadoResponse

router = APIRouter()

@router.post("/", response_model=CertificadoResponse, status_code=201)
def emitir_certificado(inscricao_id: int, db: Session = Depends(get_db), atual: Usuario = Depends(usuario_atual)):
    inscricao = db.query(Inscricao).filter(Inscricao.id == inscricao_id).first()
    if not inscricao: raise HTTPException(404, "Inscrição não encontrada.")
    if atual.perfil != "admin" and inscricao.usuario_id != atual.id:
        raise HTTPException(403, "Sem permissão para emitir este certificado.")
    if inscricao.status != "ativa": raise HTTPException(400, "Apenas inscrições ativas podem gerar certificados.")
    certificado = db.query(Certificado).filter_by(inscricao_id=inscricao_id).first()
    if certificado: return certificado
    certificado = Certificado(inscricao_id=inscricao_id, codigo_validacao=f"EVT-{uuid.uuid4().hex[:12].upper()}")
    db.add(certificado); db.commit(); db.refresh(certificado)
    return certificado

@router.get("/", response_model=list[CertificadoResponse])
def listar_certificados(db: Session = Depends(get_db), atual: Usuario = Depends(usuario_atual)):
    q = db.query(Certificado).join(Inscricao)
    if atual.perfil == "participante": q = q.filter(Inscricao.usuario_id == atual.id)
    elif atual.perfil == "organizador": q = q.join(Inscricao.evento).filter_by(organizador_id=atual.id)
    return q.all()

@router.get("/{codigo}/validar", response_model=CertificadoResponse)
def validar_certificado(codigo: str, db: Session = Depends(get_db)):
    certificado = db.query(Certificado).filter_by(codigo_validacao=codigo).first()
    if not certificado: raise HTTPException(404, "Certificado inválido ou inexistente.")
    return certificado
