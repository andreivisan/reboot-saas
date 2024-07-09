from fastapi import APIRouter, Depends, Request, Response
from fastapi.responses import HTMLResponse
from . import templates

router = APIRouter()

@router.get("/", response_class=HTMLResponse)
def home(request: Request):
    context = {
            "request": request
    }
    response = templates.TemplateResponse("/authentication/pages/authenticate.html", context)
    return response
