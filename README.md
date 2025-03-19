# BACKEND-API6S

Um chatbot baseado em RAG (Retrieval-Augmented Generation) utilizando **FastAPI**, **LangChain**, **OpenAI GPT-4o** e **Supabase** como banco de vetores.

---

## 🚀 Tecnologias Utilizadas

- **[FastAPI](https://fastapi.tiangolo.com/)** - Framework web rápido e moderno para APIs  
- **[LangChain](https://www.langchain.com/)** - Ferramenta para criação de agentes LLM  
- **[OpenAI GPT-4o](https://platform.openai.com/)** - Modelo de linguagem para processamento de texto  
- **[Supabase](https://supabase.com/)** - Banco de dados PostgreSQL com armazenamento vetorial  
- **[Docker](https://www.docker.com/)** - (Opcional) Para deploy containerizado  (implementação futura)

---

## 📁 Estrutura do Projeto

```
fastapi_rag_chatbot/
│── app/
│   ├── __init__.py
│   ├── main.py            # Ponto de entrada da API
│   ├── config.py          # Carregamento de variáveis de ambiente
│   ├── models.py          # Modelos de dados Pydantic
│   ├── routes.py          # Definição das rotas FastAPI
│   ├── services/
│   │   ├── __init__.py
│   │   ├── chat.py        # Serviço de gerenciamento de chat
│   │   ├── embeddings.py  # Serviço de embeddings OpenAI (implementação futura)
│   │   ├── vector_store.py # Armazenamento vetorial Supabase (implementação futura)
│   ├── utils/
│   │   ├── __init__.py
│   │   └── database.py # (implementação futura)
│── .env                   # Arquivo de variáveis de ambiente (necessário criar arquivo com base .env.model)
│── .env                   # Arquivo de variáveis de ambiente
│── requirements.txt       # Dependências do projeto
│── README.md              # Documentação do projeto
```

---

## ✅ Pré-requisitos

Antes de instalar, certifique-se de ter os seguintes requisitos:

- **Python 3.9+**  
- **Pip** (Gerenciador de pacotes do Python)  
- **Git** (Para controle de versão)  
- **Conta no OpenAI com 5$ créditos** (Para API do GPT-4o)  
- **Conta no GEMINI com 5$ créditos** (Para API do gemini-1.5-pro)
- **Conta no Supabase** (Para armazenamento vetorial)  

---

## ⚙️ Instalação e Configuração

### 🔹 Clone o repositório

```bash
git clone https://github.com/FATEC-FULLSTACK/BACKEND-API6S.git
cd BACKEND-API6S
```

### 🔹 Criação do ambiente virtual

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate  # Windows
```

### 🔹 Instale as dependências

```bash
pip install -r requirements.txt
```

---

## 🌍 Configuração das Variáveis de Ambiente

Crie um arquivo `.env` na raiz do projeto e adicione as credenciais necessárias:

```ini
# Configuração da OpenAI
OPENAI_API_KEY="sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"

# Configuração do Supabase
SUPABASE_URL="https://xyzcompany.supabase.co"
SUPABASE_SERVICE_KEY="your-supabase-service-key"
```

---

## 🚀 Como Executar

### 🔹 Execução local

```bash
uvicorn app.main:app --reload
```

A API estará disponível em:

```
http://127.0.0.1:8000
```

---

## 📡 Uso da API

A API possui um endpoint `/chat` para interação com o chatbot.  

### 🔹 **Enviar mensagem para o chatbot**

**Requisição:**
```bash
POST http://127.0.0.1:8000/chat
```

**Body (JSON):**
```json
"PERGUNTAS RELACIONADAS A DOENÇA ALZHEIMER"

{
  "user_id": "123456",
  "message": "ORIGEM DO ALZHEIMER?"
}
```

**Resposta (JSON):**
```json
{
  "reply": "Olá! Estou bem, como posso te ajudar?"
}
```

---

## 📜 Licença

Este projeto é licenciado sob a **MIT License**.  

---