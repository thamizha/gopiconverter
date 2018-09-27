"""
text_editor_window.py
TextEditorWindow Class
"""
__author__ = "Mohanrex"

import logging

from PySide2.QtWidgets import QWidget, QHBoxLayout
from helpers import qt_helper

class TextEditorWindow(QWidget):
    """
    TextEditorWindow Class
    """
    LOGGER = logging.getLogger()

    def __init__(self, parent=None):
        """
        Constructor for TextEditor Window
        """
        self.LOGGER.info('TextEditor init started')
        super(TextEditorWindow, self).__init__(parent)
        widget = qt_helper.ui_loader('text_editor.ui')
        layout = QHBoxLayout(self)
        layout.addWidget(widget)
        layout.setMargin(0)
        self.setLayout(layout)
        self.LOGGER.info('Text Editor initialized')
