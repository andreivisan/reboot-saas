import os
from dotenv import load_dotenv
from fastapi.templating import Jinja2Templates
from logging_config import get_logger
from supabase import create_client
from supabase.lib.client_options import ClientOptions

templates = Jinja2Templates(directory="templates")

logger = get_logger(__name__)

load_dotenv()

supabase_url = os.getenv("SUPABASE_URL")
service_role_key = os.getenv("SERVICE_ROLE")
supabase = create_client(
    supabase_url, 
    service_role_key,
    options=ClientOptions(
        auto_refresh_token=False,
        persist_session=False,
    )
)
# Access auth admin api
admin_auth_client = supabase.auth.admin