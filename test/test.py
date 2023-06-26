# !/usr/bin/env python
# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QTextEdit
from PyQt5.QtGui import QTextCursor, QTextCharFormat, QColor
import sys


class TextHighlighter(QWidget):
    def __init__(self):
        super().__init__()
        self.text_edit = QTextEdit()
        self.highlight_button = QPushButton("高亮文本")
        self.highlight_button.clicked.connect(self.highlight_text)

        layout = QVBoxLayout()
        layout.addWidget(self.text_edit)
        layout.addWidget(self.highlight_button)

        self.setLayout(layout)

    def highlight_text(self):
        text_list = ["apple", "banana", "orange"]

        cursor = self.text_edit.textCursor()
        format_ = QTextCharFormat()
        format_.setBackground(QColor("yellow"))

        # # 清除之前的高亮
        # self.clear_highlight()

        for text in text_list:
            index = self.text_edit.toPlainText().find(text)
            while index != -1:
                cursor.setPosition(index)
                cursor.movePosition(QTextCursor.Right, QTextCursor.KeepAnchor, len(text))
                cursor.mergeCharFormat(format_)
                index = self.text_edit.toPlainText().find(text, index + 1)

    # def clear_highlight(self):
    #     cursor = self.text_edit.textCursor()
    #     format_ = QTextCharFormat()
    #     format_.setBackground(QColor("white"))
    #
    #     # 清除之前的高亮
    #     cursor.setPosition(0)
    #     cursor.movePosition(QTextCursor.End, QTextCursor.KeepAnchor)
    #     cursor.mergeCharFormat(format_)


if __name__ == '__main__':
    app = QApplication(sys.argv)

    window = TextHighlighter()
    window.show()

    sys.exit(app.exec_())
