from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.models import Usuario
from app.schemas.schemas import UsuarioCreate, UsuarioUpdate, UsuarioResponse, LoginRequest, TokenResponse
from app.core.security import gerar_hash_senha, verificar_senha, criar_token_acesso
from app.core.dependencies import usuario_atual, exigir_perfis

router = APIRouter()

@router.post("/", response_model=UsuarioResponse, status_code=201)
def cadastrar_usuario(dados: UsuarioCreate, db: Session = Depends(get_db)):
    if db.query(Usuario).filter(Usuario.email == dados.email).first():
        raise HTTPException(409, "E-mail já cadastrado.")
    usuario = Usuario(nome=dados.nome, email=dados.email, senha=gerar_hash_senha(dados.senha), perfil="participante")
    db.add(usuario); db.commit(); db.refresh(usuario)
    return usuario

@router.post("/login", response_model=TokenResponse)
def login(dados: LoginRequest, db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(Usuario.email == dados.email).first()
    if not usuario or not verificar_senha(dados.senha, usuario.senha):
        raise HTTPException(401, "E-mail ou senha incorretos.")
    token = criar_token_acesso({"sub": str(usuario.id), "perfil": usuario.perfil})
    return {"access_token": token, "usuario_id": usuario.id, "perfil": usuario.perfil}

@router.get("/me", response_model=UsuarioResponse)
def meu_perfil(usuario: Usuario = Depends(usuario_atual)):
    return usuario

@router.get("/", response_model=list[UsuarioResponse])
def listar_usuarios(db: Session = Depends(get_db), _: Usuario = Depends(exigir_perfis("admin"))):
    return db.query(Usuario).order_by(Usuario.id).all()

@router.get("/{usuario_id}", response_model=UsuarioResponse)
def buscar_usuario(usuario_id: int, db: Session = Depends(get_db), atual: Usuario = Depends(usuario_atual)):
    if atual.perfil != "admin" and atual.id != usuario_id:
        raise HTTPException(403, "Sem permissão.")
    usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    if not usuario: raise HTTPException(404, "Usuário não encontrado.")
    return usuario

@router.put("/{usuario_id}", response_model=UsuarioResponse)
def atualizar_usuario(usuario_id: int, dados: UsuarioUpdate, db: Session = Depends(get_db), atual: Usuario = Depends(usuario_atual)):
    if atual.perfil != "admin" and atual.id != usuario_id:
        raise HTTPException(403, "Sem permissão.")
    usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    if not usuario: raise HTTPException(404, "Usuário não encontrado.")
    alteracoes = dados.model_dump(exclude_unset=True)
    if atual.perfil != "admin": alteracoes.pop("perfil", None)
    if "senha" in alteracoes: alteracoes["senha"] = gerar_hash_senha(alteracoes["senha"])
    if "email" in alteracoes and db.query(Usuario).filter(Usuario.email == alteracoes["email"], Usuario.id != usuario_id).first():
        raise HTTPException(409, "E-mail já utilizado.")
    for campo, valor in alteracoes.items(): setattr(usuario, campo, valor)
    db.commit(); db.refresh(usuario)
    return usuario

@router.delete("/{usuario_id}", status_code=204)
def excluir_usuario(usuario_id: int, db: Session = Depends(get_db), _: Usuario = Depends(exigir_perfis("admin"))):
    usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    if not usuario: raise HTTPException(404, "Usuário não encontrado.")
    db.delete(usuario); db.commit()
