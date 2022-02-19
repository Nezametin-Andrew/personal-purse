from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData


confirm_callback = CallbackData('confirm', 'answer')


async def confirmed():
    markup = InlineKeyboardMarkup(row_width=1)
    markup.add(InlineKeyboardButton(text="✔ Подтвердить", callback_data=confirm_callback.new(answer='true')))
    markup.add(InlineKeyboardButton(text="❌ Отмена", callback_data=confirm_callback.new(answer='false')))
    return markup
