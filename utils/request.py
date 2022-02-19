import json
import urllib3

from data import config


class Request:

    def __init__(self, model=None, data=None):
        self.url = "http://188.72.209.127/api/v1/" + model
        self.http = urllib3.PoolManager()
        self.data = {
            'token': config.SERVER_TOKEN,
        }
        if data is not None:
            self.data.update(data)

    def __call__(self, *args, **kwargs):
        return self.request()

    def request(self):
        r = self.http.request(
            method="GET",
            url=self.url,
            fields=self.data
        )

        return json.loads(r.data.decode())