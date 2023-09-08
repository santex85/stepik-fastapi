from datetime import date

from app.bookings.models import Booking
from app.database import async_session_maker
from sqlalchemy import select, and_, or_, func

from app.rooms.models import Room
from app.service.base import BaseService


class BookingService(BaseService):
    model = Booking

    @classmethod
    async def add(cls, user_id, room_id, date_from: date, date_to: date):
        async with async_session_maker() as session:
            booking = Booking(date_from=date_from, date_to=date_to)
            session.add(booking)
            await session.commit()
            booked_rooms = select(Booking).where(
                and_(
                    Booking.room_id == 1,
                    or_(
                        and_(
                            Booking.date_from >= date_from,
                            Booking.date_to <= date_to
                        ),
                        and_(
                            Booking.date_from <= date_from,
                            Booking.date_to > date_from
                        )

                    )
                )
            ).cte("booked_rooms")

            rooms_left = select(
                (Room.quantity - func.count(booked_rooms.c.room_id)).label("rooms_left")
            ).select_from(Room).join(
                booked_rooms, booked_rooms.c.room_id == Room.id
            ).where(Room.id == user_id).group_by(Room.quantity, booked_rooms.c.room_id)
