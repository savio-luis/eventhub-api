# EventHub API

API REST para gerenciamento de eventos acadêmicos, inscrições e certificados.

## Tecnologias
- Python 3.10+
- FastAPI e Swagger/OpenAPI
- SQLAlchemy
- SQLite para desenvolvimento; PostgreSQL recomendado em produção
- JWT (HS256) e hash de senha PBKDF2-SHA256
- Pytest e HTTPX

## Executar localmente
```bash
python -m venv .venv
# Windows: .venv\\Scripts\\activate
# Linux/macOS: source .venv/bin/activate
pip install -r requirements.txt
copy .env.example .env  # Windows; no Linux use cp
uvicorn app.main:app --reload
```
A API ficará em `http://127.0.0.1:8000`; Swagger em `/docs`, OpenAPI em `/openapi.json` e saúde em `/health`.

## Configuração
Defina `DATABASE_URL`, `SECRET_KEY` e `ACCESS_TOKEN_EXPIRE_MINUTES` no ambiente. Nunca publique o `.env` nem use a chave de exemplo em produção. Em produção configure PostgreSQL gerenciado com armazenamento persistente e HTTPS.

## Autenticação
1. Cadastre-se em `POST /api/v1/usuarios/` (cadastros públicos recebem perfil participante).
2. Faça login em `POST /api/v1/usuarios/login`.
3. Envie `Authorization: Bearer <access_token>` nas rotas protegidas.
4. O token expira conforme `ACCESS_TOKEN_EXPIRE_MINUTES` (padrão: 60).

Para criar o primeiro administrador, promova manualmente um usuário confiável no banco de dados, ou implemente um processo de bootstrap protegido antes da implantação. Não há cadastro público de administrador.

## Matriz de permissões

| Recurso/ação | Público | Participante | Organizador | Admin |
|---|---:|---:|---:|---:|
| Cadastrar-se / login | Sim | Sim | Sim | Sim |
| Consultar eventos | Sim | Sim | Sim | Sim |
| Criar evento | Não | Não | Sim | Sim |
| Alterar/excluir evento próprio | Não | Não | Sim | Sim |
| Alterar/excluir qualquer evento | Não | Não | Não | Sim |
| Inscrever-se | Não | Sim | Sim | Sim |
| Consultar inscrições | Não | Próprias | Dos seus eventos | Todas |
| Cancelar inscrição | Não | Própria | Não | Todas |
| Listar usuários | Não | Não | Não | Sim |
| Gerenciar usuário | Não | Próprio perfil | Próprio perfil | Todos |
| Emitir certificado | Não | Própria inscrição | Própria inscrição | Todas |
| Validar certificado por código | Sim | Sim | Sim | Sim |

## Regras de negócio
- Não permite e-mails duplicados.
- Senhas possuem no mínimo 8 caracteres e são armazenadas com hash.
- Eventos precisam ter data futura e capacidade positiva.
- Somente organizador/admin cria evento; organizador só gerencia os próprios.
- Evento cancelado não recebe inscrições.
- Uma pessoa não pode manter inscrição ativa duplicada no mesmo evento.
- Capacidade máxima é respeitada.
- Certificado é emitido somente para inscrição ativa e não duplica para a mesma inscrição.
- Código de validação é único.

## Testes
```bash
pytest -v
```
A suíte contém testes automatizados para autenticação, autorização, validações, eventos, inscrições, certificados e documentação.

## Endpoints principais
- `/api/v1/usuarios`: cadastro, login e gestão de usuários
- `/api/v1/eventos`: CRUD de eventos
- `/api/v1/inscricoes`: criação, consulta, atualização/cancelamento
- `/api/v1/certificados`: emissão, listagem e validação
- `/docs`: Swagger
- `/openapi.json`: especificação OpenAPI

## Deploy
Há um `render.yaml` como ponto de partida para Render. Configure `DATABASE_URL` com PostgreSQL gerenciado, `SECRET_KEY` forte e HTTPS. Configure também armazenamento persistente para banco caso escolha SQLite (não recomendado em deploy efêmero). Após publicar, valide `/health`, `/docs`, login, CRUD e persistência após reinicialização.

## Histórico de evolução
- Versão 1.0: estrutura inicial, entidades e primeiros endpoints.
- Versão 2.0: JWT real, controle de acesso por perfil, CRUDs ampliados, validações, documentação e testes automatizados.

## Identificação da entrega
Projeto acadêmico EventHub — versão 2.0.0. Atualize os integrantes, instituição, links do repositório e URL de produção antes da entrega.
