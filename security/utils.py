import os
import jwt
from dotenv import load_dotenv
from jwt import PyJWTError, ExpiredSignatureError
from fastapi import Depends, Request
from fastapi.responses import RedirectResponse
from security.oauth2_supabase import OAuth2CookieBearer

oath2_scheme = OAuth2CookieBearer(tokenUrl="/login")
load_dotenv()

JWT_SECRET = os.getenv("SUPABASE_JWT_SECRET")
JWT_ALGORITHM = "HS256"

def _refresh_access_token(request:Request):
    refresh_token = request.cookies.get('refresh_token')
    if not refresh_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
        )
    response = supabase.auth.refresh_session(refresh_token)
    print(f'Supabase refresh session response: {response}')
    if 'error' in response:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
        )
    new_access_token = response.session.access_token
    new_refresh_token = response.session.response_token
    return new_access_token, new_refresh_token

def get_current_user(request: Request, token: str = Depends(oauth2_scheme)):
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        print(f'JWT Payload: {payload}')
        user_id: str = payload.get('sub')
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token payload",
            )
        return user_id
    except ExpiredSignatureError:
        # deal with token refresh
        new_access_token, new_refresh_token = _refresh_access_token(request)
        new_payload = jwt.decode(new_access_token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        user_id = new_payload.get('sub')
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token payload",
            )
        # TODO place response in a middleware as we are not allowed to modify it here
        response = RedirectResponse(url=request.url.path, status_code=HTTP_303_SEE_OTHER)
        response.set_cookie(key="access_token", value=new_access_token, httponly=True, secure=True, samesite="lax")
        response.set_cookie(key="refresh_token", value=new_refresh_token, httponly=True, secure=True, samesite="lax")
        return user_id
    except PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid access token",
        )
