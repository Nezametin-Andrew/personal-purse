from aiogram import types
from aiogram.dispatcher.handler import Handler
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.dispatcher import FSMContext
from loader import dp, bot


@dp.message_handler(CommandStart(), state="*")
async def start(msg: types.Message, state: FSMContext):
    await msg.answer("hello")

