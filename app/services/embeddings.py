from langchain_openai import OpenAIEmbeddings

def get_embeddings():
    # Retorna uma instância do modelo de embeddings
    return OpenAIEmbeddings(model="text-embedding-3-small")
