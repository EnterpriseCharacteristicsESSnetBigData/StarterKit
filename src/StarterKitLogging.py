# -*- coding: utf-8 -*-

"""
Source code for the OBEC Starter Kit Logging class.
TODO: 
"""

import logging


# Class StarterKitLogging contains functions responsible for logging 
# the process of finding OBECs of Enterprises.
# These are the variables that this class uses:
#    log_path - directory where event logging information is saved.
#    log_file - name of a events log file.
#variables = {
#    'log_path': '.\\logs\\',
#    'log_file': 'OBEC_Starter_Kit_Log_Data.log',
#}

class StarterKitLogging:

    def __init__(self, iterable=(), **kwargs):
        self.__dict__.update(iterable, **kwargs)

    def start_logging(self):
        logging.basicConfig(
            filename = '{0}{1}'.format(self.log_path, self.log_file),
            filemode = 'a',
            format = ('%(asctime)s ----- %(levelname)s ::::: ' \
                      '%(message)s ..... (%(name)s)'),
            datefmt = '%Y-%m-%d %H:%M:%S %Z %z',
            level = logging.DEBUG
        )
        logging.info('Start {0}'.format(''))

    def end_logging(self):
        logging.info('End {0}'.format(''))
