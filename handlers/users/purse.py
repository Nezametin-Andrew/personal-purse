import asyncio
import pyqrcode
from aiogram import types
from aiogram.dispatcher import FSMContext
from loader import dp, bot
from keyboards.inline.purse import callback_purse
from keyboards.inline.cancel import cancel
from keyboards.inline.confirm_sent import confirmed
from .base import BaseCallBackQueryHandler
from utils.blockchain import BlockHandler
from data.msg import balance_detail
from data.config import ADDRESS_LTC
from states.sent_money import SentMoney


class PurseHandler(BaseCallBackQueryHandler):

    def __init__(self, state, call, **kwargs):
        super().__init__(state, call, **kwargs)
        self.methods.update({
            'added': self.added_balance,
            'sent': self.sent_money,
            'balance': self.get_balance,
            'out_sum': self.check_out_sum,
            'check_address': self.check_address,
        })

    async def added_balance(self):
        img = pyqrcode.create(ADDRESS_LTC)
        img.png('data/address.png', scale=6)
        img = open('data/address.png', 'rb')
        return {
            "text": f"Адрес: {ADDRESS_LTC}",
            "img": img,
            "reply_markup": types.InlineKeyboardMarkup(row_width=1).add(await cancel(level=1))
        }

    async def get_balance(self):
        r = await BlockHandler(method='get_detail')()
        if "error" not in r:
            return {
                "text": balance_detail().format(balance=str(r['balance']), un_balance=str(r['unconfirmed_balance'])),
                "reply_markup": types.InlineKeyboardMarkup(row_width=1).add(await cancel(level=1))
            }

    async def sent_money(self):
        state = await self.state.get_state()
        if state is not None:
            await self.state.finish()

        r = await BlockHandler('get_detail')()
        if "error" not in r:
            if r['balance']:
                if r['balance'] > 0.0001:
                    await SentMoney.coin.set()
                    return {
                        "text": f"Введите сумму. которую хотите перевести, без пробелов и спецсимволов.\nНапример: 0.01\nДоступно для вывода {str(r['balance'] - 0.0001)} ltc",
                        "reply_markup": types.InlineKeyboardMarkup(row_width=1).add(await cancel(level=1))
                    }
            return {
                "text": "🤷‍♂ На счеты недостаточно средств для вывода",
                "reply_markup": types.InlineKeyboardMarkup(row_width=1).add(await cancel(level=1))
            }

    async def check_out_sum(self):
        r = await BlockHandler('get_detail')()
        if await self.validate_out_sum(self.opt_data.get('out_sum'), r['balance']):
            await self.state.update_data(coin=float(self.opt_data.get('out_sum')))
            await SentMoney.address.set()
            return {
                "text": "Введите адрес на который хотите перевести, без пробелов и спецсимволов",
                "reply_markup": types.InlineKeyboardMarkup(row_width=1).add(await cancel(level=2))
            }
        return {
            "show_alert": "❌ Не коректный ввод или сумма превышает максимально допустимую"
        }

    async def check_address(self):
        r = await BlockHandler('get_detail_address', address=self.opt_data.get('address')).get_detail_address()
        if "error" not in r:
            await self.state.update_data(address=self.opt_data.get('address'))
            data = await self.state.get_data()
            return {
                "text": f"Перевести сумму: {data['coin']} ltc.\nПо адресу: {data['address']} ?",
                "reply_markup": await confirmed()
            }
        return {
            "show_alert": "❌ Такого адреса не существует"
        }

    async def validate_out_sum(self, n, ac_amount):
        try:
            if float(n.strip()) <= float(ac_amount) - 0.001:
                return True
            return False
        except Exception as e:
            print(e)
            return False


@dp.callback_query_handler(callback_purse.filter(), state="*")
async def purse_menu(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    p_h = PurseHandler(
        call=call, method=callback_data.get('level'), state=state, kwargs=callback_data)
    answer = await p_h.process_update()
    if "img" in answer:
        await bot.send_photo(chat_id=call.from_user.id, photo=answer['img'])
        await bot.send_message(text=answer['text'], chat_id=call.from_user.id)
        await bot.send_message(
            chat_id=call.from_user.id,
            text=f"Воспользуйтесь qr кодом или адресом, чтобы пополнить счет.",
            reply_markup=answer['reply_markup'], parse_mode="HTML")
    else:
        await call.message.edit_text(answer['text'])
        await call.message.edit_reply_markup(answer['reply_markup'])
        if await state.get_state() == "SentMoney:coin":
            await state.update_data(msg_id=call.message.message_id)


@dp.message_handler(state=SentMoney.coin)
async def get_coin_sum(msg: types.Message, state: FSMContext):
    p_h = PurseHandler(call=msg, method='out_sum', state=state, out_sum=msg.text.strip())
    answer = await p_h.process_update()
    if "show_alert" in answer:
        messages = await msg.answer(text=answer['show_alert'])
        await asyncio.sleep(5)
        await messages.delete()
        await msg.delete()
    else:
        data = await state.get_data()

        await bot.edit_message_text(chat_id=msg.from_user.id, text=answer['text'], message_id=data['msg_id'])
        await bot.edit_message_reply_markup(
            chat_id=msg.from_user.id, reply_markup=answer['reply_markup'], message_id=data['msg_id'])
        await msg.delete()


@dp.message_handler(state=SentMoney.address)
async def get_address(msg: types.Message, state: FSMContext):
    p_h = PurseHandler(call=msg, method='check_address', state=state, address=msg.text.strip())
    answer = await p_h.process_update()
    if "show_alert" in answer:
        messages = await msg.answer(text=answer['show_alert'])
        await asyncio.sleep(5)
        await messages.delete()
        await msg.delete()
    else:
        data = await state.get_data()
        await bot.delete_message(chat_id=msg.from_user.id, message_id=data['msg_id'])
        await bot.send_message(
            chat_id=msg.from_user.id,
            text=answer['text'], reply_markup=answer['reply_markup'])
        await msg.delete()
