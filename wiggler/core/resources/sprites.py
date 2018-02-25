from wiggler.common.resource import Resource

class Sprite(Resource):

    def __init__(self, asset_id):
        super(Sprite, self).__init__('sprite', asset_id)
