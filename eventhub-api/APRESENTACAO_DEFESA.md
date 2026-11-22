# Roteiro de apresentação e defesa — EventHub

1. **Problema e objetivo:** apresentar a necessidade de organizar eventos acadêmicos, inscrições e certificados.
2. **Arquitetura:** explicar FastAPI, separação entre endpoints, schemas, models e core, SQLAlchemy e banco de dados.
3. **Modelo de dados:** demonstrar Usuário, Evento, Inscrição e Certificado e seus relacionamentos.
4. **Autenticação:** cadastrar participante, realizar login, copiar o JWT e testar uma rota protegida no Swagger. Explicar expiração e hash de senha.
5. **Autorização:** demonstrar diferença entre participante, organizador e administrador, incluindo tentativa negada com HTTP 403.
6. **CRUD e regras:** criar/consultar/editar/excluir evento; demonstrar data futura, capacidade, bloqueio de inscrição duplicada, evento cancelado e certificado.
7. **Testes:** executar `pytest -v`, mostrar quantidade e resultado. Não afirmar aprovação sem execução real.
8. **Deploy:** abrir URL pública HTTPS, `/health` e `/docs`; demonstrar que dados continuam após reinicialização.
9. **Evolução e dificuldades:** comparar a versão inicial com a atualizada e explicar decisões de segurança, organização e persistência.
10. **Encerramento:** apresentar repositório, versão, documentação e divisão de tarefas real do grupo.

## Perguntas que podem aparecer
- Por que JWT? Para autenticar requisições sem enviar senha em cada chamada.
- Como a senha é protegida? É armazenado hash PBKDF2, não a senha em texto puro.
- Como funciona a autorização? O token identifica o usuário e a API verifica perfil e propriedade do recurso.
- Como garantir persistência em produção? Usar banco PostgreSQL gerenciado/persistente e validar após reinicialização.
- Como evitar inscrições duplicadas? Consultar inscrições ativas antes de criar e validar capacidade.
