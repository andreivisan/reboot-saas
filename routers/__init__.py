from fastapi.templating import Jinja2Templates
from logging_config import get_logger

templates = Jinja2Templates(directory="templates")

logger = get_logger(__name__)
