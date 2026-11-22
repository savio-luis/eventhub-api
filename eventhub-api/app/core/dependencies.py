from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from jose import JWTError
from app.core.database import get_db
from app.core.security import decodificar_token
from app.models.models import Usuario

bearer = HTTPBearer(auto_error=False)

def usuario_atual(credentials: HTTPAuthorizationCredentials = Depends(bearer), db: Session = Depends(get_db)):
    erro = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido ou ausente", headers={"WWW-Authenticate": "Bearer"})
    if not credentials:
        raise erro
    try:
        payload = decodificar_token(credentials.credentials)
        uid = payload.get("sub")
        if uid is None:
            raise erro
    except (JWTError, ValueError):
        raise erro
    usuario = db.query(Usuario).filter(Usuario.id == int(uid)).first()
    if not usuario:
        raise erro
    return usuario

def exigir_perfis(*perfis):
    def dependencia(usuario: Usuario = Depends(usuario_atual)):
        if usuario.perfil not in perfis:
            raise HTTPException(status_code=403, detail="Você não tem permissão para esta operação.")
        return usuario
    return dependencia
