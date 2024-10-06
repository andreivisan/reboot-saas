from fastapi import Request, HTTPException
from fastapi.responses import RedirectResponse, Response
from . import logger

async def redirect_middleware(request: Request, call_next):
    public_routes_exact = [
            "/", 
            "/login", 
            "/register", 
            "/reset_pass_input_email", 
            "/reset_pass_send_email",
            "reset_password"
    ]
    public_routes_prefix = ["/static/"]
    path = request.url.path
    if path in public_routes_exact:
        logger.info("redirect for public route exact")
        return await call_next(request)
    if any(request.url.path.startswith(route) for route in public_routes_prefix):
        logger.info("redirect for public route prefix")
        return await call_next(request)
    access_token = request.cookies.get("access_token")
    if not access_token:
        logger.info("missing access token")
        return RedirectResponse(url="/login", status_code=302)
    try:
        response = await call_next(request)
        return response
    except HTTPException as exc:
        logger.info("refresh token expired or unauthorized")
        if exc.status_code in 401:
            return RedirectResponse(url="/login", status_code=302)
        else:
            raise exc
