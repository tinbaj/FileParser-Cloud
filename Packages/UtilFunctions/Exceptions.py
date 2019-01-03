# Exceptions.py
"""
This is a file which contains class to print user defined exception
"""


class MyError(Exception):
    def __init__(self, exceptionName: str, exceptionString: str):
        self.exceptionName = exceptionName
        self.exceptionString = exceptionString

    def __str__(self):
        return repr(self.exceptionName, self.exceptionString)

    def __repr__(self):
        return '{0} Exception : {1}'.format(self.exceptionName, self.exceptionString)