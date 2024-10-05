import os
from dotenv import load_dotenv
from fastapi.templating import Jinja2Templates
from logging_config import get_logger
from supabase import create_client, Client

templates = Jinja2Templates(directory="templates")

logger = get_logger(__name__)

load_dotenv()

supabase_url = os.getenv("SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_KEY")
supabase = create_client(supabase_url, supabase_key)
