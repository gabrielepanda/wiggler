
# Resouces are instantiated Assets
class Resource(object):
    def __init__(self, meta, **kwargs):
        self._meta = meta

        for extra, meta in kwargs.items():
            setattr(self, extra, meta)
        self._asset_path = None
        self.dependencies = None
        self._data_file_name = None

    def load_data(self):
        with open(self._data_filepath, "r") as data_file:
            data = data_file.read()

        return data

    def dump(self, library_name):
        self.global_catalog.replace


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
