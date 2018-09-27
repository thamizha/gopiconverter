"""
text_editor_window.py
TextEditorWindow Class
"""
__author__ = "Mohanrex"

import logging
import os

from PySide2.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QPushButton,
    QFileDialog,
    QTextEdit,
    QMessageBox
)
from PySide2.QtCore import QFile, QTextStream

from pyth.plugins.rtf15.reader import Rtf15Reader
from pyth.plugins.xhtml.writer import XHTMLWriter

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
        self.window = qt_helper.ui_loader('text_editor.ui')
        layout = QHBoxLayout(self)
        layout.addWidget(self.window)
        layout.setMargin(0)
        self.setLayout(layout)
        self.connect_signal()
        self.LOGGER.info('Text Editor initialized')

    def connect_signal(self):
        """
        Signal connectors

        Connect buttons and all other signals to its respective slots
        """
        self.LOGGER.info('Connecting signals')
        btn_open_file = self.window.findChild(QPushButton, 'btn_open_file')
        btn_clear_te = self.window.findChild(QPushButton, 'btn_clear')

        btn_open_file.clicked.connect(self.open_file_dialog)
        btn_clear_te.clicked.connect(self.clear_te)

    def open_file_dialog(self):
        """
        Open File Dialog

        File browse dialog open function
        """
        self.LOGGER.info('Opening file browse dialog')
        file_name = QFileDialog.getOpenFileName(
            self,
            'Open File', '',
            'All Supported Files (*.txt *rtf);;Text Files (*.txt);;Rich Text (*.rtf)'
        )
        if file_name[0] != '':
            self.LOGGER.info('Selected file - %s', file_name)
            self.fill_input_file_content(file_name[0])
        else:
            self.LOGGER.info('No file selected')
    
    def clear_te(self):
        """
        Clear input text edit

        Function which will clear the input text edit
        """
        input_text_edit = self.window.findChild(QTextEdit, 'te_input')
        input_text_edit.clear()

    def fill_input_file_content(self, file_name):
        """
        Fill input file content to Input text edit

        Function which will open the input file and copy its content to the input text edit

        Parameters:
        ===========
            file_name   :   path of the input source file
        """
        try:
            input_text_edit = self.window.findChild(QTextEdit, 'te_input')
            name, extension = os.path.splitext(file_name)
            if extension == '.rtf':
                input_file = open(file_name, 'rb')
                doc = Rtf15Reader.read(input_file)
                input_text_edit.setText(XHTMLWriter.write(doc, pretty=True).read().decode('utf-8'))
                input_file.close()
            elif extension == '.txt':
                input_file = QFile(file_name)
                if not input_file.open(QFile.ReadOnly | QFile.Text):
                    QMessageBox.warning(
                        self,
                        "Error",
                        "Cannot read file " + name
                    )
                    return
                input_file_stream = QTextStream(input_file)
                input_text_edit.setPlainText(input_file_stream.readAll())
                input_file.close()
            else:
                QMessageBox.warning(self, "Error", "Unsupported file format for file " + name)    
        except Exception as error:
            self.LOGGER.error('Opening File failed for %s', file_name)
            self.LOGGER.error('Error type %s', type(error))
            self.LOGGER.error(error, exc_info=True)
            QMessageBox.warning(self, "Error", "Cannot read file " + file_name)
            return
