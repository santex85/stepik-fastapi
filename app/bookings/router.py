from datetime import date

from fastapi import APIRouter, Request, Depends

from app.bookings.schemas import SBooking
from app.bookings.service import BookingService
from app.users.dependecies import get_current_user
from app.users.models import User

router = APIRouter(
    prefix="/bookings",
    tags=["Бронирования"],
)


@router.get("")
async def get_bookings(user: User = Depends(get_current_user)) -> list[dict[str, SBooking]]:
    return await BookingService.find_all(user_id=user.id)


@router.post("")
async def add_booking(
        room_id: int, date_from: date, date_to: date,
        user: User = Depends(get_current_user)):
    await BookingService.add(user_id=user.id, room_id=room_id, date_from=date_from, date_to=date_to)
