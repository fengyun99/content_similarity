#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2023/6/30 14:25
# @Author   : FengYun
# @File     : queue_file.py
# @Software : PyCharm
import os


def process_file_queue(file_list):
    if len(file_list) > 1:
        file_name = file_list.pop(0)
        if os.path.exists(file_name):
            os.remove(file_name)
            print(f"删除文件: {file_name}")
        else:
            print(f"文件没找到: {file_name}")