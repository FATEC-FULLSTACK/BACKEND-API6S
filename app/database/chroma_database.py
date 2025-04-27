import chromadb
from chromadb.utils import embedding_functions
from sentence_transformers import SentenceTransformer
import os
# Carregar o modelo de embedding multilíngue
model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')

# Definir a função de embedding para o ChromaDB
sentence_transformer_ef = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name="paraphrase-multilingual-MiniLM-L12-v2"
)


def get_chroma_path():
    path = os.getenv("CHROMA_PATH")
    if not path:
        print("não encontrou o arquivo .env")
        path = 'chromadb'
    return path


def get_vector_database():
    path = get_chroma_path()
    client = chromadb.PersistentClient(path=path)
    database = client.get_collection("test_collection_chunknized", embedding_function=sentence_transformer_ef)
    return database