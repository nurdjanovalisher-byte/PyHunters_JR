from aiogram import BaseMiddleware
from aiogram.types import CallbackQuery
from utils.logger import logger



class CallbackLoggerMiddleware(BaseMiddleware):
    async def __call__(self, handler, event: CallbackQuery, data):

        user = event.from_user
        username = user.username or user.full_name

        logger.info(
            f"User {user.id} ({username}) clicked button payload = {event.data}"
        )

        return await handler(event, data)
