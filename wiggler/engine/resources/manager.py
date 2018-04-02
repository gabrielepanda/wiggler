import os
import imp

from wiggler_project.core.resources.manager import ResourceManager

class EngineResources(ResourceManager):

    def __init__(self, *args, **kwargs):
        super(EngineResources, self).__init__(*args, **kwargs)
        self._factory_map = {
        }
        self.user_modules = {}
        user_code_dir = ":"
        for module_filename in user_code_dir:
            asset_id = os.path.extsep(module_filename)[0]
            module = imp.load_source(self.module_name,
                                    self.module_filename)
            self.user_modules[asset_id] = module

    def get_resource(self, resource_type, asset_id):
        if resource_type == "sprite":
            module = self.user_modules[asset_id]
            self._factory_map['sprite'] = module.Sprite
        super(EngineResources, self).get_resource(resource_type, asset_id)

