from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData


callback_purse = CallbackData('purse', 'level')


async def purse():
    markup = InlineKeyboardMarkup(row_width=1)
    markup.add(InlineKeyboardButton(text="➕ Пополнить", callback_data=callback_purse.new(level='added')))
    markup.add(InlineKeyboardButton(text="➖ Перевести", callback_data=callback_purse.new(level='sent')))
    markup.add(InlineKeyboardButton(text="💰 Баланс", callback_data=callback_purse.new(level='balance')))
    return markup
