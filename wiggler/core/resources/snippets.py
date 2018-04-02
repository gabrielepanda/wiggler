from wiggler.core.resources.base import Resource

class Snippet(Resource):

    def __init__(self, asset_id):
        super(Snippet, self).__init__('snippet', asset_id)


