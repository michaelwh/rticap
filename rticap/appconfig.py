'''
A simple system to manage saving and loading configuration settings to files

@author: Michael Hodgson
'''

import os
import pickle

class AppConfig(object):
    '''A simple system to manage saving and loading configuration settings to files'''
    
    def __init__(self, configPath):
        self._config = {}
        self.configPath = configPath
        self.loadConfig()
        
    def setValue(self, key, value):
        """Automatically saves the configuration"""
        self._config[key] = value
        self.saveConfig()
        
    def getValue(self, key):
        """Returns None if value does not exist"""
        if key in self._config:
            return self._config[key]
        else:
            return None

    def loadConfig(self):
        if os.path.exists(self.configPath):
            configFile = open(self.configPath, 'rb')
            self._config = pickle.load(configFile)
            configFile.close()            
        else:
            self._config = {}
        import pprint
        pprint.pprint(self._config)
        
    def saveConfig(self):
        """Should never need to call this, since the config is automatically saved every time a value is set"""
        configDirName = os.path.dirname(self.configPath)
        if os.path.exists(configDirName) == False:
            os.mkdir(configDirName)
        configFile = open(self.configPath, 'wb')
        pickle.dump(self._config, configFile)
        configFile.close()