import os
from fastapi import APIRouter, Request
from fastapi.responses import FileResponse, HTMLResponse
from . import templates

router = APIRouter()

@router.get("/", response_class=HTMLResponse)
async def home(request: Request):
    context = {
            "request": request
    }
    response = templates.TemplateResponse("/home/pages/home.html", context)
    return response

@router.get("/favicon.ico", include_in_schema=False)
async def get_favicon():
    file_path = os.path.join(os.getcwd(), "static", "img", "favicon.ico")
    return FileResponse(file_path)
