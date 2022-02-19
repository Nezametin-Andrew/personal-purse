import blockcypher
from data.config import BlOCKCYPHER_TOKEN, ADDRESS_LTC, PRIV_KEY


class BlockHandler:

    COIN = 0.00000001

    def __init__(self, method=None, address=None):
        self.method = method
        self.address = address
        self.methods = {
            "get_detail": self.get_detail,
            'get_detail_address': self.get_detail_address
        }

    async def get_detail(self):
        try:
            detail = blockcypher.get_address_details(coin_symbol='ltc', api_key=BlOCKCYPHER_TOKEN, address=ADDRESS_LTC)
            if "error" not in detail:
                return self.serialize_balance(detail)
        except Exception as e:
            print(e)
            return {"error": "bad request"}

    async def get_detail_address(self):
        try:
            detail = blockcypher.get_address_details(coin_symbol='ltc', api_key=BlOCKCYPHER_TOKEN, address=self.address)
            if "error" not in detail:
                return self.serialize_balance(detail)
            return {"error": "bad request"}
        except Exception as e:
            print(e)
            return {"error": "bad request"}

    async def __call__(self, *args, **kwargs):
        return await self.methods[self.method]()

    async def sent_money(self, address, coin):
        try:
            detail = blockcypher.simple_spend(
                coin_symbol='ltc', from_privkey=PRIV_KEY,
                to_address=address, to_satoshis=self.reverse_convert(float(coin)), api_key=BlOCKCYPHER_TOKEN
            )
            if "error" not in detail:
                return True
            return False
        except Exception as e:
            print(e)
            return False

    def convert(self, n):
        return n * self.COIN

    def reverse_convert(self, n):
        return int(n / self.COIN)

    def serialize_balance(self, resp):
        if isinstance(resp, dict):
            if 'balance' in resp:
                resp['balance'] = self.convert(resp['balance'])
            if 'unconfirmed_balance' in resp:
                resp['unconfirmed_balance'] = self.convert(resp['unconfirmed_balance'])
        return resp
