import os
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from . import templates

router = APIRouter()

@router.get("/dasboard/components/data_card", response_class=HTMLResponse)
async def dashboard_data_card(request: Request, total_page_views: int, progress: int):
    context = {
            "request": request,
            "total_page_views": total_page_views,
            "progress": progress
    }
    response = templates.TemplateResponse("/dashboard/components/dashboard_data_card.html", context)
    return response

