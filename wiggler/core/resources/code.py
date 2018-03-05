from wiggler.common.resource import Resource
from wiggler.core.resources.snippets import Snippet

class Code(Resource):

    def __init__(self, asset_id):
        super(Code, self).__init__('code', asset_id)

        self.selfsuff_level = self._meta['selfsuff_level']
        self.sections = {}

        sections = self._meta['sections']
        for section_name, snippet_id in sections:
            snippet = Snippet(snippet_id)
            snippet_code = snippet.load_data()
            self.sections[section_name] = snippet_code


