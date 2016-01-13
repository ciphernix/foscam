import logging
from logging.handlers import RotatingFileHandler

class Logger():
    def __init__(self, log_file, name='logger', max_bytes=1024, backup_count=3, level=logging.DEBUG,
                  log_format='%(asctime)s - %(name)s - %(levelname)s : %(message)s'):
        '''Create custom logging class.'''
        
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)
        file_handler = RotatingFileHandler(log_file, maxBytes=max_bytes, backupCount=backup_count )
        formatter = logging.Formatter(log_format)
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)


    def info(self, message):
        '''Log info level.'''

        self.logger.info(message)


    def debug(self, message):
        '''Log debug level.'''

        self.logger.debug(message)


    def warn(self, message):
        '''log warning level.'''

        self.logger.warn(message)


    def error(self, message):
        '''log error levels.'''

        self.logger.error(message)

    def critical(self, message):
        '''log critical levels.'''

        self.logger.critical(message)

