from aiogram import Router, Bot
from aiogram.filters import Command, CommandObject
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.types.input_file import FSInputFile
from aiogram.filters import StateFilter


from keyboards import ikb_main_menu
import config
from utils import FileManager
from utils.enum_path import Path

from utils.logger import logger

from texts import Common
from texts import Errors, Hints




command_router = Router()



@command_router.message(Command('start'))
async def command_start(message: Message, command: CommandObject, state: FSMContext):
    await state.clear()
    user = message.from_user
    username = user.username or user.full_name
    logger.info(f"User {user.id} ({username}) used /start")

    await message.answer_photo(
        photo = FSInputFile(Path.IMAGES.value.format(file=command.command)),
        caption = Common.START,
        reply_markup = ikb_main_menu(),
    )

@command_router.message(Command("menu"), StateFilter("*"))
async def command_menu(message: Message, state: FSMContext):
    await state.clear()
    await message.answer_photo(
        photo=FSInputFile(Path.IMAGES.value.format(file = "start")),
        caption=FileManager.read_txt(Path.MESSAGES, "start"),
        reply_markup=ikb_main_menu()
    )

@command_router.message(Command("stop"), StateFilter("*"))
async def command_stop(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Диалог завершён. Возвращаю в главное меню.")
    await message.answer_photo(
        photo=FSInputFile(Path.IMAGES.value.format(file = "start")),
        caption=FileManager.read_txt(Path.MESSAGES, "start"),
        reply_markup=ikb_main_menu()
    )


@command_router.message()
async def all_messages(message: Message, bot: Bot):
    logger.info(
        f"User {message.from_user.id} sent message: {message.text}"
    )

    msg_text = f'Пользователь {message.from_user.full_name} написал:\n{message.text}'

    await bot.send_message(
        chat_id = config.ADMIN_ID,
        text = msg_text
    )


