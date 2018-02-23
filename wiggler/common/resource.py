import uuid
from wiggler.common.assets import AssetCatalog

# Resouces are instantiated Assets
class Resource(object):
    def __init__(self, asset_id, asset_meta=None):
        self.instance_id = str(uuid.uuid4())
        self.global_catalog = AssetCatalog()
        # if asset_id is 0 this means the resource is new
        # and doesn't need to be loaded
        if asset_id == 0:
            meta = self.generate_new_meta()
            asset_id =  str(uuid.uuid4())
            meta['id'] = asset_id
            self.global_catalog.create_asset(self.resource_type, meta)
        self._meta = self.global_catalog.get_asset_by_id(asset_id)
        if 'data_file' in self._meta:
            self._data_file = self._meta['data_file']
        self.asset_id = asset_id
        self._asset_path = None
        self.dependencies = None
        self._data_file_name = None

    def clone_and_write_instance(self, library):
        ''' will save modifications to the instance on
        the asset then change own asset_id to that'''
        if library == 'project':
            if 'id' in self.catalog.projects:
                #just save
                pass
            else:
                # This is a new resource
                # save and switch
                pass
        elif library == 'user':
            pass
        self.catalog.save_asset()
