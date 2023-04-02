import configparser as cp
from . import Paths

class ConfigParser():
    __config = cp.ConfigParser()

    @staticmethod
    def get_config():
        return ConfigParser.__config 

    def change_settings(to_change:str, new_value:str):
        """change settings in ini file"""
        __config.read(Paths.ini)
        cfgfile = open(Paths.ini, 'w')
        __config.set('SETTINGS', to_change, new_value)
        __config.write(cfgfile)
        cfgfile.close()
        __config = cp.ConfigParser()
        __config.read(Paths.ini)