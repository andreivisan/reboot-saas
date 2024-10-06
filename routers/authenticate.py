import json
from fastapi import APIRouter, Depends, Form, Request, Response
from fastapi.responses import HTMLResponse, RedirectResponse
from gotrue.errors import AuthApiError
from . import templates
from . import logger
from . import supabase
from models.authentication.user import User
from security.utils import get_current_user

router = APIRouter()

@router.get("/login", response_class=HTMLResponse)
def render_login_form(request: Request):
    if request.headers.get("HX-Request"):
        # If the request comes from HTMX, return an HX-Redirect header
        redirect_response = Response(status_code=200)
        redirect_response.headers["HX-Redirect"] = "/login"
        return redirect_response
    else:
        context = {
            "request": request
        }
        response = templates.TemplateResponse("/authentication/pages/login_form.html", context)
        return response

@router.get("/register", response_class=HTMLResponse)
def render_register_form(request: Request):
    if request.headers.get("HX-Request"):
        # If the request comes from HTMX, return an HX-Redirect header
        redirect_response = Response(status_code=200)
        redirect_response.headers["HX-Redirect"] = "/register"
        return redirect_response
    else:
        context = {
            "request": request
        }
        response = templates.TemplateResponse("/authentication/pages/register_form.html", context)
        return response

@router.get("/logout", response_class=HTMLResponse)
async def logout(request: Request, response: Response, user_id: str = Depends(get_current_user)):
    supabase_response = supabase.auth.sign_out()
    context = {
        "request": request
    }
    response = templates.TemplateResponse("/authentication/pages/login_form.html", context)
    response.delete_cookie("access_token")
    response.delete_cookie("refresh_token")
    return response

@router.get("/reset_pass_input_email")
async def reset_pass_input_email(request: Request):
    context = {
        "request": request,
        "error": False
    }
    return templates.TemplateResponse("/authentication/pages/reset_pass_input_email.html", context)

@router.post("/reset_pass_send_email")
async def reset_pass_send_email(request: Request, email: str = Form(...)):
    user_data = supabase.table("user_profile").select("*").eq("email", email).execute()
    if not user_data.data:
        logger.warn(f"User with email {email} not found")
        context = {
            "request": request,
            "error": "User email not found"
        }
        return templates.TemplateResponse("/authentication/pages/reset_pass_input_email.html", context)
    supabase.auth.reset_password_email(email, {
        "redirect_to": "http://localhost:8000/reset_password",
    })
    context = {
        "request": request
    }
    return templates.TemplateResponse("/authentication/pages/reset_password_message.html", context)

@router.get("/reset_password")
async def reset_password(request: Request):
    context = {
        "request": request
    }
    return templates.TemplateResponse("/authentication/pages/reset_password.html", context)

@router.post("/register")
def register(request: Request, email: str = Form(...), password: str = Form(...)):
    try:
        # supabase signup without email confirmation - disabled in Supabase
        # if you want email confirmation code needs to be added below
        response = supabase.auth.sign_up({
            "email": email,
            "password": password
        })
        user_profile = {
            "uuid": response.user.id,
            "email": response.user.email
        }
        supabase.table("user_profile").insert(user_profile).execute()
        logger.info("User successfully registered and saved to DB")
        redirect_response = RedirectResponse(url="/login", status_code=302)
        return redirect_response
    except AuthApiError as e:
        error_message = str(e)
        logger.error(error_message)
        if "User already registered" in error_message:
            error = "User already registered"
        else:
            error = "Registration failed. Please try again."
        context = {
            "request": request,
            "error": error
        }
        return templates.TemplateResponse("/authentication/pages/register_form.html", context)

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
        return templates.TemplateResponse("/authentication/pages/login_form.html", context)

