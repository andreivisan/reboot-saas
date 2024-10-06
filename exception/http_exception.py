from fastapi import Request, HTTPException
from fastapi.exception_handlers import http_exception_handler
from fastapi.responses import RedirectResponse

async def custom_http_exception_handler(request: Request, exc: HTTPException):
    if exc.status_code == 401:
        response = RedirectResponse(url='/login', status_code=302)
        response.delete_cookie("access_token")
        response.delete_cookie("refresh_token")
        return response
    else:
        return await http_exception_handler(request, exc)
