import os
import pkg_resources

class Paths(object):

    def __init__(self):
        req = pkg_resources.Requirement("wiggler")
        ws = pkg_resources.WorkingSet()
        eid = ws.find(req)
        self.dist_location = eid.location
        # is this is not present, try on install dir /var/lib
        self.syslib_base = os.path.join(self.dist_location, "assets")
        try:
            os.stat(self.syslib_base)
        except:
            raise
        self.pkg_base = pkg_resources.resource_filename('wiggler', "")
        self.schemas_base = os.path.join(self.pkg_base, "schemas")
        self.userlib_base = None


