import os
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from . import templates

router = APIRouter()

@router.get("/dasboard/components/data_card", response_class=HTMLResponse)
async def dashboard_data_card(request: Request, total_page_views: int, progress: int):
    card_data = [
            {
                "title": "Total page views",
                "value": 72245,
                "change": {
                    "percentage": -18,
                    "direction": "down"
                    }
                },
            {
                "title": "Total Revenue",
                "value": 51066.67,
                "change": {
                    "percentage": 0,
                    "direction": "none"
                    }
                },
            {
                "title": "Total Paying Users",
                "value": 345,
                "change": {
                    "percentage": -1,
                    "direction": "down"
                    }
                },
            {
                "title": "Total Signups",
                "value": 10516,
                "change": {
                    "percentage": 15,
                    "direction": "up"
                    }
                }
            ]

    context = {
            "request": request,
            "cards": card_data
    }
    response = templates.TemplateResponse("/dashboard/components/dashboard_data_card.html", context)
    return response

