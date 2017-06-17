#!/usr/bin/env python
# _*_ coding:utf-8 _*_
__author__ = "BIGNI"
__date__ = "2017/5/7 9:30"

import redis

def redis_conn(django_settings):
    #print(django_settings.REDIS_CONN)
    pool = redis.ConnectionPool(host=django_settings.REDIS_CONN['HOST'],db=django_settings.REDIS_CONN['DB'], port=django_settings.REDIS_CONN['PORT'])
    r = redis.Redis(connection_pool=pool)
    return  r