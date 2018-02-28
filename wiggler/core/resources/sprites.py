from wiggler.common.resource import Resource
from wiggler.core.resources.costumes import Costume
from wiggler.core.resources.animations import Animation
from wiggler.core.resources.sounds import Sound
from wiggler.core.resources.code import Code


class Wardrobe(object):

    def __init__(self, costumes_list):
        self.active = None
        self.costumes = {}
        self.costumes_list = []
        self.count = 0
        for costume_name in costume_names:
            self.add(costume_name)

        try:
            self.active = self.costumes[self.costumes_list[0]]
        except IndexError:
            pass

    def add(self, costume_name, position=None, make_active=False):
        costume = self.resources.load_resource('costumes', costume_name)
        self.costumes[costume_name] = costume
        if position is not None:
            self.costumes_list.insert(position, costume_name)
        else:
            self.costumes_list.append(costume_name)
        if make_active:
            self.set_active(costume_name)

    def remove(self, costume_name):
        self.costumes_list.remove(costume_name)
        if self.active == costume_name:
            self.active = None

    def set_active(self, costume_name):
        self.active = self.costumes[costume_name]
        return self.active.get()

    def get_active(self, rotate=0):
        return self.active.get(rotate=rotate)

class Sprite(Resource):

    def __init__(self, asset_id):
        super(Sprite, self).__init__('sprite', asset_id)

        self.base_class = definition['base_class']
        costumes_list = self._meta['costumes']
        self.costumes = Wardrobe(costumes_list)
        self.animations = {}
        for asset_id in self._meta['animations']:
            self.animations[asset_id] = Animation(asset_id)
        self.sounds = {}
        for asset_id in self._meta['sounds']:
            self.sounds[asset_id] = Sound(asset_id)
        self.init_data = self._meta.get('init_data', {})
        code = self._meta['code']
        self.code = Code(code)
