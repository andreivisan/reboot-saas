from fastapi import Request, HTTPException
from fastapi.responses import RedirectResponse, Response

async def redirect_middleware(request: Request, call_next):
    print("redirect middleware")
    public_routes_exact = ["/", "/login", "/register"]
    public_routes_prefix = ["/static/"]
    path = request.url.path
    if path in public_routes_exact:
        print("public route exact")
        return await call_next(request)
    if any(request.url.path.startswith(route) for route in public_routes_prefix):
        print("public route prefix")
        return await call_next(request)
    access_token = request.cookies.get("access_token")
    if not access_token:
        print("no access token")
        return RedirectResponse(url="/login", status_code=302)
    try:
        response = await call_next(request)
        return response
    except HTTPException as exc:
        print("refresh token expired or unauthorized")
        if exc.status_code in 401:
            return RedirectResponse(url="/login", status_code=302)
        else:
            raise exc
