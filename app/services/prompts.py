from langchain.prompts import ChatPromptTemplate, HumanMessagePromptTemplate
from langchain_core.messages import SystemMessage

chat_template = ChatPromptTemplate.from_messages([
    SystemMessage(content=(
        "Você é um assistente médico especializado em neurologia e doenças neurodegenerativas.\n\n"
        "Regras:\n"
        "- Seja objetivo.\n"
        "- Cite fontes apenas se solicitado.\n"
        "- Priorize informações práticas.\n"
        "- Use o contexto fornecido.\n"
        "- Caso o tema não seja Alzheimer, responda educadamente que não pode ajudar."
    )),
    HumanMessagePromptTemplate.from_template(
        'Por favor, fale sobre a Doença de Alzheimer com base na pergunta abaixo:\n{question}\n\ncontexto: {context}'
    )
])
