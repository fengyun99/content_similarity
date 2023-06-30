#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2023/6/30 14:17
# @Author   : FengYun
# @File     : compare_file.py
# @Software : PyCharm
class compare_file:
    def __init__(self, file1, file2):
        self.file1 = file1
        self.file2 = file2

    def get_file(self):
        file = open(f"{self.file1}", "r", encoding="utf-8")
        s1 = file.read()

        file = open(f"{self.file2}", "r", encoding="utf-8")
        s2 = file.read()
        return s1, s2

    def by_set(self):
        tmp_list = []
        s1, s2 = self.get_file()
        set1 = set(s1)
        set2 = set(s2)
        res = set1.intersection(set2)

        tmp = ''
        count = 0
        for s in s1:
            tmp_str = (tmp + s).lstrip().lstrip('\n')
            flag = (s in res) and (tmp_str in s1) and (tmp_str in s2)
            if flag:
                tmp += s
            else:
                res_tmp = tmp.replace('\n', '').replace(' ', '')
                if len(res_tmp) > 12:
                    tmp_result = tmp.strip().strip('\n')
                    tmp_list.append(tmp_result)
                tmp = s

            count += 1
            if count == len(s1):
                res_tmp = tmp.replace('\n', '').replace(' ', '')
                if len(res_tmp) > 12:
                    tmp_result = tmp.strip().strip('\n')
                    tmp_list.append(tmp_result)

        return tmp_list