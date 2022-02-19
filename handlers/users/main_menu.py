from aiogram import types
from aiogram.dispatcher import FSMContext
from loader import dp, bot
from keyboards.inline.main_menu import mm_callback
from keyboards.inline.purse import purse
from keyboards.inline.cancel import cancel
from .base import BaseCallBackQueryHandler
from utils.request import Request
from utils.blockchain import BlockHandler
from data.msg import statistic_msg


class MainMenuHandler(BaseCallBackQueryHandler):

    def __init__(self, state, call, **kwargs):
        super().__init__(state, call, **kwargs)
        self.methods.update({
            'purse': self.show_menu_purse,
            'statistic': self.show_statistic,
        })

    async def show_menu_purse(self):
        markup = await purse()
        return {
            "text": "⬇ Выбери нужный пункт ⬇",
            "reply_markup": markup.add(await cancel(level=0))
        }

    async def show_statistic(self):
        r = Request(model='balance').request()
        if 'full_balance' in r:
            bl_detail = await BlockHandler(method='get_detail')()
            if 'error' not in bl_detail:
                payment_players = r['full_balance']
                clean_balance = bl_detail['balance'] - float(r['full_balance'])
                return {
                    "text": statistic_msg().format(p_m=str(payment_players)[:5], balance=str(clean_balance)),
                    "reply_markup": types.InlineKeyboardMarkup(row_width=1).add(await cancel(level=0))
                }


@dp.callback_query_handler(mm_callback.filter(), state="*")
async def main_menu(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    mm_h = MainMenuHandler(state=state, call=call, method=callback_data.get('level'), kwargs=callback_data)
    answer = await mm_h.process_update()
    await call.message.edit_text(answer['text'])
    await call.message.edit_reply_markup(answer['reply_markup'])
