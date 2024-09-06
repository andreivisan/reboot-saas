import os
import json
from dotenv import load_dotenv
from fastapi import APIRouter, Depends, Form, Request, Response
from fastapi.responses import HTMLResponse
from gotrue.errors import AuthApiError
from supabase import create_client, Client
from . import templates
from models.authentication.user import User
from passlib.context import CryptContext
from passlib.hash import bcrypt

router = APIRouter()
load_dotenv()

supabase_url = os.getenv("SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_KEY")
supabase = create_client(supabase_url, supabase_key)

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def __hashpass__(pwd: str):
    return pwd_context.hash(pwd)

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
    pwd = __hashpass__(password)
    try:
        # supabase signup without email confirmation - disabled in Supabase
        # if you want email confirmation code needs to be added below
        response = supabase.auth.sign_up({
            "email": email,
            "password": pwd
        })
        print(response.session.access_token)
    except AuthApiError as e:
        if "User already registered" in str(e):
            print("User already registered")


