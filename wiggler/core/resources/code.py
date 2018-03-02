from wiggler.common.resource import Resource
from wiggler.core.resources.snippets import Snippet

class Code(Resource):

    def __init__(self, asset_id):
        super(Code, self).__init__('code', asset_id)
        self.user_code = {}

        self.sections = self._meta['sections']
        for section_name, snippet_id in self.sections:
            snippet = Snippet(snippet_id)
            snippet_code = snippet.load_data()
            self.user_code[section_name] = snippet_code


