"""
Helper functions related to QT Framework
"""
__author__ = "Mohanrex"

from PySide2.QtCore import QFile
from PySide2.QtUiTools import QUiLoader

def ui_loader(file_name, directory='views/'):
    """
    UI File Loader

    Helper function for loading QT UI file.

    Parameters:
    ===========
        file_name (string): File name of the UI file to be loaded
        directory (string): Directory in which the file is located. Default=views/

    Returns:
    ========
        QWidget: Loaded UI Widget file
    """
    ui_file = QFile(directory + file_name)
    ui_file.open(QFile.ReadOnly)
    loading_frame = QUiLoader().load(ui_file)
    ui_file.close()
    return loading_frame
