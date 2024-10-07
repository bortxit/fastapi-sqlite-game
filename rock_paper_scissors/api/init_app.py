from fastapi import FastAPI

from rock_paper_scissors.api.database import engine
from rock_paper_scissors.api.routers import game
from rock_paper_scissors.api import models

#This files initializes the FastAPI app.

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

#Routers
app.include_router(game.router)
