import uuid
import os
import yaml
import pkg_resources

from wiggler.core.colorlog import log

class NotAllowedError(Exception):
    pass

class AssetInstance(object):
    def __init__(self, asset_id):
        self.instance_id = uuid.uuid4()
        catalog = AssetCatalog()
        raw_definition = catalog.get_by_id(asset_id)
        self._load_def(raw_definition)
        self._asset_path = None
        self.dependencies = None
        self._data_file_name = None
        catalog.add_instance(self.instance_id, self)

    def _load_def(self, raw_definition):
        self._meta = raw_definition['meta']
        if 'file' in raw_definition:
            self._data_file = self._meta['data_file']

class CatalogRecord(object):
# INMEMORY SQLDB
    def __init__(self, library, tree_id, asset_type, asset_meta):
        self.library = library
        self.tree_id = tree_id
        self.asset_type = asset_type
        self.asset_meta = asset_meta

class Catalog(object):
    def __init__(self):

        self.dependency_tree
        self.assets_paths = {}
        self.trees = {}

        # trivial self.trees_by_id = {}

        self.trees_by_asset_id = {}
        def get_trees_from_asset_id(self, asset_id):
            trees = set()
            for asset_record in self.assets_paths.values():
                trees.add(asset_record.tree_id)

            return trees

        self.assets_by_tree = {}
        def get_assets_by_tree_id(self, tree_id):
            assets = []
            for asset_record in self.assets_paths.values():
                if asset_record.tree_id == tree_id:
                    assets.append(asset_record.asset_meta)

            return assets

        self.assets_by_library = {}

        # trivial self.assets_ids = [] catalog.keys

        self.assets_ids_by_tree = {}
        self.assets_ids_by_library = {}

        self.trees_by_library = {}

        self.assets_by_id_by_tree = {}
        self.type_by_id = {}
        self.ids_by_type = {}

    def add_asset(self, library, tree_id, asset_type, asset_id, asset_meta):
        self.assets_paths[asset_id] = (library, tree_id, asset_type, asset_meta)

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


#class ResourceManager()
class AssetCatalog(object):
#    metaclass singleton

    def __init__(self, conf):
        self._catalog = Catalog()

        self._asset_types = yaml.safe_load_all(conf['basepath'] + 'types.yaml')
        ''' Add system library '''
        syslib_basepath = pkg_resources.resource_filename('wiggler',
                                                           "resources")
        self.scan_library('system', syslib_basepath)

        ''' Add user library '''
        try:
            userlib_basepath = conf['userlib_basepath']
            self.scan_library(userlib_basepath)
        except KeyError:
            log("No userlib specified in conf")
            pass

        self.libraries['project'] = None

    def scan_library(self, name, base_dir):
        self._catalog.add_library(name)
        gen = os.walk(base_dir)
        __ , __ , assets_conf_files = gen.next()
        gen.close()
        for assets_conf_file in assets_conf_files:
            asset_tree = AssetTree(self.base_dir, assets_conf_file)
            self.global_catalog.add_tree(asset_tree)

    # source library when saving is always project
    def save_asset(self, target_library, asset_id  ):
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

    # target library when loading is alwasy project
    def load_asset(self, source_library, asset_id):
        if source_library == 'system' or source_library == 'user':
            asset = self._catalog.clone_asset(asset_id)
            new_asset_id = self._catalog.save_asset("project", asset)
        self._catalog.load_asset("project", new_asset_id)

    def replace_asset(self, library, asset_id, asset_data=""):
        self.remove_asset(library, asset_id)
        self.save_asset(library, asset_meta, asset_data)

    def remove_asset(self, library, asset_id):
        if library == 'system' and not self.system_mode:
            log("error not allowed")
            raise NotAllowedError
        self._catalog.remove_asset(library)
    #def get_resource(self, library, res_type, name):

    def get_by_id(self, asset_id):
        source = self._catalog[asset_id]['source']
        lib = self.libraries[source]
        return lib.get_by_id(asset_id)

    def byid(self, asset_id):
        asset_def = self._catalog[asset_id]
        asset_type = asset_def['asset_type']
        asset_type_def = self._asset_types[asset_type]
        asset_def.update(asset_type_def)

        return asset_def

    def set_project_lib(self, base_dir):
        self.scan_library("project", base_dir)

    def get_all_assets(self):
        assets = []
        for asset_id, asset_path in self._catalog.assets_paths.iteritems():
            library, tree_id, asset_type, asset_id = asset_path.split('/')
            tree = self._catalog.trees[tree_id]
            asset = tree.load_asset(asset_id)
            assets.append(asset)

        return assets

class AssetTree():

    def __init__(self, library, types_conf, global_catalog, base_dir, conf_file):
        self.library = library
        self.global_catalog = global_catalog
        self.types_conf = types_conf
        self.conf_file = conf_file
        conf = yaml.safe_load_all(conf_file)
        self.tree_id = conf['id']
        self.base_dir = os.path.join(base_dir, conf['dir'])
        self.group = conf['group']
        self.locations = conf['locations']
        self.data_dirs = {}
        self.meta_files = {}

        self.assets = []
        self.assets_ids = []
        self.assets_by_id = {}
        self.type_by_id = {}
        self.ids_by_type = {}

        for asset_type, locations in self.locations.iteritems():
            meta_file_name = locations['meta_file']
            meta_file = os.path.join(self.base_dir, meta_file_name)
            self.meta_files[asset_type] = meta_file
            assets = yaml.safe_load_all(meta_file)

            if 'data_dir' in locations[asset_type]:
                data_dir_name = locations['data_dir']
                data_dir = os.path.join(self.base_dir, data_dir_name)
                self.data_dirs[asset_type] = data_dir

            for asset_meta in assets:
                asset_id = asset_meta['id']
                self.global_catalog.add_asset(library, self.tree_id, asset_type, asset_id, asset_meta)

    def load_asset(self, asset_id):
        asset_data = None
        asset_meta = self.global_catalog.get_assets_by_id(asset_id)
        if 'file' in asset_meta:
            asset_type = self.type_by_id[asset_id]
            data_dir = self.data_dirs[asset_type]
            data_file_name = os.path.join(data_dir, asset_meta['file'])
            with open(data_file_name, "r") as data_file:
                asset_data = data_file.read()

        return asset_meta, asset_data

    def write_conf_file(self):
        write_data = {}
        write_data['dir'] = self.base_dir
        write_data['group'] = self.group
        locations = {}
        for location in self.locations:
            locations[location] = {}
            locations[location]['meta_file'] = location['meta_file']
            if 'data_dir' in location:
                locations[location]['data_dir'] = location['data_dir']

        write_data['locations'] = {}
        yaml.dump(self.conf_file)

    def add_location(self, asset_type):
        self.locations[asset_type] = {}
        self.locations[asset_type]['meta_file'] = "%s.yaml" % asset_type
        if self.types_conf[asset_type]['meta_only'] == False:
            self.locations[asset_type]['data_dir'] = asset_type

        self.write_conf_file()

    def replace_asset(self, asset_type, asset_meta, asset_data=""):
        self.remove_asset(asset_meta['id'])
        self.add_asset(asset_type, asset_meta, asset_data=asset_data)

    def save_asset(self, asset_type, asset_meta, asset_data=""):
        assets = self.global_catalog.get_assets_from_tree_id(self.tree_id)
        if 'file' in asset_meta:
            file_name = asset_meta['file']
            data_file_name = os.path.join(self.data_dirs[asset_type], file_name)
            with open (data_file_name, "w") as data_file:
                data_file.write(asset_data)
        yaml.dump_all(assets, self.meta_files[asset_type])

    def remove_asset(self, asset_id):
        asset_type, asset_meta = self.global_catalog.get_asset_by_id(asset_id)
        self.global_catalog.remove_asset(asset_id)
        assets = self.global_catalog.get_assets_by_type(asset_type)
        if 'file' in asset_meta:
            file_name = asset_meta['file']
            data_file_name = os.path.join(self.data_dirs[asset_type], file_name)
            os.unlink(data_file_name)
        yaml.safe_dump_all(
            assets, self.meta_file[asset_type], indent=4,
            default_flow_style=False)

    def load_metadata_file(self, resource_meta_file_name):
        metadata = {}
        try:
            for resource in yaml.safe_load_all(resource_meta_file_name):
                try:
                    os.stat(resource['datafile'])
                except KeyError:
                    if resource_conf[resource_meta_file_name]['meta_only'] == False:
                        log("missing datafile definition")
                        continue
                    else:
                        pass
                except OSError:
                    log("data file not accessible")
                    continue
                try:
                    metadata[resource['id']] = resource
                except KeyError:
                    continue
        except yaml.ScannerError:
            log("error reading resource meta")
            pass
        return metadata
