from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base

class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    senha = Column(String, nullable=False)
    perfil = Column(String, default="participante") # admin, organizador, participante

    eventos_criados = relationship("Evento", back_populates="organizador")
    inscricoes = relationship("Inscricao", back_populates="usuario")

class Evento(Base):
    __tablename__ = "eventos"

    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String, nullable=False)
    descricao = Column(String)
    data_evento = Column(DateTime, nullable=False)
    capacidade = Column(Integer, nullable=False)
    status = Column(String, default="ativo") # ativo, cancelado
    organizador_id = Column(Integer, ForeignKey("usuarios.id"))

    organizador = relationship("Usuario", back_populates="eventos_criados")
    inscricoes = relationship("Inscricao", back_populates="evento")

class Inscricao(Base):
    __tablename__ = "inscricoes"

    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"))
    evento_id = Column(Integer, ForeignKey("eventos.id"))
    status = Column(String, default="ativa") # ativa, cancelada
    data_inscricao = Column(DateTime, default=datetime.utcnow)

    usuario = relationship("Usuario", back_populates="inscricoes")
    evento = relationship("Evento", back_populates="inscricoes")
    certificado = relationship("Certificado", back_populates="inscricao", uselist=False)

class Certificado(Base):
    __tablename__ = "certificados"

    id = Column(Integer, primary_key=True, index=True)
    inscricao_id = Column(Integer, ForeignKey("inscricoes.id"), unique=True)
    codigo_validacao = Column(String, unique=True, index=True)
    data_emissao = Column(DateTime, default=datetime.utcnow)

    inscricao = relationship("Inscricao", back_populates="certificado")