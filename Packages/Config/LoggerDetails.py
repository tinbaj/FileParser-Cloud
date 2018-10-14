# LoggerDetails.py
"""
This is a file to create and initialize a logger
"""
import os
import logging.config

class LoggerDetails:
    """
    This is a class to create a logger and return this to the calling function
    """
    def __init__(self):
        self.log_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),'logger.config')
        print(self.log_file_path)
    def setLogger(self):
        """
        This function gets the logger:myAppLogger and returns to the calling Function
        :return: Object of Logger: myAppLogger
        """
        logging.config.fileConfig(self.log_file_path)
        logger = logging.getLogger("myAppLogger")
        return logger
    def __call__(self, *args, **kwargs):
        return self;