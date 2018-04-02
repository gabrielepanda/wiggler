from wiggler.core.resources.base import Resource
from wiggler.gui.resources.templates import Template

class SelfSufficiency(Resource):

    def __init__(self, asset_id):
        super(SelfSufficiency, self).__init__('self_sufficiency', asset_id)

        self.levels = []
        levels = self._meta['levels']
        for level_meta in levels:
            level = {}
            template_list = level_meta['templates']
            for template_meta in template_list:
                for template_id, meta in template_meta:
                    template = Template(template_id)
                    template.set_section_options(meta['sections'])
                    level['templates'][template.element_name] = template
            self.levels.append(level)

    # GUI
    def increase_level(self):
        if self.level < self.max_level:
            self.level += 1

    def decrease_level(self):
        if self.level != 0:
            self.level -= 1

    def set_default_level(self, level):
        self.level = level

    def get_template(self, element, level=None):
        if level is None:
            level = self.level
        return self.templates[element][level]

    def get_buffers_list(self, element, level=None):
        if level is None:
            level = self.level
        return self.buffers_lists[element][level]

    def get_elements(self, level=None):
        if level is None:
            level = self.level
        return self.elements[level]
