from aiogram import Router, Bot, F
from aiogram.enums.chat_action import ChatAction
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, InputMediaPhoto
from aiogram.types.input_file import FSInputFile

from services.gpt_service import ask_gpt
from ai_open.enums import GPTRole
from ai_open.messages import GPTMessage
from keyboards import ikb_main_menu, ikb_random, ikb_talk_menu, ikb_quiz_menu
from keyboards.callback_data import CallbackMenu, CallbackTalk, CallbackQUIZ
from utils import FileManager
from utils.enum_path import Path
from utils.logger import logger
from utils.text_utils import limit_text
from utils.text_utils import pluralize_ball
from .fsm import GPTRequest, CelebrityTalk, QUIZ
from utils.text_utils import split_text
from keyboards.common import back_menu_kb, menu_kb, celebrity_dialog_kb
from keyboards.callback_data import CommonCB



inline_router = Router()


@inline_router.callback_query(CallbackMenu.filter(F.button == 'start'))
@inline_router.callback_query(CallbackMenu.filter(F.button == 'main'))
async def main_menu(callback: CallbackQuery, callback_data: CallbackMenu, state: FSMContext, bot: Bot):
    logger.info(
        f"User {callback.from_user.id} pressed {callback_data.button}"
    )
    await state.clear()
    await bot.edit_message_media(
        media = InputMediaPhoto(
            media = FSInputFile(Path.IMAGES.value.format(file=callback_data.button)),
            caption = FileManager.read_txt(Path.MESSAGES, callback_data.button),
        ),
        chat_id = callback.from_user.id,
        message_id = callback.message.message_id,
        reply_markup=ikb_main_menu()
    )


@inline_router.callback_query(CallbackMenu.filter(F.button == 'random'))
async def random_handler(callback: CallbackQuery, callback_data: CallbackMenu, bot: Bot):
    logger.info(
        f"User {callback.from_user.id} pressed {callback_data.button}"
    )
    await bot.edit_message_media(
        media = InputMediaPhoto(
            media = FSInputFile(Path.IMAGES.value.format(file = callback_data.button)),
            caption = FileManager.read_txt(Path.MESSAGES, callback_data.button),
        ),
        chat_id = callback.from_user.id,
        message_id = callback.message.message_id,
    )

    await bot.send_chat_action(
        chat_id = callback.from_user.id,
        action = ChatAction.TYPING,
    )

    response = await ask_gpt(GPTMessage('random'), bot)

    parts = split_text(response)

    await bot.edit_message_media(
        media=InputMediaPhoto(
            media=FSInputFile(Path.IMAGES.value.format(file=callback_data.button)),
            caption=parts[0],
        ),
        chat_id=callback.from_user.id,
        message_id=callback.message.message_id,
        reply_markup=ikb_random(),
    )


@inline_router.callback_query(CallbackMenu.filter(F.button == 'gpt'))
async def gpt_menu(callback: CallbackQuery, callback_data: CallbackMenu, state: FSMContext, bot: Bot):
    logger.info(
        f"User {callback.from_user.id} pressed {callback_data.button}"
    )
    await state.set_state(GPTRequest.wait_for_request)
    await state.update_data(
        message_id=callback.message.message_id,
    )
    msg = await bot.send_message(
        chat_id=callback.from_user.id,
        text="Задай вопрос ChatGPT:\nДля выхода: /menu или /stop",
        reply_markup=menu_kb()
    )

    await state.update_data(gpt_controls_id=msg.message_id)

@inline_router.callback_query(CallbackMenu.filter(F.button == 'talk'))
async def talk_menu(callback: CallbackQuery, callback_data: CallbackMenu, state: FSMContext, bot: Bot):
    logger.info(
        f"User {callback.from_user.id} pressed {callback_data.button}"
    )
    await state.clear()
    await state.update_data(
        message_id=callback.message.message_id,
    )
    await bot.edit_message_media(
        media=InputMediaPhoto(
            media=FSInputFile(Path.IMAGES.value.format(file=callback_data.button)),
            caption=FileManager.read_txt(Path.MESSAGES, callback_data.button),
        ),
        chat_id=callback.from_user.id,
        message_id=callback.message.message_id,
        reply_markup=ikb_talk_menu()
    )



@inline_router.callback_query(CallbackTalk.filter(F.button == 'talk'))
async def talk_with_celebrity(callback: CallbackQuery, callback_data: CallbackTalk, state: FSMContext, bot: Bot):
    logger.info(
        f"User {callback.from_user.id} pressed {callback_data.button}"
    )
    await state.set_state(CelebrityTalk.dialog)
    message_list = GPTMessage(callback_data.celebrity)
    await bot.send_chat_action(
        chat_id=callback.from_user.id,
        action=ChatAction.TYPING
    )
    response = await ask_gpt(message_list, bot)
    message_list.update(GPTRole.CHAT, response)
    await state.update_data(message = message_list, celebrity = callback_data.celebrity)
    await bot.edit_message_media(
        media = InputMediaPhoto(
            media = FSInputFile(Path.IMAGES.value.format(file = callback_data.celebrity)),
            caption = limit_text(response, 1000),
        ),
        chat_id = callback.from_user.id,
        message_id = callback.message.message_id,
        reply_markup=celebrity_dialog_kb()
    )

@inline_router.callback_query(F.data == CommonCB.CHANGE_STAR)
async def change_star(callback: CallbackQuery, state: FSMContext, bot: Bot):
    logger.info(
            f"User {callback.from_user.id} pressed {callback.data}"
    )
    await state.clear()

    await bot.edit_message_media(
        media=InputMediaPhoto(
            media=FSInputFile(Path.IMAGES.value.format(file="talk")),
            caption=FileManager.read_txt(Path.MESSAGES, "talk"),
        ),
        chat_id=callback.from_user.id,
        message_id=callback.message.message_id,
        reply_markup=ikb_talk_menu()
    )

@inline_router.callback_query(CallbackMenu.filter(F.button == 'quiz'))
async def quiz_menu(callback: CallbackQuery, callback_data: CallbackMenu, state: FSMContext, bot: Bot):
    logger.info(
        f"User {callback.from_user.id} pressed {callback_data.button}"
    )
    await state.set_state(QUIZ.game)
    await state.update_data(
        score = 0,
        total_questions = 0,
        wrong_answers = 0
    )
    messages = await state.get_value('messages')
    if not messages:
        await state.update_data(score = 0, messages = None, message_id = callback.message.message_id)
    await bot.edit_message_media(
        media = InputMediaPhoto(
            media = FSInputFile(Path.IMAGES.value.format(file = callback_data.button)),
            caption = FileManager.read_txt(Path.MESSAGES, callback_data.button),
        ),
        chat_id = callback.from_user.id,
        message_id = callback.message.message_id,
        reply_markup = ikb_quiz_menu(),
        )

@inline_router.callback_query(CallbackQUIZ.filter(F.button == 'quiz'))
async def select_subject(callback: CallbackQuery, callback_data: CallbackQUIZ, state: FSMContext, bot: Bot):
    logger.info(
        f"User {callback.from_user.id} pressed {callback_data.button}"
    )

    if callback_data.subject != 'quiz_more':
        await state.update_data(
            topic=callback_data.subject,
            topic_score=0,
            topic_wrong=0,
            topic_total=0,
        )

    message_list = await state.get_value('messages')
    if not message_list:
        message_list = GPTMessage('quiz')

    message_list.update(GPTRole.USER, callback_data.subject)
    await bot.send_chat_action(
        chat_id=callback.from_user.id,
        action=ChatAction.TYPING
    )
    response = await ask_gpt(message_list, bot)

    message_list.update(GPTRole.CHAT, response)

    await state.update_data(
        question=response,
        messages=message_list
    )

    await bot.edit_message_media(
        media = InputMediaPhoto(
            media = FSInputFile(Path.IMAGES.value.format(file = callback_data.button)),
            caption = limit_text(response, 1000),
        ),
        chat_id = callback.from_user.id,
        message_id = callback.message.message_id,
        reply_markup=back_menu_kb()
    )


@inline_router.callback_query(CallbackQUIZ.filter(F.button == 'quiz_finish'))
async def finish_quiz(callback: CallbackQuery, state: FSMContext, bot: Bot):
    logger.info(
            f"User {callback.from_user.id} pressed {callback.data}"
    )

    topic_score = await state.get_value('topic_score') or 0
    topic_wrong = await state.get_value('topic_wrong') or 0
    topic_total = await state.get_value('topic_total') or 0

    if topic_total > 0:
        accuracy = round((topic_score / topic_total) * 100) if topic_total > 0 else 0
    else:
        accuracy = 0

    word = pluralize_ball(topic_score)

    text = (
    f"Итоги по теме: {topic_score}\n\n"
    f"Всего вопросов: {topic_total}\n"
    f"Правильных ответов: {topic_score}\n"
    f"Неправильных ответов: {topic_wrong}\n"
    f"Точность: {accuracy}%\n\n"
    f"Финальный счёт: {topic_score} {pluralize_ball(topic_score)}"
    )

    await state.clear()

    await bot.edit_message_media(
        media=InputMediaPhoto(
            media=FSInputFile(Path.IMAGES.value.format(file='start')),
            caption=text
        ),
        chat_id=callback.from_user.id,
        message_id=callback.message.message_id,
        reply_markup=ikb_main_menu()
    )


@inline_router.callback_query(F.data == CommonCB.MENU)
async def menu_handler(callback: CallbackQuery, state: FSMContext, bot: Bot):
    await state.clear()
    logger.info(
        f"User {callback.from_user.id} pressed {callback.data}"
    )
    await state.clear()

    await bot.edit_message_media(
        media=InputMediaPhoto(
            media=FSInputFile(Path.IMAGES.value.format(file="start")),
            caption=FileManager.read_txt(Path.MESSAGES, "start"),
        ),
        chat_id=callback.from_user.id,
        message_id=callback.message.message_id,
        reply_markup=ikb_main_menu()
    )