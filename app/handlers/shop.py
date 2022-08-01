from app.models.schemas import Product, User, Upload
from app.lib.fql import FQLModel as Q
from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse

app = APIRouter()

@app.post("/product/{name}/{title}/{subtitle}/{description}/{price}/{tags}}")
async def create_product(request: Request, name: str, title: str, subtitle: str, description: str, price: float, tags: str):
    return JSONResponse({"message": "Product created"})