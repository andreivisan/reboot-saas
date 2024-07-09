import os
from fastapi import APIRouter
from fastapi.responses import FileResponse

router = APIRouter()

@router.get("/favicon.ico", include_in_schema=False)
async def get_favicon():
    file_path = os.path.join(os.getcwd(), "static", "img", "favicon.ico")
    return FileResponse(file_path)
