#!/usr/bin/env python
# -*- coding: utf-8 -*-
import yaml


class Config:
    def __init__(self):
        # 设置文本框字体，字体大小
        self.FONT = None
        self.FONT_SIZE = None
        # 设置文本框是否为只读模式
        self.READ_ONLY = None
        # 设置高亮的颜色
        self.HIGHLIGHT_COLOR = None
        # 设置编码集
        self.CODE_SET = None

    def load_config(self, config_path:str):
        with open(config_path, "r") as f:
            res = yaml.load(f, Loader=yaml.Loader)
        try:
            self.FONT = res['default'][0]['font']
        except Exception:
            self.FONT = "Arial"

        try:
            self.FONT_SIZE = res['default'][0]['size']
        except Exception:
            self.FONT_SIZE = 10

        try:
            self.READ_ONLY = res['default'][0]['readonly']
        except Exception:
            self.READ_ONLY = True

        try:
            self.HIGHLIGHT_COLOR = res['default'][0]['color']
        except Exception:
            self.HIGHLIGHT_COLOR = "yellow"

        try:
            self.CODE_SET = res['default'][0]['code']
        except:
            self.CODE_SET = "utf-8"
