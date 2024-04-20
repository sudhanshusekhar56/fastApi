from fastapi import FastAPI
from enum import Enum

app = FastAPI()

class AvailableCusinines(str,Enum):
    indian:"indian"
    american:"american"
    italian:"italian"

foodItems = {
    'indian':['samosa','dosa'],
    'american':['hot dog', 'apple pie'],
    'italian':['ravioli','pizza']
}

validCuisines = foodItems.keys()

@app.get('/getItems/{cuisine}')
async def getItems(cuisine:AvailableCusinines):
    if cuisine not in foodItems:
        return f"Supported cuisines are {validCuisines}"
    return foodItems.get(cuisine)



coupon_code = {
    1:"10%",
    2:"20%",
    3:"30%"
}

@app.get('/getCoupon/{code}')
async def getitems(code:int):
    return {'discount amount': coupon_code.get(code)}