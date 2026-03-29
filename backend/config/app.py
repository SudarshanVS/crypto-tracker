import os

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from config.lifespan import lifespan
from config.settings import ALLOWED_HOSTS

app = FastAPI(lifespan=lifespan)

origins = ALLOWED_HOSTS

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
