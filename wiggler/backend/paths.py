import os
import pkg_resources


from wiggler.core.singleton import Singleton

class Paths(object):
    __metaclass__ = Singleton

    def __init__(self, package_name="wiggler"):
        req = pkg_resources.Requirement(package_name)
        ws = pkg_resources.WorkingSet()
        eid = ws.find(req)
        self.dist_location = eid.location
        # is this is not present, try on install dir /var/lib
        self.syslib_base = os.path.join(self.dist_location, "assets")
        self.conf_base = os.path.join(self.dist_location, "default_config")
        self.conf_file_path = os.path.join(self.conf_base, "default-config.yaml")
        try:
            os.stat(self.syslib_base)
        except:
            raise
        self.pkg_base = pkg_resources.resource_filename('wiggler', "")
        self.schemas_base = os.path.join(self.pkg_base, "schemas")
        self.userlib_base = None


