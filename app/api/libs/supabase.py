from supabase import create_client, Client
from app.core.config import settings


def supabase_connect():
    url: str = settings.DATABASE_LINK
    key: str = settings.DATABASE_KEY
    supabase: Client = create_client(url, key)

    return supabase
