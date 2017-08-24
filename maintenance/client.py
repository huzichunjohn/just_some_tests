# -*- coding: utf-8 -*-

import redis

class MaintenanceClient(object):
    def __init__(self):
        self.connection = redis.StrictRedis(host='localhost', port=6379, db=0)

    def get_maintenance_mode(self):
        return self.connection.get('maintenance')

    def set_maintainance_mode(self, maintenance):
        return self.connection.set('maintenance', maintenance)