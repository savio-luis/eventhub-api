from pydantic import BaseModel, EmailStr, ConfigDict, Field
from datetime import datetime
from typing import Optional, Literal

Perfil = Literal["admin", "organizador", "participante"]

class UsuarioCreate(BaseModel):
    nome: str = Field(min_length=2, max_length=120)
    email: EmailStr
    senha: str = Field(min_length=8)
    perfil: Literal["participante"] = "participante"

class UsuarioUpdate(BaseModel):
    nome: Optional[str] = Field(default=None, min_length=2, max_length=120)
    email: Optional[EmailStr] = None
    senha: Optional[str] = Field(default=None, min_length=8)
    perfil: Optional[Perfil] = None

class UsuarioResponse(BaseModel):
    id: int
    nome: str
    email: EmailStr
    perfil: str
    model_config = ConfigDict(from_attributes=True)

class LoginRequest(BaseModel):
    email: EmailStr
    senha: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    usuario_id: int
    perfil: str

class EventoBase(BaseModel):
    titulo: str = Field(min_length=3, max_length=180)
    descricao: Optional[str] = None
    data_evento: datetime
    capacidade: int = Field(gt=0)

class EventoCreate(EventoBase):
    pass

class EventoUpdate(BaseModel):
    titulo: Optional[str] = Field(default=None, min_length=3, max_length=180)
    descricao: Optional[str] = None
    data_evento: Optional[datetime] = None
    capacidade: Optional[int] = Field(default=None, gt=0)
    status: Optional[Literal["ativo", "cancelado"]] = None

class EventoResponse(EventoBase):
    id: int
    status: str
    organizador_id: int
    model_config = ConfigDict(from_attributes=True)

class InscricaoCreate(BaseModel):
    evento_id: int

class InscricaoUpdate(BaseModel):
    status: Literal["ativa", "cancelada"]

class InscricaoResponse(BaseModel):
    id: int
    usuario_id: int
    evento_id: int
    status: str
    data_inscricao: datetime
    model_config = ConfigDict(from_attributes=True)

class CertificadoResponse(BaseModel):
    id: int
    inscricao_id: int
    codigo_validacao: str
    data_emissao: datetime
    model_config = ConfigDict(from_attributes=True)
