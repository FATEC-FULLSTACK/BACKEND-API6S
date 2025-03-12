from langchain_community.vectorstores import SupabaseVectorStore
from app.services.embeddings import get_embeddings
from app.utils.supabase_client import get_supabase_client

def get_vector_store():
    embeddings = get_embeddings()
    supabase_client = get_supabase_client()
    vector_store = SupabaseVectorStore(
        embedding=embeddings,
        client=supabase_client,
        table_name="documents",
        query_name="match_documents",
    )
    return vector_store
