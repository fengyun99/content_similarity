#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os


def process_file_queue(file_list):
    if len(file_list) > 0:
        file_name = file_list.pop(0)
        if os.path.exists(file_name):
            os.remove(file_name)
            print(f"Deleted file: {file_name}")
        else:
            print(f"File not found: {file_name}")
    else:
        print("File list is empty.")


# 示例用法
file_queue = ["lib/file1.txt", "lib/file2.txt", "lib/file3.txt"]
process_file_queue(file_queue)  # 删除并打印 "Deleted file: file1.txt"
process_file_queue(file_queue)  # 删除并打印 "Deleted file: file2.txt"
process_file_queue(file_queue)  # 删除并打印 "Deleted file: file3.txt"
process_file_queue(file_queue)  # 打印 "File list is empty."
