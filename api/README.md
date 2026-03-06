# User Data Processing API

REST API para importar um arquivo JSON de usuários via URL (form-data), persistir no banco e consultar usuário por ID.

## Pré-requisitos
- Python 3.11+
- Git (opcional)
- Ambiente virtual recomendado (venv)

## Passo a passo para instalação
1. Abra o diretório do projeto e entre na pasta `api`:

```powershell
cd C:\Users\Cliente\OneDrive\Documentos\Roos\api
```

2. Crie e ative um virtualenv:

```powershell
python -m venv .venv
.venv\Scripts\activate
```

3. Instale dependências:

```powershell
pip install -r requirements.txt
```
 
## Como executar a aplicação localmente
1. A partir do diretório pai (`C:\Users\Cliente\OneDrive\Documentos\Roos`) execute:

```powershell
.venv\Scripts\python.exe -m uvicorn api.app.main:app --reload --port 8000
```

2. A API ficará disponível em `http://127.0.0.1:8000`.

## Como testar os endpoints
- Health: `GET /health` — retorna `{"status":"ok"}`
- Import: `POST /api/v1/import/users` (form-data: `url=<json_url>`)
- Get user: `GET /api/v1/users/{user_id}`

## Exemplos de requisições (cURL)

- Health check
```bash
curl http://127.0.0.1:8000/health
```

- Import (exemplo com URL pública)
```bash
curl -X POST -F "url=https://exemplo.com/users.json" http://127.0.0.1:8000/api/v1/import/users
```

- Buscar usuário
```bash
curl http://127.0.0.1:8000/api/v1/users/user-123
```

## Como o projeto funciona

- **Organização da estrutura do projeto**: separação em camadas (`app/core`, `app/db`, `app/repositories`, `app/services`, `app/routes`).
- **Clareza e padronização do código**: uso de tipagem e padrões claros `black` e `ruff`.
- **Tratamento de erros**: `ImportService` e rotas usam `HTTPException` com status apropriado.
- **Validação de dados**: `_extract_user_row` valida campos essenciais; adicione Pydantic schemas para validação nas rotas.
- **Performance no processamento do arquivo**: streaming com `ijson` e otimização do `bulk_upsert` para evitar N+1.
- **Documentação da API**: FastAPI fornece `/docs` e `/openapi.json` por padrão.
- **Boas práticas**: separação de camadas, `Depends` para injeção, uso de SQLAlchemy 2.0.

## Parar servidores locais
- No Windows: identifique o PID com `netstat -ano | findstr :8000` e finalize com `taskkill /PID <pid> /F`.

## Como contribuir / enviar para avaliação

Siga estes passos para preparar e enviar seu fork para avaliação:

1. Crie um fork do repositório original no GitHub.
2. No repositório local, crie uma branch com um nome descritivo:

```powershell
cd "C:\Users\Cliente\OneDrive\Documentos\Roos"
git checkout -b feat/minha-melhora
```

3. Revise e adicione as mudanças (ex.: depois de rodar `black`/`ruff`):

```powershell
git add -A
git commit -m "feat: descrição curta da mudança"
```

4. Adicione o remote do seu fork (substitua `<seu-usuario>` e `<repo>`):

```powershell
git remote add myfork https://github.com/<seu-usuario>/<repo>.git
git push -u myfork feat/minha-melhora
```

5. No GitHub, abra um Pull Request (PR) da sua branch para o repositório original. Copie o link do PR ou do seu fork e envie para avaliação.

Observações:
- Recomendo rodar `black .` e `ruff check . --fix` antes de commitar.
- Não é necessário incluir o arquivo `.json` no repositório — sirva-o via HTTP local (ex.: `python -m http.server 9000`) e use a URL no form-data ao testar o endpoint de import.

Se quiser, eu posso criar um PR template automático (já adicionei um arquivo `.github/PULL_REQUEST_TEMPLATE.md` neste repositório) e ajudar a preencher a descrição do PR.
