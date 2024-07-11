from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from . import templates

router = APIRouter()

@router.get("/dashboard", response_class=HTMLResponse)
async def home(request: Request):
    context = {
            "request": request
    }
    response = templates.TemplateResponse("/dashboard/pages/dashboard_home.html", context)
    return response

