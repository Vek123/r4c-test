import contextlib

import pika
from pika.adapters.blocking_connection import BlockingChannel

from django.conf import settings


@contextlib.contextmanager
def get_rabbit_channel() -> BlockingChannel:
    with pika.BlockingConnection(settings.RABBIT_PARAMS) as connection:
        try:
            connection = pika.BlockingConnection(settings.RABBIT_PARAMS)
            channel = connection.channel()
            yield channel
        finally:
            if 'connection' in locals() and connection.is_open:
                connection.close()
