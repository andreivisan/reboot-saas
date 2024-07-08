from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers.authenticate import Authenticate


app = FastAPI()

app.include_router(Authenticate.router)

origins = [
    "http://localhost:3000", 
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # You can restrict this to only what's needed (GET, POST, etc.)
    allow_headers=["*"],  # You can restrict headers if needed
)


