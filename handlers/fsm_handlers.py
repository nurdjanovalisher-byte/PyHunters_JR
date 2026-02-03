from http.client import responses

from aiogram import Router, Bot, F
from aiogram.filters import Command, CommandObject
from aiogram.types import Message, InputMediaPhoto, InlineKeyboardMarkup
from aiogram.types.input_file import FSInputFile
from aiogram.enums.chat_action import ChatAction

from keyboards.common import menu_kb
from services.gpt_service import ask_gpt
from .fsm import GPTRequest, CelebrityTalk, QUIZ
from aiogram.fsm.context import FSMContext

from keyboards import ikb_main_menu, ikb_random, ikb_gpt_menu, ikb_talk_back, ikb_quiz_navigation
import config
from utils import FileManager
from utils.enum_path import Path
from utils.logger import logger
from ai_open import chat_gpt
from ai_open.messages import GPTMessage
from keyboards.callback_data import CallbackMenu
from ai_open.enums import GPTRole
from utils.text_utils import pluralize_ball
from utils.text_utils import limit_text
from utils.text_utils import split_text



fsm_router = Router()



@fsm_router.message(GPTRequest.wait_for_request)
async def wait_for_user_request(message: Message, state: FSMContext, bot: Bot):

    text = message.text.strip()
    if not text:
        await message.answer("Введите сообщение")
        return

    if text in ("/menu", "/stop"):
        await state.clear()
        await message.answer_photo(
            photo = FSInputFile(Path.IMAGES.value.format(file="start")),
            caption = FileManager.read_txt(Path.MESSAGES, "start"),
            reply_markup = ikb_main_menu()
        )
        return

    msg_list = GPTMessage('gpt')
    msg_list.update(GPTRole.USER, text)

    try:
        response = await ask_gpt(msg_list, bot)
        parts = split_text(response)
    except Exception as e:
        logger.error(f"GPT request error: {e}")
        await message.answer("Произошла ошибка при работе с ИИ")
        return

    for part in parts:
        await message.answer(part)



@fsm_router.message(CelebrityTalk.dialog)
async def user_dialog_with_celebrity(message: Message, state: FSMContext, bot: Bot):
    message_list = await state.get_value('message')
    celebrity = await state.get_value('celebrity')

    message_list.update(GPTRole.USER, message.text)

    await bot.send_chat_action(
        chat_id=message.from_user.id,
        action=ChatAction.TYPING
    )

    response = await ask_gpt(message_list, bot)
    message_list.update(GPTRole.CHAT, response)
    await state.update_data(messages = message_list)
    await bot.send_photo(
        chat_id=message.from_user.id,
        photo = FSInputFile(Path.IMAGES.value.format(file=celebrity)),
        caption = limit_text(response, 1000),
        reply_markup = ikb_talk_back(),
    )


@fsm_router.message(QUIZ.game)
async def user_answer(message: Message, state: FSMContext, bot: Bot):
    topic_score = await state.get_value('topic_score') or 0
    topic_wrong = await state.get_value('topic_wrong') or 0
    topic_total = await state.get_value('topic_total') or 0

    message_list = await state.get_value('messages')
    message_id = await state.get_value('message_id')
    question = await state.get_value('question')

    message_list.update(
        GPTRole.USER,
        f"Вопрос: {question}\n"
        f"Ответ пользователя: {message.text}\n"
        f"Проверь правильность."
    )

    response = await ask_gpt(message_list, bot)

    topic_total += 1

    if response == 'Правильно!':
        topic_score += 1
    else:
        topic_wrong += 1

    message_list.update(GPTRole.CHAT, response)
    await state.update_data(messages = message_list)

    await state.update_data(
        topic_score = topic_score,
        topic_wrong = topic_wrong,
        topic_total = topic_total
    )

    word = pluralize_ball(topic_score)

    final_text = (
        f"Вопрос:\n{question}\n\n"
        f"Ваш ответ:\n{message.text}\n\n"
        f"Результат:\n{response}\n\n"
        f"Ваш счёт: {topic_score} {word}!"
    )

    await bot.edit_message_media(
        media = InputMediaPhoto(
            media = FSInputFile(Path.IMAGES.value.format(file='quiz')),
            caption = final_text,
        ),
        chat_id = message.from_user.id,
        message_id = message_id,
        reply_markup = ikb_quiz_navigation()
    )
