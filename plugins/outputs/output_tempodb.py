""" emitting to TempoDB """

import sys
sys.path.append('~/Projects/env/tempo/lib/python2.7/site-packages/tempodb')

import json
from datetime import datetime, timedelta
from random import randrange
from pprint import pprint
from tempodb import Client

API_KEY = '[KEY]'
API_SECRET = '[SECRET]'

def output_print_line(line):
    if not line.has_key('info'):
        return
    info = line['info']

    tracker_key = ''
    referrer_key = ''

    performance_key = _get_performance_key(info)

    if info.has_key('aff'):
        tracker_key = _get_tracker_key(info)

    if info.has_key('ref'):
        referrer_key = _get_referrer_key(info)

    print '------------------------------'
    try:
        for key in [performance_key, tracker_key, referrer_key]:
            if key:
                print key
    except Exception, ex:
        print ex

def output_tempodb_record(line):
    db_client = Client(API_KEY, API_SECRET)

    if not line.has_key('info'):
        return
    info = line['info']

    keys = []
    performance_key = _get_performance_key(info)
    keys.append(performance_key)

    if info.has_key('aff'):
        tracker_key = _get_tracker_key(info)
        keys.append(tracker_key)

    if info.has_key('ref'):
        referrer_key = _get_referrer_key(info)
        keys.append(referrer_key)

    series_list = db_client.get_series(keys=keys)
    series_to_record = []
    for key in keys:
        key_series = None
        for series in series_list:
            if series.key == key:
                key_series = series
                break
        if key_series is None:
            key_series = db_client.create_series(key)
            guid = info.get('guid')
            attrs = {'guid': guid, 'tag': info.get('tag')}
            if '.tracker.' in key:
                tags = ['tracker']
                attrs.update({'tracker': info.get('aff')})
            elif '.referrer.' in key:
                tags = ['referrer']
                attrs.update({'referrer': info.get('ref')})
            else:
                tags = ['performance']
            key_series.tags = tags
            key_series.attributes = attrs
            db_client.update_series(key_series)
        series_to_record.append(key_series)

    time_stamp = _get_random_date()
    data = []
    try:
        for series in series_to_record:
            data.append({'key': series.key, 'v': 4})
        db_client.write_bulk(time_stamp, data)
    except Exception, ex:
        print ex

def _get_performance_key(info):
    return 'guid:{guid}.{tag}.performance.1'.format(
        guid=info.get('guid'),
        tag=info.get('tag')
    ).lower()

def _get_tracker_key(info):
    return 'guid:{guid}.tracker:{tracker}.{tag}.tracker.1'.format(
        guid=info.get('guid'),
        tag=info.get('tag'),
        tracker=info.get('aff'),
    ).lower()

def _get_referrer_key(info):
    return 'guid:{guid}.referrer:{referrer}.{tag}.referrer.1'.format(
        guid=info.get('guid'),
        tag=info.get('tag'),
        referrer=info.get('ref').replace('.', '')
    ).lower()

def _get_random_date():
    start = datetime(2013, 6, 1)
    end = datetime(2013, 6, 12)
    delta = end - start
    int_delta = (delta.days * 24 * 60 * 60) + delta.total_seconds()
    random_second = randrange(int_delta)
    return start + timedelta(seconds=random_second)