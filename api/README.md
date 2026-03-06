# User Data Processing API

REST API desenvolvida para processar e armazenar dados de usuários a partir de um arquivo JSON remoto.

Este projeto foi desenvolvido como parte de um teste técnico com foco em:

* Boas práticas de programação
* Organização e estruturação de código
* Performance no processamento de dados
* Clareza na documentação

---

# Arquitetura da Aplicação

A aplicação segue uma arquitetura em camadas para garantir separação de responsabilidades e facilitar manutenção.

```
API (FastAPI)
│
├── Routes
│     Responsáveis por expor os endpoints HTTP
│
├── Services
│     Contêm a lógica de negócio
│
├── Repositories
│     Responsáveis pela comunicação com o banco de dados
│
├── Models
│     Representação das entidades no banco
│
└── Database
      Configuração de conexão e sessão
```

---

# Estrutura do Projeto

```
api
│
├── app
│   ├── core
│   │   └── config.py
│   │
│   ├── db
│   │   ├── base.py
│   │   ├── session.py
│   │   ├── init_db.py
│   │   └── models
│   │       └── user.py
│   │
│   ├── repositories
│   │   └── user_repository.py
│   │
│   ├── services
│   │   └── import_service.py
│   │
│   ├── routes
│   │   └── users.py
│   │
│   └── main.py
│
├── tests
│   ├── conftest.py
│   ├── test_import_users.py
│   ├── test_get_user.py
│   └── test_health.py
│
├── requirements.txt
└── README.md
```

---

# Tecnologias Utilizadas

* Python
* FastAPI
* SQLAlchemy
* SQLite
* Pytest
* Requests
* IJSON

---

# Pré-requisitos

Antes de executar o projeto é necessário ter instalado:

* Python 3.10+
* pip

---

# Instalação

Clone o repositório:

```
git clone https://github.com/seuusuario/user-data-processing-api.git
```

Entre na pasta do projeto:

```
cd api
```

Crie um ambiente virtual:

```
python -m venv venv
```

Ative o ambiente virtual:

Linux / Mac

```
source venv/bin/activate
```

Windows

```
venv\Scripts\activate
```

Instale as dependências:

```
pip install -r requirements.txt
```

---

# Executando a aplicação

Para iniciar o servidor:

```
uvicorn app.main:app --reload
```

A API estará disponível em:

```
http://127.0.0.1:8000
```

Documentação automática:

```
http://127.0.0.1:8000/docs
```

---

# Endpoints da API

## Importar usuários a partir de um JSON remoto

```
POST /api/v1/import/users
```

O endpoint recebe uma URL via **form-data** contendo o arquivo JSON.

Exemplo de requisição usando cURL:

```
curl -X POST http://127.0.0.1:8000/api/v1/import/users \
-F "url=https://example.com/users.json"
```

Resposta esperada:

```
{
  "status": "ok",
  "inserted": 32000,
  "skipped": 0,
  "invalid": 0
}
```

---

## Buscar usuário por ID

```
GET /api/v1/users/{id}
```

Exemplo:

```
curl http://127.0.0.1:8000/api/v1/users/5df38f6e695566a48211da8f
```

Resposta:

```
{
  "user": {
    "id": "5df38f6e695566a48211da8f",
    "first_name": "Blankenship",
    "last_name": "Vincent",
    "email": "blankenshipvincent@rocklogic.com"
  }
}
```

# Estratégia de Performance

O processamento do JSON foi implementado utilizando **streaming parsing** com `ijson`.

Isso evita carregar todo o arquivo na memória, permitindo processar arquivos grandes de forma eficiente.

O processo ocorre em batches para reduzir overhead de operações no banco.

---

# Autor

**Kevin Di Domenico Matos**
