from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from routers import authenticate, root


app = FastAPI()

app.include_router(authenticate.router)
app.include_router(root.router)

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
