from fastapi import Depends, Request
from security.oauth2_supabase import OAuth2CookieBearer

oath2_scheme = OAuth2CookieBearer(tokenUrl="/login")

async def get_current_user(request: Request, token: str = Depends(oauth2_scheme)):
    pass
