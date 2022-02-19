from aiogram import types
from aiogram.dispatcher import FSMContext
from loader import dp, bot
from keyboards.inline.cancel import cancel_callback, cancel as cn
from keyboards.inline.main_menu import main_menu
from .base import BaseCallBackQueryHandler
from keyboards.inline.purse import purse
from .purse import PurseHandler


class CancelHandler(BaseCallBackQueryHandler):
    def __init__(self, state, call, **kwargs):
        super().__init__(state, call, **kwargs)
        self.methods.update({
            '0': self.show_main_menu,
            '1': self.show_purse_menu,
            '2': self.show_added_balance,
        })

    async def show_main_menu(self):
        state = await self.state.get_state()
        if state is not None:
            await self.state.finish()
        return {
            "text": "⬇️ Выбери нужный пункт ⬇️",
            "reply_markup": await main_menu()
        }

    async def show_purse_menu(self):
        markup = await purse()
        return {
            "text": "⬇ Выбери нужный пункт ⬇",
            "reply_markup": markup.add(await cn(level=0))
        }

    async def show_added_balance(self):
        p_h = PurseHandler(call=self.call, state=self.state, method='sent')
        return await p_h.process_update()


@dp.callback_query_handler(cancel_callback.filter(), state="*")
async def cancel(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    c_h = CancelHandler(method=callback_data.get('level'), call=call, state=state, kwargs=callback_data)
    answer = await c_h.process_update()
    await call.message.edit_text(answer['text'])
    await call.message.edit_reply_markup(answer['reply_markup'])
