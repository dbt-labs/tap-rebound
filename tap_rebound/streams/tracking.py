from tap_rebound.streams.base import SubStream

import singer

LOGGER = singer.get_logger()  # noqa


class TrackingStream(SubStream):
    API_METHOD = 'POST'
    TABLE = 'tracking'
    KEY_PROPERTIES = ['tracking_code']
    REQUIRES = ['returns_search', 'returns']

    @property
    def path(self):
        return '/tracking/get/json'

    def get_body(self, tracking_code):
        return {
            "request": {
                "tracking": {
                    "code": tracking_code
                }
            }
        }

    def get_stream_data(self, response):
        if response.get('success'):
            data = response['success']
            return data
        else:
            raise RuntimeError("bad resp: {}".format(response))

    def incorporate_parent_id(self, obj, parent):
        obj['tracking_code'] = parent
        return obj
