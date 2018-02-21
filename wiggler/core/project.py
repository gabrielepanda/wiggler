
new_project_def = {
    'name': "untitled",
    'characters': {},
    'background': {
        'type': 'solid',
        'color': "255, 255, 255",
    },
}

class Project(object):

    def __init__(self, resman, filename=None):
        self.resman = resman
        self.needs_save = False
        self.code_status = "undef"
        self.active_sprite = None
        self.stage_background = None
        self.modules_dir = None
        self.name = None
        self.abspath = None
        self.filename = None

        if filename is None:
            self.new()
        else:
            self.load(filename=filename)


    def change_default_background(self, back_type, back_spec):
        background_def = {
            'type': back_type,
        }
        if back_type == "solid":
            background_def['color'] = back_spec
        elif back_type == "image":
            background_def['image_name'] = back_spec
        self.project_def['background'] = background_def

    def new(self):
        return new_project_def

    def load_project(self, filename):
        if self.projectres is not None:
            self.projectres.cleanup()

    def load(self, filename):
        project_def = self.load_project(filename)
        self.abspath = filename
        self.load_def(project_def)

    def load_def(self, project_def):
        self.name = project_def['name']
        self.stage_background = project_def['background']
        self.characters = project_def['characters']

    def save(self, filename):
        if self.projectres is not None:
            for resource_type in self.types:
                self.save_resources(resource_type, save_all=True)
            self.projectres.save(filename)

    def load_resource
        resource_def =
        self.elements[resource_type][resource_name] = instance


    def cleanup(self):
        shutil.rmtree(self.modules_dir)

