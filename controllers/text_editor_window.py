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
    QMessageBox,
    QComboBox
)

from PySide2.QtGui import QStandardItemModel, QStandardItem
from PySide2.QtCore import QFile, QTextStream, Signal, QModelIndex, Qt

from tamil import txt2unicode

#from pyth.plugins.rtf15.reader import Rtf15Reader
#from pyth.plugins.xhtml.writer import XHTMLWriter

from helpers import qt_helper
from resources.constant import Constant


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
        
        self.cmb_source_encoding = self.window.findChild(QComboBox, 'cmb_source_encoding')
        self.cmb_dest_encoding = self.window.findChild(QComboBox, 'cmb_dest_encoding')        
        
        self.te_input = self.window.findChild(QTextEdit, 'te_input')
        self.te_output = self.window.findChild(QTextEdit, 'te_output')

        self.dest_encodings_model = QStandardItemModel()
        self.source_encodings_model = QStandardItemModel()

        for i in Constant.SUPPORTED_ENCODINGS:    
           item =  QStandardItem()     
           item.setData(Constant.SUPPORTED_ENCODINGS[i], Qt.DisplayRole)      
           item.setData(i, Qt.UserRole)                      
           self.source_encodings_model.appendRow(item)

        self.cmb_source_encoding.setModel(self.source_encodings_model)    

        self.setLayout(layout)
        self.connect_signal()
        
        self.prepare_destination_model("anjal")   

        self.on_source_changed(0)
        
        self.LOGGER.info('Text Editor initialized')

    def connect_signal(self):
        """
        Signal connectors

        Connect buttons and all other signals to its respective slots
        """
        self.LOGGER.info('Connecting signals')
        btn_open_file = self.window.findChild(QPushButton, 'btn_open_file')
        btn_clear_te = self.window.findChild(QPushButton, 'btn_clear')
        btn_save_file = self.window.findChild(QPushButton, 'btn_save_file')        

        btn_open_file.clicked.connect(self.open_file_dialog)
        btn_clear_te.clicked.connect(self.clear_te)   
        self.cmb_source_encoding.currentIndexChanged.connect(self.on_source_changed)
        self.cmb_dest_encoding.currentIndexChanged.connect(self.on_dest_changed)
        self.te_input.textChanged.connect(self.convert)

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
        pass
        # try:
        #     input_text_edit = self.window.findChild(QTextEdit, 'te_input')
        #     name, extension = os.path.splitext(file_name)
        #     if extension == '.rtf':
        #         input_file = open(file_name, 'rb')
        #         doc = Rtf15Reader.read(input_file)
        #         input_text_edit.setText(XHTMLWriter.write(doc, pretty=True).read().decode('utf-8'))
        #         input_file.close()
        #     elif extension == '.txt':
        #         input_file = QFile(file_name)
        #         if not input_file.open(QFile.ReadOnly | QFile.Text):
        #             QMessageBox.warning(
        #                 self,
        #                 "Error",
        #                 "Cannot read file " + name
        #             )
        #             return
        #         input_file_stream = QTextStream(input_file)
        #         input_text_edit.setPlainText(input_file_stream.readAll())
        #         input_file.close()
        #     else:
        #         QMessageBox.warning(self, "Error", "Unsupported file format for file " + name)    
        # except Exception as error:
        #     self.LOGGER.error('Opening File failed for %s', file_name)
        #     self.LOGGER.error('Error type %s', type(error))
        #     self.LOGGER.error(error, exc_info=True)
        #     QMessageBox.warning(self, "Error", "Cannot read file " + file_name)
        #     returnbtn_save_file

    def prepare_destination_model(self, source_selection = ""):        
        self.dest_encodings_model.clear()
        for i in Constant.SUPPORTED_ENCODINGS:            
            item =  QStandardItem(Constant.SUPPORTED_ENCODINGS[i])
            item.setData(i, Qt.UserRole)
            self.dest_encodings_model.appendRow(item)

       
        # if source_selection == "unicode":
        #     for i in Constant.SUPPORTED_ENCODINGS:  
        #         if i != "unicode": 
        #             item =  QStandardItem(Constant.SUPPORTED_ENCODINGS[i])
        #             item.setData(i, Qt.UserRole)
        #             self.dest_encodings_model.appendRow(item)
                
        # else:
        #     item = QStandardItem("Unicode")
        #     item.setData(item)
        #     item.setData("unicode", Qt.UserRole)
        #     self.dest_encodings_model.appendRow(item)
        
        self.cmb_dest_encoding.setModel(self.dest_encodings_model)        

    def on_source_changed(self, index):
        #source_selection = self.cmb_source_encoding.itemData(index, Qt.UserRole)
        # self.prepare_destination_model(source_selection)   
        self.convert()   

    def on_dest_changed(self, index):
        self.convert()   
       
    def convert(self):        
        source_encoding = self.cmb_source_encoding.itemData(self.cmb_source_encoding.currentIndex(), Qt.UserRole)
        dest_encoding = self.cmb_dest_encoding.itemData(self.cmb_dest_encoding.currentIndex(), Qt.UserRole)
        txt_to_convert = self.te_input.toPlainText()

        if source_encoding != dest_encoding :
            if dest_encoding != "unicode":
                if source_encoding != "unicode":
                    tmp_dest_encoding = "unicode"
                    intermediate_func = getattr(txt2unicode, source_encoding + "2" + "unicode")
                    txt_to_convert = intermediate_func(txt_to_convert)
                    source_encoding = "unicode"


            conversion_function_to_call = getattr(txt2unicode, source_encoding + "2" + dest_encoding) 
            converted_string = conversion_function_to_call(txt_to_convert)

        else:
            converted_string = txt_to_convert        

        self.te_output.setPlainText(converted_string)
        
