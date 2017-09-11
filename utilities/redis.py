# -*- coding: utf-8 -*-
from contextlib import contextmanager
from random import random
from time import sleep
import traceback

class UnableToGetLock(Exception):
    pass

@contextmanager
def lock(conn, lock_key, lock_value='', timeout=3, expire=None, nowait=False):
    if expire is None:
        expire = timeout

    delay = 0.01 + random() / 10
    attempt = 0
    max_attempts = int(timeout / delay)
    got_lock = None
    while not got_lock and attempt < max_attempts:
        pipe = conn.pipeline()
        pipe.setnx(lock_key, lock_value)
        pipe.expire(lock_key, expire)
        got_lock = pipe.execute()[0]
        if not got_lock:
            if nowait:
                break
            sleep(delay)
            attempt += 1
    print('Acquiring lock on %s' % lock_key)

    if not got_lock:
        raise UnableToGetLock('Unable to fetch lock on %s' % lock_key)

    try:
        yield
    finally:
        print('Releasing lock on %s' % lock_key)

        try:
            conn.delete(lock_key)
        except Exception:
            traceback.print_exc()
