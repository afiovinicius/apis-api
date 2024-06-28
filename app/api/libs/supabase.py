from supabase import Client, create_client

from app.core.config import settings


def supabase_connect():
    url: str = settings.DATABASE_LINK
    key: str = settings.DATABASE_KEY
    supabase: Client = create_client(url, key)

    return supabase
