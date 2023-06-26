#!/usr/bin/env python
# -*- coding: utf-8 -*-
import shutil
from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QFileDialog, \
    QTextEdit, QMessageBox
from PyQt5.QtGui import QTextCursor, QTextCharFormat, QColor
from lib.docx_api import *
from lib.queue_file import process_file_queue
from lib.compare_file import compare_file

# 全局变量
highlight_list = []  # 高亮字段列表
# 创建左右两个文件名称队列，实现先进先出，删除文件
left_file_names = []  # 存储左边文件名的列表
right_file_names = []  # 存储右边文件名的列表


class FileUploadWidget(QWidget):
    def __init__(self, label_text):
        super().__init__()
        self.label = QLabel(label_text)
        self.file_button = QPushButton("上传文件")
        self.file_label = QLabel()
        self.text_edit = QTextEdit()
        self.text_edit.setReadOnly(True)  # 设置为只读模式
        # 初始化列表
        left_file_names.clear()
        right_file_names.clear()
        highlight_list.clear()

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.file_button)
        layout.addWidget(self.file_label)
        layout.addWidget(self.text_edit)

        self.setLayout(layout)

        self.file_button.clicked.connect(self.open_file_dialog)

    def open_file_dialog(self):

        # 获取当前目录
        current_directory = os.getcwd()

        # 当前目录下data目录--判断目录存在吗不存在创建
        current_directory += r"\tmp"

        if not os.path.exists(os.path.abspath(current_directory)):
            os.makedirs(os.path.abspath(current_directory))

        file_dialog = QFileDialog()
        file_dialog.setFileMode(QFileDialog.ExistingFile)

        def read_file(name: str):
            with open(name, 'r', encoding="utf-8") as file:
                file_content = file.read()
                self.text_edit.setPlainText(file_content)

        def label_append(name: str):
            if self.label.text() == "左边文件":
                left_file_names.append(name)  # 将左边文件的名称添加到left_file_names列表
                print("左边文件列表:", left_file_names)
                process_file_queue(left_file_names)
            elif self.label.text() == "右边文件":
                right_file_names.append(name)  # 将右边文件的名称添加到right_file_names列表
                print("右边文件列表:", right_file_names)
                process_file_queue(right_file_names)

        if file_dialog.exec_():
            selected_files = file_dialog.selectedFiles()
            file_path = selected_files[0]
            self.file_label.setText(file_path)
            # 实例化对象
            docx_read = Docx()
            try:
                if file_path.endswith("txt") or file_path.endswith("log"):
                    shutil.copy(file_path, current_directory)
                    file_name = os.path.basename(file_path)
                    new_path = current_directory + "\\" + file_name
                    read_file(new_path)
                    label_append(new_path)
                elif file_path.endswith("docx"):
                    file_name = os.path.basename(file_path)
                    new_name = docx_read.loadDoc(file_name, file_path)
                    read_file(new_name)
                    label_append(new_name)
                elif file_path.endswith("doc"):
                    QMessageBox.warning(window, "提示", "doc文件处理较慢请耐心等待")
                    file_name = os.path.basename(file_path)
                    # 转换doc
                    new_path = docx_read.doc_to_docx(file_path)
                    new_name = docx_read.loadDoc(file_name, new_path)
                    os.remove(new_path)
                    read_file(new_name)
                    label_append(new_name)
                else:
                    raise Exception("不支持该格式的文件")
            except Exception as e:
                QMessageBox.warning(window, "文件类型错误", str(e))

            # 清除高亮
            self.clear_highlight_signal.emit()

    clear_highlight_signal = QtCore.pyqtSignal()


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        main_layout = QHBoxLayout()

        # 创建左边的文件上传栏和文本框
        self.left_upload_widget = FileUploadWidget("左边文件")
        main_layout.addWidget(self.left_upload_widget)
        # 创建右边的文件上传栏和文本框
        self.right_upload_widget = FileUploadWidget("右边文件")
        main_layout.addWidget(self.right_upload_widget)

        button_layout = QHBoxLayout()

        compare_button = QPushButton("对比文件")
        compare_button.clicked.connect(self.compare_files)
        button_layout.addWidget(compare_button)

        layout = QVBoxLayout()
        layout.addLayout(main_layout)

        clear_button = QPushButton("清除文本")
        clear_button.clicked.connect(self.clear_text)
        button_layout.addWidget(clear_button)

        layout.addLayout(button_layout)

        self.setLayout(layout)

        # 连接清除高亮信号与槽函数
        self.left_upload_widget.clear_highlight_signal.connect(self.clear_right_highlight)
        self.right_upload_widget.clear_highlight_signal.connect(self.clear_left_highlight)

    def compare_files(self):
        # 改
        highlight_list.clear()
        try:
            file_list = os.listdir("tmp")
            if len(file_list) < 2:
                raise Exception("请先上传两个对比文件再对比")
            # 获取当前目录
            current_directory = os.getcwd()

            # 当前目录下data目录--判断目录存在吗不存在创建
            current_directory += r"\tmp"

            file1 = current_directory + "\\" + file_list[0]
            file2 = current_directory + "\\" + file_list[1]
            highlight_list.extend(compare_file(file1, file2).by_set())
            if not highlight_list:
                raise Exception("文本不存在重复内容")
            # 设置高亮颜色
            format_ = QTextCharFormat()
            format_.setBackground(QColor("yellow"))

            # 高亮左边文本编辑框中的相同部分
            left_cursor = self.left_upload_widget.text_edit.textCursor()

            # 清除之前的高亮
            self.clear_left_highlight()

            for text in highlight_list:
                index = self.left_upload_widget.text_edit.toPlainText().find(text)
                while index != -1:
                    left_cursor.setPosition(index)
                    left_cursor.movePosition(QTextCursor.Right, QTextCursor.KeepAnchor, len(text))
                    left_cursor.mergeCharFormat(format_)
                    index = self.left_upload_widget.text_edit.toPlainText().find(text, index + 1)

            # 高亮右边文本编辑框中的相同部分
            right_cursor = self.right_upload_widget.text_edit.textCursor()

            self.clear_right_highlight()

            for text in highlight_list:
                index = self.right_upload_widget.text_edit.toPlainText().find(text)
                while index != -1:
                    right_cursor.setPosition(index)
                    right_cursor.movePosition(QTextCursor.Right, QTextCursor.KeepAnchor, len(text))
                    right_cursor.mergeCharFormat(format_)
                    index = self.right_upload_widget.text_edit.toPlainText().find(text, index + 1)


        except Exception as e:
            QMessageBox.warning(window, "提示", str(e))

    def clear_left_highlight(self):
        cursor = self.left_upload_widget.text_edit.textCursor()
        format_ = QTextCharFormat()
        format_.setBackground(QColor("white"))

        # 清除之前的高亮
        cursor.setPosition(0)
        cursor.movePosition(QTextCursor.End, QTextCursor.KeepAnchor)
        cursor.mergeCharFormat(format_)

    def clear_right_highlight(self):
        cursor = self.right_upload_widget.text_edit.textCursor()
        format_ = QTextCharFormat()
        format_.setBackground(QColor("white"))

        # 清除之前的高亮
        cursor.setPosition(0)
        cursor.movePosition(QTextCursor.End, QTextCursor.KeepAnchor)
        cursor.mergeCharFormat(format_)

    def clear_text(self):
        self.clear_left_highlight()
        self.clear_right_highlight()
        self.left_upload_widget.text_edit.clear()
        self.left_upload_widget.file_label.clear()
        self.right_upload_widget.text_edit.clear()
        self.right_upload_widget.file_label.clear()
        left_file_names.clear()
        right_file_names.clear()
        highlight_list.clear()
        # 检查文件夹是否存在
        if os.path.exists("tmp"):
            # 删除文件夹及其内部的所有文件
            shutil.rmtree("tmp")

    def closeEvent(self, event):
        # 删除tmp文件夹及其内容
        if os.path.exists('tmp'):
            shutil.rmtree('tmp')

        event.accept()


if __name__ == '__main__':
    app = QApplication(sys.argv)

    # 创建窗口
    window = MainWindow()
    # 设置窗口标题
    window.setWindowTitle("文本查重")
    # 设置窗口尺寸
    window.resize(1000, 700)

    window.show()

    sys.exit(app.exec_())
