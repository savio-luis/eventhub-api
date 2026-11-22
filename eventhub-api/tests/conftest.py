import os
os.environ["SECRET_KEY"] = "test-secret-key-at-least-32-characters-long"
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from fastapi.testclient import TestClient
from app.main import app
from app.core.database import Base, get_db
from app.models.models import Usuario
from app.core.security import gerar_hash_senha

@pytest.fixture()
def db_engine():
    engine = create_engine("sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool)
    Base.metadata.create_all(bind=engine)
    yield engine
    Base.metadata.drop_all(bind=engine)

@pytest.fixture()
def db_session(db_engine):
    TestingSession = sessionmaker(autocommit=False, autoflush=False, bind=db_engine)
    session = TestingSession()
    yield session
    session.close()

@pytest.fixture()
def client(db_engine):
    TestingSession = sessionmaker(autocommit=False, autoflush=False, bind=db_engine)
    def override_get_db():
        session = TestingSession()
        try:
            yield session
        finally:
            session.close()
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()

@pytest.fixture()
def criar_usuario(db_session):
    def _criar(nome, email, perfil="participante", senha="SenhaForte123"):
        u = Usuario(nome=nome, email=email, perfil=perfil, senha=gerar_hash_senha(senha))
        db_session.add(u); db_session.commit(); db_session.refresh(u)
        return u
    return _criar

@pytest.fixture()
def token(client):
    client.post("/api/v1/usuarios/", json={"nome":"Participante","email":"p@teste.com","senha":"SenhaForte123"})
    r = client.post("/api/v1/usuarios/login", json={"email":"p@teste.com","senha":"SenhaForte123"})
    return r.json()["access_token"]

@pytest.fixture()
def auth(token):
    return {"Authorization": f"Bearer {token}"}
