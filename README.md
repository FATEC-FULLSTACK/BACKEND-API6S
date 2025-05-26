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

PARA DETALHES DA DOCUMENTAÇÃO DA API
http://127.0.0.1:8000/docs
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
  "user_id": "123",
  "message": "Como as variações genéticas específicas, além dos genes APP, PSEN1 e PSEN2, influenciam o risco e a progressão do Alzheimer?"
}'
```

**Resposta (JSON):**
```json
{
  "status": "success",
  "data": {
    "user_id": "123",
    "question": "Como as variações genéticas específicas, além dos genes APP, PSEN1 e PSEN2, influenciam o risco e a progressão do Alzheimer?",
    "responses": {
      "openai": "1️⃣ **Introdução**: A Doença de Alzheimer (DA) é uma condição neurodegenerativa progressiva caracterizada por declínio cognitivo e perda de memória. Embora os genes APP, PSEN1 e PSEN2 estejam fortemente associados à forma familiar da doença, variações genéticas adicionais também desempenham um papel significativo no risco e na progressão da DA esporádica.\n\n2️⃣ **Fisiopatologia**: A DA é marcada pela deposição de placas de beta-amiloide e emaranhados neurofibrilares de proteína tau no cérebro. Além dos genes APP, PSEN1 e PSEN2, outras variações genéticas influenciam esses processos patológicos. Por exemplo, o gene APOE, especialmente o alelo ε4, é um dos fatores de risco genéticos mais significativos para a DA esporádica, influenciando a deposição de amiloide e a inflamação cerebral (Karch et al., 2014).\n\n3️⃣ **Diagnóstico**: O diagnóstico da DA envolve avaliação clínica, testes neuropsicológicos e biomarcadores, como a análise de líquido cefalorraquidiano (LCR) para beta-amiloide e tau, além de neuroimagem. Testes genéticos podem ser realizados para identificar variações em genes de risco, como APOE, embora não sejam rotineiramente usados para diagnóstico clínico.\n\n4️⃣ **Tratamento Atual**: Atualmente, os tratamentos para DA incluem inibidores da colinesterase (donepezila, rivastigmina, galantamina) e memantina, que ajudam a aliviar sintomas, mas não alteram a progressão da doença. Intervenções não medicamentosas, como estimulação cognitiva e suporte psicossocial, também são importantes.\n\n5️⃣ **Pesquisas Recentes**: Estudos recentes têm explorado o papel de outros genes, como TREM2, que está associado à resposta imune e inflamação no cérebro, e CLU, que está envolvido no metabolismo lipídico e na homeostase amiloide (Guerreiro et al., 2013). Pesquisas também estão investigando terapias genéticas e imunoterapias que visam modificar a expressão ou o impacto dessas variações genéticas.\n\n6️⃣ **Conclusão**: A compreensão das variações genéticas além de APP, PSEN1 e PSEN2 está ampliando",
      "gemini": "## Relatório sobre a Influência de Variações Genéticas no Risco e Progressão da Doença de Alzheimer\n\n1️⃣ **Introdução**: A Doença de Alzheimer (DA) é uma doença neurodegenerativa progressiva, caracterizada por declínio cognitivo, perda de memória e alterações comportamentais. Embora mutações nos genes APP, PSEN1 e PSEN2 causem formas familiares raras de DA de início precoce, a maioria dos casos são esporádicos e de início tardio, com forte influência genética.  Compreender a contribuição de outras variações genéticas além desses genes principais é crucial para o desenvolvimento de novas estratégias de prevenção e tratamento.\n\n2️⃣ **Fisiopatologia**: A DA é caracterizada pelo acúmulo de placas amiloides (Aβ) e emaranhados neurofibrilares de tau hiperfosforilada no cérebro.  Variações genéticas podem influenciar diversos processos patológicos, incluindo a produção, agregação e clearance de Aβ, a fosforilação de tau, a neuroinflamação, a função sináptica e a homeostase do cálcio.  Além dos genes APP, PSEN1 e PSEN2, que afetam diretamente o processamento da proteína precursora amiloide (APP), outros genes modulam o risco e a progressão da DA.\n\n3️⃣ **Diagnóstico**: O diagnóstico da DA é baseado na avaliação clínica, incluindo histórico médico, exame neurológico e testes neuropsicológicos. Biomarcadores como níveis de Aβ e tau no líquido cefalorraquidiano (LCR) e imagens de amiloide por PET podem auxiliar no diagnóstico, especialmente em estágios iniciais.  A identificação de variantes genéticas de risco pode contribuir para a estratificação de risco e o desenvolvimento de abordagens personalizadas de medicina de precisão.\n\n4️⃣ **Tratamento Atual**: Atualmente, os tratamentos disponíveis para DA oferecem alívio sintomático e incluem inibidores da colinesterase (donepezil, rivastigmina, galantamina) e memantina (antagonista do receptor NMDA).  Recentemente, o aducanumab, um anticorpo monoclonal direcionado contra Aβ, foi aprovado para o tratamento da DA, representando um avanço significativo. No entanto, sua eficácia clínica ainda é debatida.  Terapias não farma"
    }
  }
}
```
