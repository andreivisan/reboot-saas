from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from middleware.refresh_token_middleware import refresh_token_middleware
from routers import authenticate, dashboard, root
from components import dashboard_components


app = FastAPI()

app.middleware("http")(refresh_token_middleware)

app.include_router(authenticate.router)
app.include_router(root.router)
app.include_router(dashboard.router)
app.include_router(dashboard_components.router)

origins = [
    "http://localhost:3000", 
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"], 
)

# --------------------------------------------------------------------------------
# Static Files
# --------------------------------------------------------------------------------
app.mount("/static", StaticFiles(directory="static"), name="static")
