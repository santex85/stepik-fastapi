from fastapi import FastAPI, Query, Depends
from typing import Optional
from datetime import date
from pydantic import BaseModel
from app.bookings.router import router as router_bookings
from app.users.router import router as router_users

app = FastAPI()

app.include_router(router_users, prefix="/bookings")
app.include_router(router_bookings, prefix="/users")


class HotelSearchArg:
    def __init__(
            self,
            location: str,
            date_checkin: date,
            date_checkout: date,
            has_spa: Optional[bool] = None,
            stars: Optional[int] = Query(None, ge=1, le=5),
    ):
        self.location = location
        self.date_checkin = date_checkin
        self.date_checkout = date_checkout
        self.has_spa = has_spa
        self.stars = stars


class SHotel(BaseModel):
    address: str
    name: str
    starts: int


@app.get("/hotels")
def get_hotels(search_args: HotelSearchArg = Depends()):
    return search_args
