"""
    Main Module docstring
"""

import os
import uvicorn
from fastapi import FastAPI
from src.routes.chat import chat
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = {"http://localhost:3000", "http://localhost"}

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat)
