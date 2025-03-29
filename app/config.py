import os
from dotenv import load_dotenv

def load_environment():
    load_dotenv()

# Variáveis globais de configuração
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_SERVICE_KEY = os.environ.get("SUPABASE_SERVICE_KEY")
MONGO_URL = os.getenv("CONNECTION_MONGO")

if not SUPABASE_URL or not SUPABASE_SERVICE_KEY:
    raise ValueError("Variáveis do SUPABASE não foram inseridos.")
