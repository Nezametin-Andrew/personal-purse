from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData


cancel_callback = CallbackData('cancel', 'level')


async def cancel(level=0):
    return InlineKeyboardButton(text="🔙 Назад", callback_data=cancel_callback.new(level=level))
