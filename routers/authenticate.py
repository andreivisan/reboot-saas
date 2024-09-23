import os
import json
from dotenv import load_dotenv
from fastapi import APIRouter, Depends, Form, Request, Response
from fastapi.responses import HTMLResponse, RedirectResponse
from gotrue.errors import AuthApiError
from supabase import create_client, Client
from . import templates
from models.authentication.user import User

router = APIRouter()
load_dotenv()

supabase_url = os.getenv("SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_KEY")
supabase = create_client(supabase_url, supabase_key)

@router.get("/login", response_class=HTMLResponse)
def render_login_form(request: Request):
    context = {
            "request": request
    }
    response = templates.TemplateResponse("/authentication/fragments/login_form.html", context)
    return response

@router.get("/register", response_class=HTMLResponse)
def render_register_form(request: Request):
    context = {
            "request": request
    }
    response = templates.TemplateResponse("/authentication/fragments/register_form.html", context)
    return response

@router.post("/register")
def register(request: Request, email: str = Form(...), password: str = Form(...)):
    try:
        # supabase signup without email confirmation - disabled in Supabase
        # if you want email confirmation code needs to be added below
        response = supabase.auth.sign_up({
            "email": email,
            "password": password
        })
        context = {
            "request": request
        }
        return template.TemplateResponse("/authentication/fragments/login_form.html", context)
    except AuthApiError as e:
        error_message = str(e)
        if "User already registered" in error_message:
            error = "User already registered"
        else:
            error = "Registration failed. Please try again."
        context = {
            "request": request,
            "error": error
        }
        return templates.TemplateResponse("/authentication/fragments/register_form.html", context)

@router.post("/login", response_class=HTMLResponse)
def login(request: Request, email: str = Form(...), password: str = Form(...)):
    try:
        response = supabase.auth.sign_in_with_password({
            "email": email,
            "password": password
        })
        if response.session is None:
            raise AuthApiError("Authentication failed")
        # retrieve tokens from session
        access_token = response.session.access_token
        refresh_token = response.session.refresh_token
        # if login successful redirect to /dashboard
        # also attach a cookie for each of the tokens
        redirect_response = RedirectResponse(url="/dashboard", status_code=303)
        redirect_response.set_cookie(
            key="access_token",
            value=access_token,
            httponly=True,
            secure=True,
            samesite="lax"
        )
        redirect_response.set_cookie(
            key="refresh_token",
            value=refresh_token,
            httponly=True,
            secure=True,
            samesite="lax"
        )
        return redirect_response
    except AuthApiError as e:
        error = "Invalid email or password. Please try again."
        context = {
            "request": request,
            "error": error
        }
        return template.TemplateResponse("/authentication/fragments/login_form.html", context)

