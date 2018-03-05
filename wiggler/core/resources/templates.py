import jinja2
import os

from wiggler.common.resource import Resource


class Template(Resource):

    def __init__(self, asset_id):
        super(Template, self).__init__('template', asset_id)

        self.element_name = self._meta['element']
        path = os.path.dirname(self._data_filepath)
        filename = os.path.basename(self._data_filepath)
        self.env = jinja2.Environment(
            loader=jinja2.FileSystemLoader(path))
        self.template = self.env.get_template(filename)
        self.template_source = self.env.loader.get_source(
            self.env, filename)[0]
        self.sections = {}
        self.find_sections()

    def set_section_options(self, sections_options):
        for section_name, section_options in sections_options:
            try:
                self.sections[section_name]['options'] = section_options
            except KeyError:
                pass

    def find_sections(self):
        tree = self.env.parse(self.template_source)
        for variable in tree.find_all(jinja2.nodes.Getitem):
            if variable.node.name == 'user_code':
                section_name = variable.arg.value
                self.sections[section_name] = {}
                self.sections[section_name]['start_offset'] = variable.lineno

    def render(self, user_code):
        return self.template.render(class_name="example", user_code=user_code)
