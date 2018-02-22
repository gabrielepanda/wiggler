
class ResourceManager(object):

    def __init__(self):
        self.factory_map = {}
        self.resources = {}

    def new_resource(self, resource_type):
        resource_class = self.factory_map[resource_type]
        resource = resource_class(0)
        resource.create_asset()

    def load_resource_from_asset(self, resource_type, asset_id):
        resource_class = self.factory_map[resource_type]
        resource = resource_class(asset_id)
        self.resources[asset_id] = resource

    def remove_resource(self, resrouce_type, remove_asset=False):
