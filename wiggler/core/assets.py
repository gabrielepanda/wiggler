import os
import uuid
import yaml
import pprint

from wiggler.core.colorlog import log
from wiggler.core.singleton import Singleton


class NotAllowedError(Exception):
    pass


class CatalogRecord(object):
# INMEMORY SQLDB
    def __init__(self, library, tree_id, asset_type, asset_meta):
        self.library = library
        self.tree_id = tree_id
        self.asset_type = asset_type
        self.asset_meta = asset_meta

class Catalog(object):

    def __init__(self):

        self.assets_paths = {}
        self.trees = {}
        self.libraries = {}


    def get_library_tree_ids(self, library_name):
        tree_ids = self.libraries[library_name]['trees']
        return tree_ids

    def get_trees_from_asset_id(self, asset_id):
        trees = set()
        for asset_record in self.assets_paths.values():
            trees.add(asset_record.tree_id)

        return trees

    def get_assets_by_tree_id(self, tree_id):
        assets = []
        for asset_record in self.assets_paths.values():
            if asset_record.tree_id == tree_id:
                assets.append(asset_record.asset_meta)

        return assets

    def add_asset(self, library, tree_id, asset_type, asset_meta):
        asset_id = asset_meta['id']
        self.assets_paths[asset_id] = (library, tree_id, asset_type, asset_meta)


#class ResourceManager()
class AssetCatalog(object):
    __metaclass__ = Singleton

    def __init__(self, scan_systemlib=True, scan_userlib=True):
        self._catalog = Catalog()
        self._asset_types = {}

    def scan_library(self, library_name, base_dir):
        #self._catalog.add_library(name)
        self._catalog.libraries[library_name] = {}
        self._catalog.libraries[library_name]['trees'] = []
        gen = os.walk(base_dir)
        assets_conf_files = []
        try:
            __ , __ , assets_conf_files = gen.next()
        except StopIteration:
            pass
        gen.close()
        for assets_conf_filename in assets_conf_files:
            assets_conf_filepath = os.path.join(base_dir,
                                                assets_conf_filename)
            asset_tree = AssetTree(library_name, self._asset_types,
                                   self._catalog, base_dir,
                                   assets_conf_filepath)
            self._catalog.trees[asset_tree.tree_id] = asset_tree


    # target library when loading is alwasy project
    def load_asset(self, source_library, asset_id):
        if source_library == 'system' or source_library == 'user':
            asset = self._catalog.clone_asset(asset_id)
            new_asset_id = self._catalog.save_asset("project", asset)
        self._catalog.load_asset("project", new_asset_id)


    def get_asset_by_id(self, asset_id):
        __, __, __, meta = self._catalog.assets_paths[asset_id]
        return meta

    def get_datadir_by_id(self, asset_id):
        __, tree_id, asset_type, __ = self._catalog.assets_paths[asset_id]
        tree = self._catalog.trees[tree_id]
        return tree.get_data_dir(asset_type)


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

class AssetTree(object):

    def __init__(self, library, types_conf, global_catalog,
                 base_dir, conf_filename):
        self.library = library
        self.global_catalog = global_catalog
        self.types_conf = types_conf
        self.conf_filename = conf_filename
        with open(conf_filename, "r") as conf_file:
            conf = yaml.safe_load(conf_file)
        self.tree_id = conf['id']
        self.global_catalog.libraries[library]['trees'].append(self.tree_id)
        self.base_dir = os.path.join(base_dir, conf['assets_dir'])
        self.assets_type = conf['assets_type']
        self.assets_locations = conf['assets']
        self.data_dirs = {}
        self.meta_files = {}

        self.assets = []
        self.assets_ids = []
        self.assets_by_id = {}
        self.type_by_id = {}
        self.ids_by_type = {}


        for asset_type, location in self.assets_locations.items():
            self.set_meta_files(asset_type)
            with open(self.meta_files[asset_type], "r") as meta_file:
                assets = list(yaml.safe_load_all(meta_file))

            if 'data_dir' in location:
                data_dir_name = location['data_dir']
                data_dir = os.path.join(self.base_dir, data_dir_name)
                self.data_dirs[asset_type] = data_dir

            for asset_meta in assets:
                asset_id = asset_meta['id']
                self.global_catalog.add_asset(library, self.tree_id, asset_type, asset_meta)

    def get_data_dir(self, asset_type):
        data_dir =  self.assets_locations[asset_type]["data_dir"]
        return os.path.join(self.base_dir, data_dir)

    def set_meta_files(self, asset_type):
        location = self.assets_locations[asset_type]
        meta_file_name = location['meta_file']
        meta_filepath = os.path.join(self.base_dir, meta_file_name)
        self.meta_files[asset_type] = meta_filepath


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
        write_data['id'] = self.tree_id
        write_data['assets_dir'] = os.path.basename(self.base_dir)
        write_data['assets_priority'] = self.assets_type
        write_data['assets_type'] = self.assets_type
        write_data['assets'] = self.assets_locations
        with open(self.conf_filename, "w") as conf_file:
            yaml.dump(write_data, conf_file)

    def add_location(self, asset_type):
        self.assets_locations[asset_type] = {}
        self.assets_locations[asset_type]['meta_file'] = "%s.yaml" % asset_type
        if self.types_conf[asset_type]['meta_only'] == False:
            self.assets_locations[asset_type]['data_dir'] = asset_type

        self.write_conf_file()

    def replace_asset(self, asset_type, asset_meta, asset_data=""):
        self.remove_asset(asset_meta['id'])
        self.add_asset(asset_type, asset_meta, asset_data=asset_data)

    def save_asset(self, asset_type, asset_meta, asset_data=""):
        if asset_type not in self.assets_locations:
            self.add_location(asset_type)
        asset_meta_filename = self.assets_locations[asset_type]['meta_file']
        asset_meta_filepath = os.path.join(self.base_dir, asset_meta_filename)
        try:
            os.stat(asset_meta_filepath)
            assets = self.global_catalog.get_assets_from_tree_id(self.tree_id)
        except OSError:
            assets = []
            self.set_meta_files(asset_type)


        if 'data_file' in asset_meta:
            file_name = asset_meta['data_file']
            data_file_name = os.path.join(self.data_dirs[asset_type], file_name)
            with open (data_file_name, "w") as data_file:
                data_file.write(asset_data)

        assets.append(asset_meta)

        with open(self.meta_files[asset_type], "w") as meta_file:
            yaml.dump_all(assets, meta_file, default_flow_style=False)
        self.global_catalog.add_asset(self.library, self.tree_id, asset_type,
                                      asset_meta)

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
