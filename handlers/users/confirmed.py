import asyncio
from aiogram import types

from aiogram.dispatcher import FSMContext
from loader import dp, bot
from keyboards.inline.confirm_sent import confirm_callback
from .base import BaseCallBackQueryHandler
from utils.blockchain import BlockHandler
from states.sent_money import SentMoney
from .main_menu import MainMenuHandler


class ConfirmHandler(BaseCallBackQueryHandler):

    def __init__(self, state, call, **kwargs):
        super().__init__(state, call, **kwargs)
        self.methods.update({
            'true': self.confirmed,
            'false': self.unconfirmed,

        })

    async def confirmed(self):
        data = await self.state.get_data()
        await self.state.finish()
        if await BlockHandler().sent_money(coin=float(data['out_sum']), address=data['address']):
            return {"status": True, "result": True}
        return {"status": True, "result": False}

    async def unconfirmed(self):
        await self.state.finish()
        return {"status": False, "result": False}


@dp.callback_query_handler(confirm_callback.filter(), state=SentMoney.address)
async def confirmed_sent_money(call: types.CallbackQuery, state: FSMContext, callback_data: dict):
    c_h = ConfirmHandler(call=call, state=state, method=callback_data.get('answer'))
    answer = await c_h.process_update()
    if answer['status']:
        if answer['result']:
            msg = await bot.send_message(chat_id=call.from_user.id, text="✔ Перевод успешно завершен")
        else:
            msg = await bot.send_message(chat_id=call.from_user.id, text="❌ Произошла непредвиденная ошибка, повторите позже")
    else:
        msg = await bot.send_message(chat_id=call.from_user.id,
                                     text="❌ Перевод успешно отменен")

    m_h = MainMenuHandler(call=call, state=state, method='purse')
    answer = await m_h.process_update()
    await call.message.edit_text(answer['text'])
    await call.message.edit_reply_markup(answer['reply_markup'])
    await asyncio.sleep(10)
    await msg.delete()
