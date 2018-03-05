# This class will map asset type to resource factory class
# and properly load


class ResourceManager(object):

    def __init__(self, *args, **kwargs):
        super(ResourceManager, self).__init__(*args, **kwargs)
        self._factory_map = {}
        self.resources = {}

    def get_resource(self, resource_type, asset_id):
        factory = self._factory_map[resource_type]
        resource = factory(asset_id)
        self.resources[asset_id] = resource
        return resource

    def new_resource(self, resource_type):
        asset_id = 0
        return self.get_resource(resource_type, asset_id)

    def remove_resource(self, resrouce_type, remove_asset=False):
        pass
