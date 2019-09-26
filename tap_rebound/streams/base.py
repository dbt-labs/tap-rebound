import math
import pytz
import singer
import singer.utils
import singer.metrics

from datetime import timedelta, datetime

from tap_rebound.config import get_config_start_date
from tap_rebound.state import incorporate, save_state, \
    get_last_record_value_for_table

from tap_framework.streams import BaseStream as base


LOGGER = singer.get_logger()


class BaseStream(base):
    KEY_PROPERTIES = ['id']

    def __init__(self, config, state, catalog, client, stream_map):
        super().__init__(config, state, catalog, client)

    def get_url(self):
        return 'https://intelligentreturns.net/api{}'.format(self.path)

    def sync(self):
        LOGGER.info('Syncing stream {} with {}'
                    .format(self.catalog.tap_stream_id,
                            self.__class__.__name__))

        self.write_schema()
        for substream in self.substreams:
            substream.write_schema()

        return self.sync_data()

    def sync_data(self):
        table = self.TABLE

        delta = timedelta(days=7)
        lookback_delta = timedelta(days=self.config.get('sync_lookback_days', 30))
        start_date = get_last_record_value_for_table(self.state, table)
        if start_date is None:
            start_date = get_config_start_date(self.config)

        start_date -= lookback_delta

        start_date = start_date.date()
        while start_date <= datetime.today().date():
            end_date = start_date + delta
            self.sync_for_period(start_date, end_date)

            start_date = end_date
            end_date += delta

    def sync_for_period(self, start_date, end_date):
        table = self.TABLE
        url = self.get_url()

        body = self.get_body(start_date, end_date)
        response = self.client.make_request(url, self.API_METHOD, body)
        data = self.get_stream_data(response)

        LOGGER.info("Got {} results for range {} to {}".format(len(data), start_date, end_date))

        streams = {s.TABLE: s for s in self.substreams}
        for i, return_id in enumerate(data):
            return_obj = streams['returns'].sync_data(parent=return_id)
            tracking_obj = streams['tracking'].sync_data(parent=return_obj['tracking'])

        self.state = incorporate(self.state,
            table,
            'start_date',
            start_date.isoformat())
        save_state(self.state)

class SubStream(base):
    KEY_PROPERTIES = ['id']

    def __init__(self, config, state, catalog, client, stream_map):
        super().__init__(config, state, catalog, client)

    def get_parent_id(self, parent):
        return paren

    def get_url(self):
        return 'https://intelligentreturns.net/api{}'.format(self.path)

    def sync(self):
        pass

    def sync_data(self, parent=None):
        if parent is None:
            raise RuntimeError('Cannot sync a subobject of null!')

        table = self.TABLE
        url = self.get_url()
        body = self.get_body(parent)

        result = self.client.make_request(url, self.API_METHOD, body)
        obj = self.get_stream_data(result)

        with singer.metrics.record_counter(endpoint=table) as counter:
            singer.write_records(
                table,
                #[self.transform_record(self.incorporate_parent_id(obj, parent))]
                [self.incorporate_parent_id(obj, parent)]
            )
            counter.increment()

        return obj
