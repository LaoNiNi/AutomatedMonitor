#!/usr/bin/env python
# _*_ coding:utf-8 _*_
__author__ = "BIGNI"
__date__ = "2017/5/1 17:00"

import requests

r = requests.get('http://192.168.1.105:8889/api/client/config/1/',timeout=1000)
print(type(r.json()),r.json())