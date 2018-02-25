from wiggler.common.resource import Resource

class Image(Resource):

    def __init__(self, asset_id, **kwargs):
        super(Image, self).__init__('image', asset_id)
