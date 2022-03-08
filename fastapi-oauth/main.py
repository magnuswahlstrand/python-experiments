from fastapi import FastAPI

from app import app as main_app
from login import app as login_app

app = FastAPI()
app.mount("/auth", login_app)
app.mount("/", main_app)
