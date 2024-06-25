from supabase import create_client, Client
from app.core.config import settings


def supabase_connect():
    url: str = settings.SUPABASE_URL
    key: str = settings.SECRET_KEY
    supabase: Client = create_client(url, key)

    return supabase
