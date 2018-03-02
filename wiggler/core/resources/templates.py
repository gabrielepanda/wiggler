import jinja2
import os

from wiggler.common.resource import Resource


class Template(Resource):

    def __init__(self, asset_id):
        super(Template, self).__init__('template', asset_id)

        path = os.path.dirname(self._data_filepath)
        filename = os.path.basename(self._data_filepath)
        self.env = jinja2.Environment(
            loader=jinja2.FileSystemLoader(path))
        self.template = self.env.get_template(filename)
        self.template_source = self.env.loader.get_source(
            self.env, filename)[0]
        self.section_offset = {}
        self.find_section_start()

    def find_section_start(self):
        tree = self.env.parse(self.template_source)
        for variable in tree.find_all(jinja2.nodes.Getitem):
            if variable.node.name == 'user_code':
                self.section_offset[variable.arg.value] = variable.lineno

    def render(self, user_code):
        return self.template.render(class_name="example", user_code=user_code)
