from fastapi import FastAPI, HTTPException, Depends,status
from typing import List
import schemas

from fastapi.staticfiles import StaticFiles

from routes import movies,genre
from database import db
from fastapi.middleware.cors import CORSMiddleware

collection=db.users

origins = [
    "http://localhost",  # Allow localhost
    "http://localhost:3000",  # Allow React frontend on localhost:3000
    "http://your-domain.com",  # Add your actual domain here
    # Add other allowed origins as necessary
]

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Allow these origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)

app.mount("/images", StaticFiles(directory="images"), name="images")
app.include_router(movies.router)
app.include_router(genre.router)


