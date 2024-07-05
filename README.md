# Apis API

Bem-vindo a API da Apis, uma ferramenta de produtividade pessoal projetada para ajudar você a manter o foco em suas tarefas e projetos. Apis oferece um painel simples e intuitivo com recursos de colaboração, relatórios de produtividade e notificações em tempo real.

### Principais Funcionalidades

Em desenvolvimento...

## Requisitos

As principais dependências utilizadas no projeto são:

- [FastAPI](https://fastapi.tiangolo.com/)
- [Uvicorn](https://www.uvicorn.org/)
- [Gunicorn](https://gunicorn.org/)
- [SQLAlchemy](https://www.sqlalchemy.org/)
- [Alembic](https://alembic.sqlalchemy.org/en/latest/)
- [Supabase](https://supabase.io/)
- [Strawberry GraphQL](https://strawberry.rocks/)

Para uma lista completa das dependências, consulte o arquivo `pyproject.toml`.

## Instalação e Configuração

1. Clone o repositório:

   ```sh
   git clone https://github.com/afiovinicius/apis-api.git
   cd apis-api
   ```

2. Instale as dependências:

   ```sh
   poetry install
   ```

3. Crie um arquivo `.env` na raiz do projeto com as seguintes variáveis:

   ```env
   DATABASE_URL=""
   DATABASE_HOST=""
   DATABASE_USER=""
   DATABASE_PASS=""
   DATABASE_LINK=""
   DATABASE_KEY=""

   ALGORITHM="HS256"
   ACCESS_TOKEN_EXPIRE_MINUTES=30

   EMAIL_USER="" # seu email do gmail
   EMAIL_PASS="" # crie uma senha para apps no gerenciador do gmail

   GOOGLE_CLIENT_ID=""
   GOOGLE_CLIENT_SECRET_KEY=""
   GOOGLE_REDIRECT_URI=""

   REDIS_URL=""
   ```

   OBS: Use o arquivo .env-example encontrado na raiz do projeto como base.

## Uso

### Desenvolvimento

Para iniciar o servidor em modo de desenvolvimento, utilize o seguinte comando:

```sh
poetry run task dev
```

### Produção

Para iniciar o servidor em modo de produção, utilize o seguinte comando:

```sh
poetry run task start
```

### Contribuição

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues e pull requests no repositório.
