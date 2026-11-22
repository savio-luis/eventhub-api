# Matriz de permissões EventHub

| Ação | Público | Participante | Organizador | Administrador |
|---|---|---|---|---|
| Cadastro e login | Sim | Sim | Sim | Sim |
| Consultar eventos | Sim | Sim | Sim | Sim |
| Criar evento | Não | Não | Sim | Sim |
| Editar/excluir evento próprio | Não | Não | Sim | Sim |
| Editar/excluir evento de terceiros | Não | Não | Não | Sim |
| Inscrever-se em evento | Não | Sim | Sim | Sim |
| Consultar inscrições | Não | Próprias | Dos eventos próprios | Todas |
| Cancelar inscrição | Não | Própria | Não | Todas |
| Listar usuários | Não | Não | Não | Sim |
| Consultar/editar perfil | Não | Próprio | Próprio | Todos |
| Excluir usuário | Não | Não | Não | Sim |
| Emitir certificado | Não | Da própria inscrição | Da própria inscrição | Todas |
| Validar certificado | Sim | Sim | Sim | Sim |

A autorização é aplicada nas dependências e nas rotas, não apenas na interface. Cadastros públicos sempre criam participantes.
