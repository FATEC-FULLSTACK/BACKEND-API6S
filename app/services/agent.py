from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.tools import tool
from app.services.vector_store import get_vector_store

# Inicializa o modelo de linguagem (LLM)
llm = ChatOpenAI(model="gpt-4o", temperature=0) 

# Obtem a instância do vector store
vector_store = get_vector_store()

# Define a ferramenta de recuperação de documentos
@tool(response_format="content_and_artifact")
def retrieve(query: str):
    """
    Recupera informações relacionadas a uma query utilizando a similaridade semântica.
    """
    retrieved_docs = vector_store.similarity_search(query, k=2)
    serialized = "\n\n".join(
        (f"Source: {doc.metadata}\nContent: {doc.page_content}") for doc in retrieved_docs
    )
    return serialized, retrieved_docs

tools = [retrieve]

# Cria um template de prompt (substitua "Agent prompt template" pelo template desejado)
prompt_template = PromptTemplate.from_template("""
{input}
{agent_scratchpad}
""")

# Cria o agente utilizando o mecanismo de chamadas de ferramenta
agent = create_tool_calling_agent(llm, tools, prompt_template)

# Cria o executor do agente
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

def get_agent_executor():
    return agent_executor
