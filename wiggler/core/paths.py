import pkg_resources

from wiggler.core.singleton import Singleton

class Paths(object):
    __metaclass__ = Singleton

    def __init__(self, package_name):
        req = pkg_resources.Requirement(package_name)
        ws = pkg_resources.WorkingSet()
        eid = ws.find(req)
        self.dist_location = eid.location
        #self.pkg_base = pkg_resources.resource_filename(package_name, "")


