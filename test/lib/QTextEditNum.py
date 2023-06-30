from PySide2.QtWidgets import QTextEdit
from PySide2.QtGui import QPainter, QFontMetrics
from PySide2.QtCore import QRect, Qt

class QTextEditNum(QTextEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.line_numbers_width = 0

    def paintEvent(self, event):
        # Let the base class handle the painting of the text area
        super().paintEvent(event)

        # Create a painter to draw the line numbers
        painter = QPainter(self.viewport())

        # Set the font and color for the line numbers
        font_metrics = QFontMetrics(self.font())
        painter.setFont(self.font())
        painter.setPen(self.palette().color(self.foregroundRole()))

        # Calculate the width of the line numbers based on the maximum line count
        line_count = self.document().blockCount()
        max_line_width = font_metrics.width(str(line_count))
        self.line_numbers_width = max_line_width + 10

        # Get the visible rectangle of the text area
        visible_rect = self.viewport().contentsRect()

        # Get the first and last visible blocks
        first_block = self.document().findBlock(self.cursorForPosition(visible_rect.topLeft()).position())
        last_block = self.document().findBlock(self.cursorForPosition(visible_rect.bottomLeft()).position())

        # Calculate the starting position for drawing the line numbers
        top = self.blockBoundingRect(first_block).translated(self.contentOffset()).top()
        bottom = self.blockBoundingRect(last_block).translated(self.contentOffset()).bottom()

        # Iterate over the visible blocks and draw the line numbers
        block = first_block
        while block.isValid() and top <= bottom:
            line_number = block.blockNumber() + 1
            line_position = self.blockBoundingRect(block).translated(self.contentOffset()).topLeft()
            line_rect = QRect(0, line_position.y(), self.line_numbers_width, font_metrics.height())
            painter.drawText(line_rect, Qt.AlignRight, str(line_number))

            # Move to the next block
            block = block.next()
            top = self.blockBoundingRect(block).translated(self.contentOffset()).top()

        painter.end()

        # Adjust the left margin of the text area to accommodate the line numbers
        margin = self.line_numbers_width + self.frameWidth()
        self.setViewportMargins(margin, 0, 0, 0)
