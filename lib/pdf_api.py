#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2023/6/30 14:25
# @Author   : FengYun
# @File     : pdf_api.py
# @Software : PyCharm
import os
from pypdf import PdfReader



class PdfApi:
    def __init__(self, file_path):
        self.file_path = file_path

    # 读取pdf文件的内容，返回内容
    def read_pdf_paragraphs(self):
        if self.file_path is None:
            raise ValueError('pdf_path not exists')

        if not os.path.exists(self.file_path):
            raise ValueError('pdf_path not exists')
        pdf_file = None
        try:
            pdf_file = open(self.file_path, 'rb')
            pdf_reader = PdfReader(pdf_file)
            paragraphs = []
            for page in pdf_reader.pages:
                text_str = page.extract_text()
                if text_str and len(text_str) > 0:
                    tmp_arr = text_str.split("\n")
                    for tmp in tmp_arr:
                        paragraphs.append(tmp)
            return paragraphs
        except Exception as e:
            print('文档pdf解析失败')
            print(e)
            raise Exception('文档pdf解析失败')
        finally:
            if pdf_file is not None:
                pdf_file.close()

    def loadPdf(self):
        base_name = os.path.basename(self.file_path)
        content_list = self.read_pdf_paragraphs()
        message = "".join(content_list).replace("   ", "\n")
        name = f"{base_name}.txt"
        # 确保文件夹存在
        os.makedirs(os.path.dirname(name), exist_ok=True)

        if not os.path.exists(name):
            # 文件不存在，创建文件
            open(name, "w", encoding="utf-8").close()
            with open(name, "w", encoding="utf-8") as f:
                # 进行下一步操作，比如写入内容等
                f.write(message + "\n")
        else:
            # 文件已存在，进行重命名操作
            index = 1
            while os.path.exists(name):
                # 生成新的文件名，添加序号
                name = "tmp/" + f"{name.split('/')[-1]}_{index}.txt"
                index += 1
                print(name)

            with open(name, "w", encoding="utf-8") as f:
                # 进行下一步操作，比如写入内容等
                f.write(message + "\n")
        return name