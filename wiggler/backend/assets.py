class Catalog(CoreCatalog):


    def __init__(self):

        self.dependency_tree = []
        self.assets_by_library = {}
        self.assets_ids_by_tree = {}
        self.assets_ids_by_library = {}

        self.trees_by_library = {}

        self.assets_by_id_by_tree = {}
        self.type_by_id = {}
        self.ids_by_type = {}
        # trivial self.trees_by_id = {}
        self.trees_by_asset_id = {}
        self.assets_by_tree = {}
        # trivial self.assets_ids = [] catalog.keys

    def find_deps(self, resource_type, name):
        # hard deps
        # costumes -> sheets
        # animations -> sheets
        # soft_deps
        # character -> sprites
        # sprite -> costumes
        # sprite -> sounds
        # sprite -> animations
        hard_deps = set()
        soft_deps = set()
        if resource_type == 'sheets':
            abs_path = getattr(self, 'sheets')[name]['abs_path']
            sheet_file = os.path.basename(abs_path)
            for costume_name, costume_def in getattr(self, 'costumes').items():
                if costume_def['sheet'] == sheet_file:
                    hard_deps.update(set([('costumes', costume_name)]))
                    hard, soft = self.find_deps('costumes', costume_name)
                    hard_deps.update(hard)
                    soft_deps.update(soft)
            animations = getattr(self, 'animations').items()
            for animation_name, animation_def in animations:
                if animation_def['sheet'] == sheet_file:
                    hard_deps.update(set([('animations', animation_name)]))
                    hard, soft = self.find_deps('animations', animation_name)
                    hard_deps.update(hard)
                    soft_deps.update(soft)
        elif resource_type == 'costumes':
            for sprite_name, sprite_def in getattr(self, 'sprites').items():
                if name in sprite_def['costumes']:
                    soft_deps.update(set([('sprites', sprite_name)]))
                    __, soft = self.find_deps('sprites', sprite_name)
                    soft_deps.update(soft)
        elif resource_type == 'sounds':
            for sprite_name, sprite_def in getattr(self, 'sprites').items():
                if name in sprite_def['sounds']:
                    soft_deps.update(set([('sprites', name)]))
                    __, soft = self.find_deps('sprites', sprite_name)
                    soft_deps.update(soft)
        elif resource_type == 'animations':
            for sprite_name, sprite_def in getattr(self, 'sprites').items():
                if name in sprite_def['animations']:
                    soft_deps.update(set([('sprites', name)]))
                    __, soft = self.find_deps('sprites', sprite_name)
                    soft_deps.update(soft)
        elif resource_type == 'sprites':
            for character_name, character_def in \
                    getattr(self, 'characters').items():
                if name in character_def['sprites']:
                    soft_deps.update(set([('sprites', name)]))

        return list(hard_deps), list(soft_deps)


class AssetCatalog(object):
    __metaclass__ = Singleton


    def __init__(self):
        self.paths = Paths()
        schemas = os.listdir(self.paths.schemas_base)
        for asset_type_filename in schemas:
            asset_type_filepath = os.path.join(self.paths.schemas_base,
                                               asset_type_filename)
            try:
                with open(asset_type_filepath, "r") as asset_type_file:
                    asset_type_schema = yaml.safe_load(asset_type_file)
            except yaml.YAMLError:
                log.error("yaml parsing failed: %s" % (asset_type_filepath))
                continue
            self._asset_types[asset_type_schema['name']] = asset_type_schema
        ''' Add system library '''
        self.scan_library('system', self.paths.syslib_base)

        ''' Add user library '''
        if self.paths.userlib_base is not None:
            self.scan_library('user',self.paths.userlib_base)

    def change_project_library(self, project_file):
        #self.remove_project_library_assets()
        self.projectlibrary = ProjectLibrary(project_file)
        project_library_path = os.path.join(self.projectlibrary._render_dir,
                                        "assets")
        self.scan_library('project', project_library_path)

    def new_asset(self, asset_type):
        asset_meta = self._asset_types[asset_type]['schema']
        asset_meta['id'] = str(uuid.uuid4())
        tree_id = self._catalog.get_library_tree_ids('project')[0]
        project_tree = self._catalog.trees[tree_id]
        project_tree.save_asset(asset_type, asset_meta)

        return asset_meta['id']

    def clone_asset(self):
        """ copy assett from disk to disk, generating new id"""
        pass

    # saves asset from project resource
    def save_asset(self, target_library, asset_id):
        if target_library == 'project':
            self._catalog.save_asset( target_library )
        elif target_library == 'user':
            asset = self._catalog.clone_asset(asset_id)
            self._catalog.save_asset(target_library, asset )
        elif target_library == 'system' and self.system_mode:
            asset = self._catalog.clone_asset(asset_id)
            self._catalog.save_asset(target_library, asset )
        else:
            log("error not allowed")
            raise NotAllowedError

    def replace_asset(self, library, asset_id, asset_data=""):
        self.remove_asset(library, asset_id)
        self.save_asset(library, asset_meta, asset_data)

    def remove_asset(self, library, asset_id):
        if library == 'system' and not self.system_mode:
            log("error not allowed")
            raise NotAllowedError
        self._catalog.remove_asset(library)
    #def get_resource(self, library, res_type, name):
