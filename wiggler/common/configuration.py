import yaml

from wiggler.common.paths import Paths
from wiggler.common.singleton import Singleton

class Configuration(object):
    __metaclass__ = Singleton

    def __init__(self):
        self.paths = Paths()
        with open(self.paths.conf_file_path) as conf_file:
            conf = yaml.load(conf_file)
        for k, v in conf.items():
            setattr(self, k, v)
