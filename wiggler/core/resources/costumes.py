from wiggler.core.resources.base import Resource

class Costume(Resource):

    def __init__(self, meta, **kwargs):
        super(Costume, self).__init__(meta, **kwargs)
        self.name= self._meta['name']
        sheet_id = self._meta['sheet_id']
        self.sheet = self._manager.get_resource('sheet', sheet_id)
        rect = self._meta['rect']
        self.rect = tuple(map(int,rect.split(",")))
