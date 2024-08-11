import os
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from . import templates

router = APIRouter()

@router.get("/dasboard/components/data_card", response_class=HTMLResponse)
async def dashboard_data_card(request: Request):
    card_data = [
            {
                "title": "Total page views",
                "value": 72245,
                "change": {
                    "percentage": -18,
                    "direction": "down"
                    },
                "icon": "/img/svg/eye_icon.svg"
            },
            {
                "title": "Total Revenue",
                "value": 51066.67,
                "change": {
                    "percentage": 0,
                    "direction": "none"
                    },
                "icon": "/img/svg/cart_icon.svg"
            },
            {
                "title": "Total Paying Users",
                "value": 345,
                "change": {
                    "percentage": -1,
                    "direction": "down"
                    },
                "icon": "/img/svg/bag_icon.svg"
            },
            {
                "title": "Total Signups",
                "value": 10516,
                "change": {
                    "percentage": 15,
                    "direction": "up"
                    },
                "icon": "/img/svg/users_icon.svg"
            }
    ]

    context = {
            "request": request,
            "cards": card_data
    }
    response = templates.TemplateResponse("/dashboard/components/dashboard_data_card.html", context)
    return response

@router.get("/dashboard/components/graph", response_class=HTMLResponse) 
async def dashboard_data_graph(request: Request):
    graph_data = {
            "caption": "Single Dataset Table",
            "data": [
                { "month": "Jan", "progress": 30, "start": 0.0, "end": 0.3 },
                { "month": "Feb", "progress": 50, "start": 0.3, "end": 0.5 },
                { "month": "Mar", "progress": 80, "start": 0.5, "end": 0.8 },
                { "month": "Apr", "progress": 100, "start": 0.8, "end": 1.0 },
                { "month": "May", "progress": 65, "start": 1.0, "end": 0.65 },
                { "month": "Jun", "progress": 45, "start": 0.65, "end": 0.45 },
                { "month": "Jul", "progress": 15, "start": 0.45, "end": 0.15 },
                { "month": "Aug", "progress": 32, "start": 0.15, "end": 0.32 },
                { "month": "Sep", "progress": 60, "start": 0.32, "end": 0.6 },
                { "month": "Oct", "progress": 90, "start": 0.6, "end": 0.9 },
                { "month": "Nov", "progress": 55, "start": 0.9, "end": 0.55 },
                { "month": "Dec", "progress": 40, "start": 0.55, "end": 0.4 }
                ]
    }
    context = {
        "request": request,
        "graph_data": graph_data
    }
    response = templates.TemplateResponse("/dashboard/components/dashboard_graph.html", context)
    return response

@router.get("/dashboard/components/data_table", response_class=HTMLResponse) 
async def dashboard_data_table(request: Request):
    table_data = {
            "headers": ["Name", "Job", "Favorite Color"],
            "rows": [
                { "index": 1, "name": "Cy Ganderton", "job": "Quality Control Specialist", "favorite_color": "Blue" },
                { "index": 2, "name": "Hart Hagerty", "job": "Desktop Support Technician", "favorite_color": "Purple" },
                { "index": 3, "name": "Brice Swyre", "job": "Tax Accountant", "favorite_color": "Red" }
            ]
    }
    context = {
        "request": request,
        "table_data": table_data
    }
    response = templates.TemplateResponse("/dashboard/components/dashboard_data_table.html", context)
    return response
