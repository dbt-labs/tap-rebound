import requests
import urllib
import json
import singer
import singer.metrics

LOGGER = singer.get_logger()  # noqa


class ReboundClient:

    MAX_TRIES = 5

    def __init__(self, config):
        self.config = config

    def _make_request(self, url, method, payload=None):
        response = requests.request(
            method,
            url,
            headers={
                'Content-Type': "application/x-www-form-urlencoded",
            },
            data=payload
        )

        if response.status_code != 200:
            raise RuntimeError(response.text)

        return response.json()

    def make_request(self, url, method, body):
        payload = {
            'login': self.config.get('username'),
            'api_key': self.config.get('token')
        }

        LOGGER.info("Making request to {} with ({})".format(url, body))

        for k, v in body.items():
            payload[k] = urllib.parse.quote(json.dumps(v))

        payload = "&".join(["{}={}".format(k,v) for (k,v) in payload.items()])
        return self._make_request(url, method, payload)
