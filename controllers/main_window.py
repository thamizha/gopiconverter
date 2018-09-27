"""
main_window.py
MainWindow class
"""
__author__ = "Mohanrex"

import logging

from PySide2.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout
)

from resources.constant import Constant
from helpers import qt_helper
from .text_editor_window import TextEditorWindow

class Mainwindow(QMainWindow):
    """
    MainWindow Class
    """
    LOGGER = logging.getLogger()

    def __init__(self):
        """
        Constructor for Mainwindow class
        """
        self.LOGGER.info('Mainwindow init started')
        super(Mainwindow, self).__init__()
        self.window = qt_helper.ui_loader('mainwindow.ui')

        # Create child widget and fill into the container object
        container = self.window.findChild(QWidget, 'container')
        container_widget = TextEditorWindow(container)
        layout = QVBoxLayout(container)
        layout.addWidget(container_widget)
        layout.setMargin(0)
        container.setLayout(layout)

        # Set window properties
        self.window.setWindowTitle(Constant.APP_NAME)
        self.window.showMaximized()
        self.LOGGER.info('Mainwindow initialized')
