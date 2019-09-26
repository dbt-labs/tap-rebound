#!/usr/bin/env python3

import singer

import tap_framework
import json
import sys

from tap_rebound.client import ReboundClient
from tap_rebound.streams import AVAILABLE_STREAMS
from tap_framework.streams import is_selected

LOGGER = singer.get_logger()  # noqa


class ReboundRunner(tap_framework.Runner):
    def get_streams_to_replicate(self):
        streams = []

        if not self.catalog:
            return streams

        stream_map = {s.stream: s for s in self.catalog.streams}

        for stream_catalog in self.catalog.streams:
            if not is_selected(stream_catalog):
                LOGGER.info("'{}' is not marked selected, skipping."
                            .format(stream_catalog.stream))
                continue

            for available_stream in self.available_streams:
                if available_stream.matches_catalog(stream_catalog):
                    if not available_stream.requirements_met(self.catalog):
                        raise RuntimeError(
                            "{} requires that that the following are "
                            "selected: {}"
                            .format(stream_catalog.stream,
                                    ','.join(available_stream.REQUIRES)))

                    to_add = available_stream(
                        self.config, self.state, stream_catalog, self.client, stream_map)

                    streams.append(to_add)

        return streams

    def do_discover(self):
        LOGGER.info("Starting discovery.")

        catalog = []

        for available_stream in self.available_streams:
            stream = available_stream(self.config, self.state, None, None, {})

            catalog += stream.generate_catalog()

        json.dump({'streams': catalog}, sys.stdout, indent=4)


@singer.utils.handle_top_exception(LOGGER)
def main():
    args = singer.utils.parse_args(required_config_keys=['token', 'username'])
    client = ReboundClient(args.config)
    runner = ReboundRunner(
        args, client, AVAILABLE_STREAMS)

    if args.discover:
        runner.do_discover()
    else:
        runner.do_sync()


if __name__ == '__main__':
    main()
