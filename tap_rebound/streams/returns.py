from tap_rebound.streams.base import SubStream

import singer

LOGGER = singer.get_logger()  # noqa


class ReturnsStream(SubStream):
    API_METHOD = 'POST'
    TABLE = 'returns'
    KEY_PROPERTIES = ['id']
    REQUIRES = ['returns_search']

    @property
    def path(self):
        return '/returns/get/json'

    def get_body(self, return_id):
        return {
            "request": {
                "return": {
                    "id": return_id,
                    "type": "id"
                }
            }
        }

    def get_stream_data(self, response):
        if response.get('success'):
            data = response['success']
            # Big ol base64-encoded printing label - get rid of it
            data.pop('label')
            return data
        else:
            raise RuntimeError("bad resp: {}".format(response))

    def incorporate_parent_id(self, obj, parent):
        return obj
