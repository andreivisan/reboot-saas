from fastapi import APIRouter, Depends, Request, Response
from fastapi.responses import HTMLResponse
from . import templates

router = APIRouter()

@router.get("/authenticate", response_class=HTMLResponse)
def home(request: Request):
    context = {
            "request": request
    }
    response = templates.TemplateResponse("/authentication/pages/authenticate.html", context)
    return response

@router.get("/login", response_class=HTMLResponse)
def home(request: Request):
    context = {
            "request": request
    }
    response = templates.TemplateResponse("/authentication/fragments/login_form.html", context)
    return response

@router.get("/register", response_class=HTMLResponse)
def home(request: Request):
    context = {
            "request": request
    }
    response = templates.TemplateResponse("/authentication/fragments/register_form.html", context)
    return response
