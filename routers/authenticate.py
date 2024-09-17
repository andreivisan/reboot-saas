import os
import json
import bcrypt
from dotenv import load_dotenv
from fastapi import APIRouter, Depends, Form, Request, Response
from fastapi.responses import HTMLResponse
from gotrue.errors import AuthApiError
from supabase import create_client, Client
from . import templates
from models.authentication.user import User

router = APIRouter()
load_dotenv()

supabase_url = os.getenv("SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_KEY")
supabase = create_client(supabase_url, supabase_key)

def _hashpass(pwd: str):
    salt = bcrypt.gensalt()
    hashed_password =  bcrypt.hashpw(pwd.encode('utf-8'), salt)
    return hashed_password.decode('utf-8')

def _verifypass(plain_pwd: str, hashed_pwd: str):
    pass

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
    print(pwd)
    try:
        # supabase signup without email confirmation - disabled in Supabase
        # if you want email confirmation code needs to be added below
        response = supabase.auth.sign_up({
            "email": email,
            "password": pwd
        })
        print(response.session.access_token)

        # redirect to the login page
    except AuthApiError as e:
        if "User already registered" in str(e):
            print("User already registered")
        # return registration page with error

@router.post("/login", response_class=HTMLResponse)
def login(request: Request, email: str = Form(...), password: str = Form(...)):
    # login process

    # if successful send access_token as HTML only cookie

    # if successful send refresh_token as HTML only cookie

    # redirect the user to the dashboard page

    pass


