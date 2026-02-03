from aiogram.utils.keyboard import InlineKeyboardBuilder
from keyboards.callback_data import CommonCB


def menu_kb():
    kb = InlineKeyboardBuilder()
    kb.button(text="🏠 В меню", callback_data=CommonCB.MENU)
    return kb.as_markup()


def celebrity_dialog_kb():
    kb = InlineKeyboardBuilder()
    kb.button(text="🔄 Сменить звезду", callback_data=CommonCB.CHANGE_STAR)
    kb.button(text="🏠 В меню", callback_data=CommonCB.MENU)
    kb.adjust(2)
    return kb.as_markup()


def back_menu_kb():
    return None