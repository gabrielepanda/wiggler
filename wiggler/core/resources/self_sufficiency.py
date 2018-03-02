from wiggler.common.resource import Resource

class SelfSufficiency(Resource):

    def __init__(self, asset_id):
        super(SelfSufficiency, self).__init__('self_sufficiency', asset_id)

        self.element = self._meta['element']
        buffers = self._meta['buffers']
        self.max_level = len(buffers)

        self.level = initial_level
        self.templates = {}
        self.update_templates_elements()
        self.buffers_lists = {}
        for template_name, template_def in self.resources.templates.items():
            template = self.resources.load_resource('templates', template_name)
            element = template_def['element']
            level = template_def['level']
            self.templates[element][level] = template
        self.buffers_lists['sprite'] = sprites_buffers_lists
        self.buffers_lists['controller'] = controller_buffers_lists


        self.buffers = meta['buffers']
        self.scripts_list = meta['scripts']
        buffername_script_pairs = zip(self.buffernames_list, self.scripts_list)
        self.scripts.update(buffername_script_pairs)
        for buffer_name in self.buffernames_list:
            if buffer_name not in self.scripts:
                self.scripts[buffer_name] = ""
        self.user_code = {}

    def update_templates_elements(self):
        self.templates = {}
        for element in self.elements[self.level]:
            self.templates[element] = {}

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
