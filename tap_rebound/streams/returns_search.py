from tap_rebound.streams.base import BaseStream
from tap_rebound.streams.returns import ReturnsStream
from tap_rebound.streams.tracking import TrackingStream

import singer

LOGGER = singer.get_logger()  # noqa


class ReturnsSearchStream(BaseStream):
    API_METHOD = 'POST'
    TABLE = 'returns_search'
    KEY_PROPERTIES = ['id']

    def __init__(self, config, state, catalog, client, stream_map):
        super().__init__(config, state, catalog, client, stream_map)
        self.substreams = [
            ReturnsStream(config, state, stream_map.get('returns'), client, stream_map),
            TrackingStream(config, state, stream_map.get('tracking'), client, stream_map)
        ]

    def get_body(self, start_date, end_date):
        return {
            "request": {
                "filter": {
                    "date_from": start_date.strftime('%Y/%m/%d'),
                    "date_to": end_date.strftime('%Y/%m/%d'),
                }
            }
        }

    @property
    def path(self):
        return '/returns/search/json'

    def get_stream_data(self, response):
        if response.get('error') and response.get('error').get('code') == 'empty':
            return []
        elif response.get('success'):
            return response['success']['id']
        else:
            raise RuntimeError("bad resp: {}".format(response))

