from supabase.client import Client, create_client
from app.config import SUPABASE_URL, SUPABASE_SERVICE_KEY

def get_supabase_client() -> Client:
    return create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)
