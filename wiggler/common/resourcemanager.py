# This class will map asset type to resource factory class
# and properly load


class ResourceManager(object):

    def __init__(self):
        super(ResourceManager, self).__init__()
        self.factory_map = {}
        self.resources = {}

    def new_resource(self, resource_type):
        asset_id = 0
        return self.load_resource_from_asset(resource_type, asset_id)

    def load_resource_from_asset(self, resource_type, asset_id):
        resource_class = self.factory_map[resource_type]
        resource = resource_class(asset_id)
        self.resources[asset_id] = resource

        return resource

    def remove_resource(self, resrouce_type, remove_asset=False):
        pass
