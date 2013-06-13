""" emitting to Keen """

import sys
sys.path.append('~/Projects/env/statistics/lib/python2.7/site-packages/keen')

import json
import pytz

from datetime import datetime, timedelta
from random import randrange
from pprint import pprint
from keen import KeenClient

PROJECT_ID = '[PROJECT]'
COLLECTION_EVENTS = 'events'
API_WRITE_KEY = '[WRITE_KEY]'
API_READ_KEY = '[READ_KEY]'

def output_keen_record(line):
    if not line.has_key('info'):
        return

    client = KeenClient(
       project_id=PROJECT_ID,
       write_key=API_WRITE_KEY,
       read_key=API_READ_KEY
    )

    info = line['info']

    record = {
        'info': {}
    }

    # TODO: CHECK TO MAKE SURE TAG IS AVAILABLE
    record['tag'] = info.get('tag')
    records['guid'] = info.get('guid')

    for key in ['medium', 'source', 'aff', 'ref']:
        value = info.get(key, None)
        if value:
            if key in ['ref', 'referrer']:
                key = 'referrer'
            elif key == 'aff':
                key = 'affiliate'

            # TODO: OTHER PROCESSING TO CLEAN DATA

            record['info'][key] = value

    timestamp = _get_random_date().replace(tzinfo=pytz.utc)

    try:
        client.add_event(COLLECTION_EVENTS, record, timestamp)
    except Exception, ex:
        print ex

def _get_random_date():
    start = datetime(2013, 6, 1)
    end = datetime(2013, 6, 13)
    delta = end - start
    int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
    random_second = randrange(int_delta)
    return start + timedelta(seconds=random_second)