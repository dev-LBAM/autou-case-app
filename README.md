# Processador de Emails

## Descrição

Aplicação que classifica emails como **Produtivo** ou **Improdutivo** e sugere respostas automáticas.  

Funciona com emails enviados por **texto** ou **arquivo (.txt / .pdf)**.  

## Tecnologias

- **Backend**: Python 3 + FastAPI  
- **Frontend**: React, TypeScript, Tailwind CSS  

## Pré-requisitos

- Python >= 3.10  
- Node.js >= 18
- pip
- npm ou yarn  
- Git  

## Execução

Clone o repositório:
```bash
git clone https://github.com/dev-LBAM/autou-email-processor.git
cd autou-email-processor
```
#### BACKEND

O backend requer uma **chave da OpenAI** para funcionar. Crie um arquivo `.env` na pasta do backend:
```env
OPENAI_API_KEY=your_openai_api_key_here
FRONTEND_ORIGIN=http://localhost:5173
```
Obtenha sua chave aqui: [OpenAI](https://platform.openai.com/), e o FRONTEND_ORIGIN copie o mesmo que está ali, pois ao iniciar o nosso frontend ele vai permitir o consumo do nosso backend.

Com o terminal no diretorio raiz do projeto **../autou-email-processor/** digite:
```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```

- Endpoints principais:

    - POST /process_email → processa email em texto

    - POST /process_email/file → processa email via arquivo .txt ou .pdf

- Documentação interativa (Swagger UI) disponível em:
```arduino
http://127.0.0.1:8000/docs
```

- Exemplo de requisição:
```bash
curl -X POST http://127.0.0.1:8000/process_email \
-H "Content-Type: application/json" \
-d '{"content": "Exemplo de email"}'
```

---

#### FRONTEND

O frontend requer a URL do backend para usar suas funcionalidades. Crie um arquivo `.env` na pasta do frontend:
```env
VITE_BACKEND_URL=http://127.0.0.1:8000
```
Com o terminal no diretorio raiz do projeto **../autou-email-processor/** digite:
```bash
cd frontend
npm install
npm run dev
```

Abra no navegador: http://localhost:5173/

## Uso

- Escolha o modo de envio: Texto ou Arquivo

- Digite o email ou selecione o arquivo

- Clique em Enviar (botão desativado durante processamento)

- Clique em Cancelar para interromper processamento se necessário

- Visualize histórico e copie respostas sugeridas

- Clique em Mostrar mais para expandir o histórico

## Observações

- Apenas arquivos .txt e .pdf são aceitos

- Cancelamento interrompe a requisição e mostra “Processamento cancelado.”

- Histórico é salvo no localStorage, mantendo os dados entre sessões

- O backend deve estar rodando localmente na porta 8000 para que o frontend funcione corretamente