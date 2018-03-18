# This class will map asset type to resource factory class
# and properly load
import os
from wiggler.common.assets import AssetCatalog


class ResourceManager(object):

    def __init__(self, *args, **kwargs):
        super(ResourceManager, self).__init__(*args, **kwargs)
        self._factory_map = {}
        self._catalog = {}
        self._asset_catalog = AssetCatalog()

    def get_resource(self, resource_type, asset_id):
        if resource_type not in self._catalog:
            self._catalog[resource_type] = {}
        factory = self._factory_map[resource_type]
        # From one asset we can create two different resources

        # if the asset id is in the library, mark it as read only
        extra_meta = {}

        # Every project taht wants to use library assets
        # *MUST* clone them first.
        extra_meta['_manager'] = self
        meta = self._asset_catalog.get_asset_by_id(asset_id)
        if 'data_file' in meta:
            data_filename = meta['data_file']
            data_dir = self._asset_catalog.get_datadir_by_id(asset_id)
            data_filepath = os.path.join(data_dir, data_filename)
            extra_meta['_data_filepath'] = data_filepath

        resource = factory(meta, **extra_meta)

        self._catalog[resource_type][asset_id] = resource
        return resource

    def get_resources_list(self, resource_type):
        res_list = []
        for resource_id, resource in self._catalog[resource_type].items():
            res_list.append(resource)

        return res_list

    def new_resource(self, resource_type):
        asset_id = self._asset_catalog.new_asset(resource_type)
        return self.get_resource(resource_type, asset_id)

    def remove_resource(self, resrouce_type, remove_asset=False):
        pass
