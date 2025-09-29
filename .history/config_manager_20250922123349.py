import configparser
import os 
class ConfigManager:
    def __init__(self, filename='settings.ini'):
        self.filename = filename
        self.config = configparser.ConfigParser()
        self._ensure_file()
    