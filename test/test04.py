#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2023/6/27 15:39
# @Author   : FengYun
# @File     : test04.py
# @Software : PyCharm
import yaml
with open("../config/set.yaml", "r") as f :
    res = yaml.load(f, Loader=yaml.Loader)
size = None
try:
    size = res['default'][0]['readonly']
    print(type(size))
except Exception:
    size = 1
finally:
    print(size)