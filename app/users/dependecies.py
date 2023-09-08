from datetime import datetime

from fastapi import Request, Depends
from jose import jwt, JWTError

from app.config import settings
from app.exceptions import TokenAbsentException, IncorrectTokenFormatException, TokenExpiredException, \
    UserIsNotPresentException
from app.users.service import UserService


def get_token(request: Request):
    token = request.cookies.get("booking_access_token")
    if not token:
        raise TokenAbsentException
    return token


async def get_current_user(token: str = Depends(get_token)):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, settings.ALGORITHM)
    except JWTError:
        raise IncorrectTokenFormatException
    expire = payload.get("exp")
    if (not expire) or (int(expire) < datetime.utcnow().timestamp()):
        raise TokenExpiredException
    user_id = payload.get("sub")
    if not user_id:
        raise UserIsNotPresentException
    user = await UserService.find_by_id(int(user_id))
    if not user:
        raise UserIsNotPresentException
    return user
