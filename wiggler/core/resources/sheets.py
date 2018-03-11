from wiggler.common.resource import Resource


class Sheet(Resource):

    def __init__(self, meta, **kwargs):
        super(Sheet, self).__init__(meta, **kwargs)
        color_key = self._meta['color_key']
        self.color_key = tuple(map(int,color_key.split(",")))
