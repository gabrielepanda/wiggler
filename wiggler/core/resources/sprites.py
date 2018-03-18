from wiggler.common.resource import Resource


class Wardrobe(object):

    def __init__(self, costumes_ids, manager):
        self._manager = manager
        self.active = None
        self.costumes_ids = []
        self.costumes = {}
        for asset_id in costumes_ids:
            self.add_costume(asset_id)


        try:
            self.active = self.costumes[self.costumes_ids[0]]
        except IndexError:
            pass

    def add_costume(self, asset_id, position=None, make_active=False):
        costume = self._manager.get_resource('costume', asset_id)
        self.costumes[asset_id] = costume
        if position is not None:
            self.costumes_ids.insert(position, asset_id)
        else:
            self.costumes_ids.append(asset_id)
        if make_active:
            self.set_active(asset_id)

    def remove(self, asset_id):
        del(self.costumes[asset_id])
        self.costumes_ids.remove(asset_id)
        if self.active == asset_id:
            act_index = self.costumes_ids.index(asset_id)
            if act_index < len(self.costumes_ids - 1):
                act_index += 1
            else:
                act_index -= 1
            try:
                self.active == self.costumes_ids[act_index]
            except IndexError:
                self.active = None

    def set_active(self, asset_id):
        self.active = asset_id

    def get_active_costume(self, asset_id):
        return self.costumes[self.active]

    def get_active(self):
        return self.active


class Sprite(Resource):

    def __init__(self, meta, **kwargs):
        super(Sprite, self).__init__(meta, **kwargs)

        self.base_class = self._meta['base_class']
        costumes_list = self._meta['costumes']
        self.costumes = Wardrobe(costumes_list, self._manager)
        self.animations = {}
        for asset_id in self._meta['animations']:
            self.animations[asset_id] = self._manager.get_resource('animation', asset_id)
        self.sounds = {}
        for asset_id in self._meta['sounds']:
            self.sounds[asset_id] = self._manager.get_resource('sound',asset_id)
        self.init_data = self._meta.get('init_data', {})

