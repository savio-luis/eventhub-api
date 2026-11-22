# Relatório resumido de evolução — EventHub

## Situação da versão anterior (1ª/2ª Unidade)
A estrutura entregue continha os modelos de Usuário, Evento, Inscrição e Certificado, seus relacionamentos SQLAlchemy, hash de senha, endpoints iniciais e regras para impedir inscrições duplicadas, controlar capacidade e emitir certificado único. A API já utilizava FastAPI e gerava documentação OpenAPI.

## Melhorias consolidadas nesta versão 2.0
- Substituição do token fictício por JWT assinado (HS256), com expiração configurável.
- Validação de credenciais e hash de senha PBKDF2-SHA256.
- Cadastro público restrito ao perfil participante; elevação de privilégio não é permitida no cadastro.
- Controle de acesso por perfil e propriedade do recurso.
- CRUD de eventos e usuários; consulta/atualização/cancelamento de inscrições; emissão e validação de certificados.
- Validação de datas, capacidade, e-mail duplicado, inscrição duplicada e evento cancelado.
- Configuração por variáveis de ambiente e suporte a PostgreSQL via DATABASE_URL.
- Documentação Swagger/OpenAPI, README técnico e matriz de permissões.
- Inclusão de suíte com mais de 20 testes automatizados.

## Pontos que dependem da equipe antes da entrega
1. Executar `pip install -r requirements.txt` e `pytest -v` em ambiente com internet/dependências.
2. Corrigir qualquer falha identificada na execução real.
3. Configurar PostgreSQL persistente e segredo JWT forte no provedor de hospedagem.
4. Publicar e preencher os links reais de GitHub, API e Swagger.
5. Registrar evidências (prints da execução de testes, login, autorização, CRUD e banco persistido).
6. Identificar integrantes, instituição e decisões técnicas da equipe com informações verdadeiras.

## Limitação desta revisão
Este relatório descreve alterações de código realizadas nesta atualização. A implantação em produção, publicação no GitHub e demonstração online precisam ser feitas com acesso às contas da equipe e não são consideradas concluídas por este pacote.
