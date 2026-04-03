# Message Board

Projeto individual para a aula de MAC0350 do IME-USP.

**Message Board** é um fórum de mensagens onde múltiplos usuários podem criar postagens.

## Stack

O projeto foi construído utilizando a seguinte stack:

- **Frontend:** HTML, CSS, JavaScript e [HTMX](https://htmx.org/)
- **Backend:** [FastAPI](https://fastapi.tiangolo.com/) (Python)
- **Banco de Dados:** 
  - **SQLite** para desenvolvimento local
  - **PostgreSQL** para ambiente de produção

Para o gerenciamento de conexões, ORM e migrações, foi utilizado o [SQLAlchemy](https://www.sqlalchemy.org/).

## Como rodar

Para rodar o projeto localmente, utilize os seguintes comandos:

```bash
uv sync
uv run start
```

ou com docker:

```bash
docker compose up -d
```
