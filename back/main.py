from fastapi import FastAPI, HTTPException, Depends
from typing import List


from fastapi.staticfiles import StaticFiles

from routes import movies,genre

app = FastAPI()

app.mount("/images", StaticFiles(directory="images"), name="images")
app.include_router(movies.router)
app.include_router(genre.router)

