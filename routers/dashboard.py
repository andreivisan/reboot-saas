from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from security.utils import get_current_user
from . import templates

router = APIRouter()

@router.get("/dashboard", response_class=HTMLResponse)
async def home(request: Request, user_id: str = Depends(get_current_user)):
    context = {
            "request": request,
            "user_id": user_id
    }
    response = templates.TemplateResponse("/dashboard/pages/dashboard_home.html", context)
    return response

