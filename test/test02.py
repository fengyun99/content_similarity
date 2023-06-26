from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QFileDialog, QTextEdit
from PyQt5.QtGui import QTextCursor, QTextCharFormat, QColor
import sys

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

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.file_button)
        layout.addWidget(self.file_label)
        layout.addWidget(self.text_edit)

        self.setLayout(layout)

        self.file_button.clicked.connect(self.open_file_dialog)

    def open_file_dialog(self):
        file_dialog = QFileDialog()
        file_dialog.setFileMode(QFileDialog.ExistingFile)
        if file_dialog.exec_():
            selected_files = file_dialog.selectedFiles()
            file_path = selected_files[0]
            self.file_label.setText(file_path)

            with open(file_path, 'r') as file:
                file_content = file.read()
                self.text_edit.setPlainText(file_content)

            if self.label.text() == "左边文件":
                left_file_names.append(file_path)  # 将左边文件的名称添加到left_file_names列表
                print("左边文件列表:", left_file_names)
            elif self.label.text() == "右边文件":
                right_file_names.append(file_path)  # 将右边文件的名称添加到right_file_names列表
                print("右边文件列表:", right_file_names)


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

        compare_button = QPushButton("对比文件")
        compare_button.clicked.connect(self.compare_files)

        clear_button = QPushButton("清除文本")
        clear_button.clicked.connect(self.clear_text)

        button_layout = QVBoxLayout()
        button_layout.addWidget(compare_button)
        button_layout.addWidget(clear_button)

        layout = QVBoxLayout()
        layout.addLayout(main_layout)
        layout.addLayout(button_layout)

        self.setLayout(layout)

    def compare_files(self):
        compare_text = "Sample compare text"

        left_text = self.left_upload_widget.text_edit.toPlainText()
        right_text = self.right_upload_widget.text_edit.toPlainText()

        cursor = QTextCursor(left_text)
        format_ = QTextCharFormat()
        format_.setBackground(QColor("red"))

        # Find and highlight occurrences of compare_text in the left text
        index = left_text.find(compare_text)
        while index != -1:
            cursor.setPosition(index)
            cursor.movePosition(QTextCursor.Right, QTextCursor.KeepAnchor, len(compare_text))
            cursor.mergeCharFormat(format_)
            index = left_text.find(compare_text, index + 1)

        cursor = QTextCursor(right_text)

        # Find and highlight occurrences of compare_text in the right text
        index = right_text.find(compare_text)
        while index != -1:
            cursor.setPosition(index)
            cursor.movePosition(QTextCursor.Right, QTextCursor.KeepAnchor, len(compare_text))
            cursor.mergeCharFormat(format_)
            index = right_text.find(compare_text, index + 1)

    def clear_text(self):
        self.left_upload_widget.text_edit.clear()
        self.left_upload_widget.file_label.clear()
        self.right_upload_widget.text_edit.clear()
        self.right_upload_widget.file_label.clear()


if __name__ == '__main__':
    app = QApplication(sys.argv)

    # 创建窗口
    window = MainWindow()
    window.show()

    sys.exit(app.exec_())

