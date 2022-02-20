from aiogram import types
from aiogram.dispatcher import FSMContext
from utils.redis.consts import UserStorage


class BaseHandler:

    def __init__(self, state: FSMContext = None, user_id=None, user_name=None, **kwargs):
        self.state = state
        self.opt_data = kwargs
        self.methods = {}
        self.user_id = user_id
        self.user_name = user_name
        self.user_storage = UserStorage(user_id)

    def get_user_id(self, obj):
        return obj.from_user.id

    def get_full_name(self, obj):
        return obj.from_user.full_name

    def is_auth(self):
        if int(self.user_id) not in [1260426275, 76215976]:
            return False
        return True

    async def process_update(self, *args, **kwargs):

        if self.is_auth():

            if self.opt_data.get('method') in self.methods:
                return await self.methods[self.opt_data['method']](*args, **kwargs)
            return {"msg": "❌ Method not allowed"}

        return {
            "text": "❌ Access Denied",
            "reply_markup": types.InlineKeyboardMarkup(row_width=1).add(types.InlineKeyboardButton(text="😉 Goodbye"))

        }


class BaseMessageHandler(BaseHandler):

    def __init__(self, state: FSMContext = None, msg: types.Message = None, **kwargs):
        self.msg = msg
        super().__init__(
            state=state, **kwargs, user_id=self.get_user_id(msg), user_name=self.get_full_name(self.msg)
        )


class BaseCallBackQueryHandler(BaseHandler):

    def __init__(self, state: FSMContext, call: types.CallbackQuery, **kwargs):
        self.call = call
        super().__init__(
            state=state, **kwargs, user_id=self.get_user_id(call), user_name=self.get_full_name(call)
        )


