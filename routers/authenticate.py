import os
from dotenv import load_dotenv
from fastapi import APIRouter, Depends, Form, Request, Response
from fastapi.responses import HTMLResponse
from supabase import create_client, Client
from . import templates
from models.authentication.user import User

router = APIRouter()
load_dotenv()

supabase_url = os.getenv("SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_KEY")
supabase = create_client(supabase_url, supabase_key)

@router.get("/authentication_page", response_class=HTMLResponse)
def home(request: Request):
    context = {
            "request": request
    }
    response = templates.TemplateResponse("/authentication/pages/authenticate.html", context)
    return response

@router.get("/login_form", response_class=HTMLResponse)
def render_login_form(request: Request):
    context = {
            "request": request
    }
    response = templates.TemplateResponse("/authentication/fragments/login_form.html", context)
    return response

@router.get("/register_form", response_class=HTMLResponse)
def render_register_form(request: Request):
    context = {
            "request": request
    }
    response = templates.TemplateResponse("/authentication/fragments/register_form.html", context)
    return response

@router.post("/register", response_class=HTMLResponse)
def register(request: Request, email: str = Form(...), password: str = Form(...)):
    print(email + password)
