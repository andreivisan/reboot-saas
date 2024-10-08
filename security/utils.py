import os
import jwt
from dotenv import load_dotenv
from jwt import PyJWTError, ExpiredSignatureError
from fastapi import Depends, Request, Response, HTTPException, status
from security.oauth2_supabase import OAuth2CookieBearer
from supabase import create_client
from . import logger

oauth2_scheme = OAuth2CookieBearer(tokenUrl="/login")
load_dotenv()

supabase_url = os.getenv("SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_KEY")
supabase = create_client(supabase_url, supabase_key)

JWT_SECRET = os.getenv("SUPABASE_JWT_SECRET")
JWT_ALGORITHM = "HS256"
AUDIENCE = "authenticated"

def _handle_authentication_failure():
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Not authenticated",
    )

async def _refresh_access_token(request:Request):
    refresh_token = request.cookies.get('refresh_token')
    if not refresh_token:
       _handle_authentication_failure() 
    try:
        response = supabase.auth.refresh_session(refresh_token)
        new_access_token = response.session.access_token
        new_refresh_token = response.session.refresh_token
        return new_access_token, new_refresh_token
    except Exception as e:
        logger.error(f"Error refreshing token: {e}")
        _handle_authentication_failure() 

async def get_current_user(
        request: Request,
        response: Response,
        token: str = Depends(oauth2_scheme)):
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM], audience=AUDIENCE)
        user_id: str = payload.get('sub')
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token payload",
            )
        return user_id
    except ExpiredSignatureError:
        # deal with token refresh
        new_access_token, new_refresh_token = await _refresh_access_token(request)
        new_payload = jwt.decode(new_access_token, JWT_SECRET, algorithms=[JWT_ALGORITHM], audience=AUDIENCE)
        user_id = new_payload.get('sub')
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token payload",
            )
        request.state.new_tokens = (new_access_token, new_refresh_token)
        return user_id
    except PyJWTError as e:
        logger.error(e)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid access token",
        )
