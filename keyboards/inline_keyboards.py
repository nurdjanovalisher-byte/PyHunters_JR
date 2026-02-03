from collections import namedtuple

from aiogram.utils import keyboard
from aiogram.utils.keyboard import InlineKeyboardBuilder

from .callback_data import CallbackMenu, CallbackTalk, CallbackQUIZ

import os
from utils.enum_path import Path
from utils import FileManager

Button = namedtuple('Button', ['text', 'callback'])

def ikb_main_menu():
    keyboard = InlineKeyboardBuilder()
    buttons = [
        Button ('Рандомный факт', 'random'),
        Button('Узнать у GTP', 'gpt'),
        Button('Разговор со звездой', 'talk'),
        Button('КВИЗ!', 'quiz'),
    ]
    for button in buttons:
        keyboard.button(
            text = button.text,
            callback_data = CallbackMenu(button = button.callback),
        )
    keyboard.adjust(2,2)
    return keyboard.as_markup()

def ikb_random():
    keyboard = InlineKeyboardBuilder()
    buttons = [
        Button ('Хочу ещё факт!', 'random'),
        Button ('Хватит фактов!', 'start'),
    ]

    for button in buttons:
        keyboard.button(
            text = button.text,
            callback_data = CallbackMenu(button = button.callback),
        )
    return keyboard.as_markup()


def ikb_gpt_menu():
    keyboard = InlineKeyboardBuilder()
    buttons = [
        Button ('Ещё запрос', 'gpt'),
        Button ('Закончить общение', 'start'),
    ]

    for button in buttons:
        keyboard.button(
            text = button.text,
            callback_data = CallbackMenu(button = button.callback),
        )
    return keyboard.as_markup()


def ikb_cancel_gpt():
    keyboard = InlineKeyboardBuilder()
    keyboard.button(
        text = 'Отмена вопроса',
        callback_data = CallbackMenu(button = 'start'),
    )
    return keyboard.as_markup()


def ikb_talk_menu():
    keyboard = InlineKeyboardBuilder()
    celebrity = [file.rsplit('.',1)[0] for file in os.listdir(Path.IMAGES_DIR.value) if file.startswith('talk_')]
    for item in celebrity:
        text_button = FileManager.read_txt(Path.PROMPTS, item).split(',',1)[0].split(' - ')[-1]
        keyboard.button(
            text = text_button,
            callback_data = CallbackTalk(
                button = 'talk',
                celebrity = item,
                )
            )
    keyboard.button(
        text = 'В главное меню',
        callback_data = CallbackMenu(button = 'start'),
    )
    keyboard.adjust(1)
    return keyboard.as_markup()

def ikb_talk_back():
    keyboard = InlineKeyboardBuilder()
    keyboard.button(
        text = 'Закончить разговор',
        callback_data = CallbackMenu(button = 'start')
    )
    return keyboard.as_markup()


def ikb_quiz_menu():
    keyboard = InlineKeyboardBuilder()
    buttons = [
        Button('Программирование','quiz_prog'),
        Button('Математика','quiz_math'),
        Button('Биология','quiz_biology'),
    ]
    for button in buttons:
        keyboard.button(
            text = button.text,
            callback_data = CallbackQUIZ(
            button = 'quiz',
                subject = button.callback,
        )

    )
    keyboard.button(
        text='В главное меню',
        callback_data=CallbackMenu(button='start'),
    )
    keyboard.adjust(1)
    return keyboard.as_markup()


def ikb_quiz_navigation():
    keyboard = InlineKeyboardBuilder()

    keyboard.button(
        text = 'Ещё вопрос',
        callback_data = CallbackQUIZ(
            button = 'quiz',
            subject = 'quiz_more'),
    )

    keyboard.button(
        text = 'Сменить тему!',
        callback_data = CallbackMenu(button = 'quiz')
    )

    keyboard.button(
        text = 'Закончить КВИЗ',
        callback_data = CallbackQUIZ(
            button = 'quiz_finish',
            subject = 'finish',
        )
    )

    return keyboard.as_markup()