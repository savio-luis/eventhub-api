from datetime import datetime, timedelta, timezone

def cadastro(client, email="user@teste.com"):
    return client.post("/api/v1/usuarios/", json={"nome":"Usuario Teste","email":email,"senha":"SenhaForte123"})

def login(client, email="user@teste.com", senha="SenhaForte123"):
    return client.post("/api/v1/usuarios/login", json={"email":email,"senha":senha})

def criar_org(client, db_session):
    from app.models.models import Usuario
    from app.core.security import gerar_hash_senha
    u=Usuario(nome="Org",email="org@teste.com",perfil="organizador",senha=gerar_hash_senha("SenhaForte123"))
    db_session.add(u); db_session.commit()
    r=login(client,"org@teste.com")
    return {"Authorization":f"Bearer {r.json()['access_token']}"}

def evento(client, headers, capacidade=2):
    return client.post("/api/v1/eventos/",headers=headers,json={
        "titulo":"Evento de Tecnologia","descricao":"Descricao","data_evento":(datetime.now(timezone.utc)+timedelta(days=10)).isoformat(),"capacidade":capacidade
    })

def test_raiz_ok(client):
    assert client.get("/").status_code == 200

def test_health_ok(client):
    assert client.get("/health").json()["status"] == "ok"

def test_cadastro_usuario(client):
    assert cadastro(client).status_code == 201

def test_email_duplicado(client):
    cadastro(client)
    assert cadastro(client).status_code == 409

def test_senha_minima(client):
    r=client.post("/api/v1/usuarios/",json={"nome":"Teste","email":"a@b.com","senha":"123"})
    assert r.status_code == 422

def test_login_sucesso(client):
    cadastro(client)
    r=login(client)
    assert r.status_code == 200 and len(r.json()["access_token"]) > 30

def test_login_senha_incorreta(client):
    cadastro(client)
    assert login(client,senha="errada").status_code == 401

def test_me_sem_token(client):
    assert client.get("/api/v1/usuarios/me").status_code == 401

def test_me_com_token(client,auth):
    assert client.get("/api/v1/usuarios/me",headers=auth).status_code == 200

def test_perfil_nao_pode_listar_usuarios(client,auth):
    assert client.get("/api/v1/usuarios/").status_code == 401
    assert client.get("/api/v1/usuarios/",headers=auth).status_code == 403

def test_usuario_nao_acessa_outro_perfil(client,auth):
    assert client.get("/api/v1/usuarios/999",headers=auth).status_code == 403

def test_evento_exige_login(client):
    assert client.post("/api/v1/eventos/",json={}).status_code == 401

def test_participante_nao_cria_evento(client,auth):
    assert evento(client,auth).status_code == 403

def test_organizador_cria_evento(client,db_session):
    headers=criar_org(client,db_session)
    assert evento(client,headers).status_code == 201

def test_lista_eventos_publica(client):
    assert client.get("/api/v1/eventos/").status_code == 200

def test_evento_nao_encontrado(client):
    assert client.get("/api/v1/eventos/999").status_code == 404

def test_data_evento_passada_rejeitada(client,db_session):
    headers=criar_org(client,db_session)
    r=client.post("/api/v1/eventos/",headers=headers,json={"titulo":"Evento passado","data_evento":"2020-01-01T10:00:00","capacidade":10})
    assert r.status_code == 400

def test_inscricao_exige_login(client):
    assert client.post("/api/v1/inscricoes/",json={"evento_id":1}).status_code == 401

def test_inscricao_evento_inexistente(client,auth):
    assert client.post("/api/v1/inscricoes/",headers=auth,json={"evento_id":999}).status_code == 404

def test_inscricao_evento_cancelado(client,auth,db_session):
    from app.models.models import Evento, Usuario
    u=db_session.query(Usuario).first()
    e=Evento(titulo="Cancelado",data_evento=datetime.now()+timedelta(days=2),capacidade=10,status="cancelado",organizador_id=u.id)
    db_session.add(e); db_session.commit()
    assert client.post("/api/v1/inscricoes/",headers=auth,json={"evento_id":e.id}).status_code == 400

def test_certificado_inexistente(client,auth):
    assert client.post("/api/v1/certificados/?inscricao_id=999",headers=auth).status_code == 404

def test_validar_certificado_inexistente(client):
    assert client.get("/api/v1/certificados/INVALIDO/validar").status_code == 404

def test_swagger_disponivel(client):
    assert client.get("/docs").status_code == 200

def test_openapi_disponivel(client):
    r=client.get("/openapi.json")
    assert r.status_code == 200 and "EventHub API" in r.text
