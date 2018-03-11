from wiggler.common.resource import Resource

class Character(Resource):

    def __init__(self, meta, **kwargs):
        super(Character, self).__init__(meta, **kwargs)

        self.name = self._meta['name']
        self.sprites = {}
        for asset_id in self._meta['sprites']:
            self.add_sprite(asset_id)

    def add_sprite(self, asset_id):
        sprite = self._manager.get_resource('sprite', asset_id)
        self.sprites[asset_id] = sprite

    def remove_sprite(self, sprite_name):
        self.builders_list.remove(sprite_name)
        del(self.builders[sprite_name])
        self.active_sprite = 0
        self.definition['sprites'].remove(sprite_name)
        self.definition['modified'] = True

    def build_sprites(self):
        for name, builder in self.builders.items():
            sprite = builder.build()
            if sprite is not None:
                self.add(builder.build())

    def destroy_sprites(self):
        self.empty()

    def get_sprite_builder(self, name=None, index=None):
        if index is None and name is None:
            index = self.active_sprite
        if name is not None:
            return self.builders[name]
        if index is not None:
            return self.builders[self.builders_list[index]]
