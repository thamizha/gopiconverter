"""
app.py
Main Application entry file.
Entry file which will instantiate the application main window and intialize all the
components required.
"""
__author__ = "Mohanrex"

import logging
from logging.config import dictConfig

import sys

from PySide2.QtWidgets import QApplication

from controllers.main_window import Mainwindow
from resources.constant import Constant

LOGGING_CONFIG = dict(
    version=1,
    formatters={
        'f': {'format':
              '%(asctime)4s %(name)-4s %(levelname)-4s %(message)s'}
        },
    handlers={
        'h': {'class': 'logging.StreamHandler',
              'formatter': 'f',
              'level': logging.DEBUG}
        },
    root={
        'handlers': ['h'],
        'level': logging.DEBUG,
        },
)

def main():
    """
    Main Runner function
    """
    dictConfig(LOGGING_CONFIG)
    logger = logging.getLogger()
    logger.info('Starting Application')
    app = QApplication(sys.argv)
    main_window = Mainwindow()
    sys.exit(app.exec_())
    logger.info('Application is closed')

if __name__ == "__main__":
    main()
