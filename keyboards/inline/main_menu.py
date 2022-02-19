from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData


mm_callback = CallbackData('main_menu', 'level')


async def main_menu():
    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(InlineKeyboardButton(text="💼 Кошелек", callback_data=mm_callback.new(level='purse')))
    markup.add(InlineKeyboardButton(text="📈 Статистика", callback_data=mm_callback.new(level='statistic')))
    return markup

