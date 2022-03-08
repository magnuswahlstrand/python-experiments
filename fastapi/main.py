from enum import Enum
from typing import Optional

from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}


class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"


@app.get("/models/{model_name}")
def get_model(model_name: ModelName):
    return {"model_name": model_name}


@app.get("/query")
def get_query(q: int):
    return int


favicon_path = 'favicon.ico'
from starlette.responses import FileResponse


@app.get("/favicon.ico")
async def favicon():
    return FileResponse(favicon_path)


from pydantic import BaseModel


class MagnusClass(BaseModel):
    age: int
    name: str
    type: str = "unknown"


@app.post("/model")
def get_model_v2(query: MagnusClass):
    return {"query": query}
