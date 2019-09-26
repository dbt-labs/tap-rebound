from tap_rebound.streams.returns_search import ReturnsSearchStream
from tap_rebound.streams.returns import ReturnsStream
from tap_rebound.streams.tracking import TrackingStream

AVAILABLE_STREAMS = [
    ReturnsSearchStream,
    ReturnsStream,
    TrackingStream,
]

__all__ = [
    'ReturnsSearchStream',
    'ReturnsStream',
    'TrackingStream',
]
