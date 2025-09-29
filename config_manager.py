import configparser
import os 
class ConfigManager:
    def __init__(self, filename='settings.ini'):
        self.filename = filename
        self.config = configparser.ConfigParser()
        self._ensure_file()
        
    def _ensure_file(self):
        if not os.path.exists(self.filename):
            self._create_default()
        self.config.read(self.filename, encoding="utf-8")
        
    def _create_default(self):
        self.config["Audio"] = {"volume": "0.8", "mute": "False"}
        self.config["Player"] = {"name": "Alice", "high_score": "0"}
        with open(self.filename, "w", encoding="utf-8") as f:
            self.config.write(f)
            
    #get setting
    def get(self, section, key, fallback=None):
        return self.config.get(section, key, fallback=fallback)
    
    #set configuration
    def set(self, section, key, value):
        if section not in self.config:
            self.config[section] = {}
        self.config[section][key] = str(value)
        with open(self.filename, "w", encoding="utf-8") as f:
            self.config.write(f)
    