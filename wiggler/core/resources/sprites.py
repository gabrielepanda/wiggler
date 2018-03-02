from wiggler.common.resource import Resource
from wiggler.core.resources.costumes import Wardrobe
from wiggler.core.resources.animations import Animation
from wiggler.core.resources.sounds import Sound
from wiggler.core.resources.code import Code


class Sprite(Resource):

    def __init__(self, asset_id):
        super(Sprite, self).__init__('sprite', asset_id)

        self.base_class = self._meta['base_class']
        costumes_list = self._meta['costumes']
        self.costumes = Wardrobe(costumes_list)
        self.animations = {}
        for asset_id in self._meta['animations']:
            self.animations[asset_id] = Animation(asset_id)
        self.sounds = {}
        for asset_id in self._meta['sounds']:
            self.sounds[asset_id] = Sound(asset_id)
        self.init_data = self._meta.get('init_data', {})


        # gui
        code_meta = self._meta['code']
        self.code = Code('sprite', code_meta)
