from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from security.utils import get_current_user
from . import templates
from . import supabase

router = APIRouter()

@router.get("/dashboard", response_class=HTMLResponse)
async def home(request: Request, user_id: str = Depends(get_current_user)):
    user_data = supabase.table("user_profile").select("*").eq("uuid", user_id).execute()
    context = {
            "request": request,
            "user_data": user_data.data[0]
    }
    response = templates.TemplateResponse("/dashboard/pages/dashboard_home.html", context)
    return response

