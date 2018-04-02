import unittest
import pprint

from wiggler.core.assets import AssetCatalog


class BasicTest(unittest.TestCase):

    def setUp(self):
        self.assets = AssetCatalog()

    def runTest(self):
        assets_paths = self.assets._catalog.assets_paths
        with open("/tmp/log", 'w') as f:
            pprint.pprint(assets_paths, stream=f)
        self.assertIs(type(assets_paths), dict)
        for asset_id, asset_path in assets_paths.items():
            self.assertIs(type(asset_path), tuple)


if __name__ == '__main__':
    unittest.main()
