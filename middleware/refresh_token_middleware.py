from fastapi import Request
from fastapi.responses import Response

# when tokens are refreshed this middleware is called to add
# the new tokens inside HTTP only cookies to the response
async def refresh_token_middleware(request: Request, call_next):
    response: Response = await call_next(request)
    new_tokens = getattr(request.state, 'new_tokens', None)
    if new_tokens:
        new_access_token, new_refresh_token = new_tokens
        response.set_cookie(
            key="access_token",
            value=new_access_token,
            httponly=True,
            secure=True,
            samesite="lax"
        )
        response.set_cookie(
            key="refresh_token",
            value=new_refresh_token,
            httponly=True,
            secure=True,
            samesite="lax"
        )
    return response
