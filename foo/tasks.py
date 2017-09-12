# -*- coding: utf-8 -*-
from __future__ import absolute_import
from celery.task import task
import time

from demo.settings import REDIS_CLIENT
from utilities.redis import lock

@task
def add(x, y):
    with lock(REDIS_CLIENT, 'add', timeout=5):
        time.sleep(10)
        return x + y