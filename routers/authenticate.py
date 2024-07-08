from fastapi import APIRouter, Depends, Request, Response
from fastapi.responses import HTMLResponse
from . import templates


class Authenticate:
    router = APIRouter()

    @staticmethod
    @router.get("/", response_class=HTMLResponse)
    def home(request: Request):
        context = {
                "request": request
        }
        response = templates.TemplateResponse("base.html", context)
        return response
