from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.dispatcher import FSMContext
from loader import dp, bot
from keyboards.inline.main_menu import main_menu
from .base import BaseMessageHandler


@dp.message_handler(CommandStart(), state="*")
async def start(msg: types.Message, state: FSMContext):
    bm_h = BaseMessageHandler(msg=msg, state=state).is_auth()
    if bm_h:
        await msg.answer(text="⬇ Выбери нужный пункт ⬇", reply_markup=await main_menu())
    else:
        await msg.answer(**{
            "text": "❌ Access Denied",
        })
