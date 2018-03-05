from wiggler.common.resource import Resource

project_asset_file_content = {
    "name": "project",
    "characters": [],
    "background" : {
        "type": "solid",
        "color": "255, 255, 255",
    },
}


class Project(Resource):

    def __init__(self, asset_id):
        super(Project, self).__init__('projects', asset_id)

        self.name = self._meta['name']
        self.characters = self._meta['characters']
        self.background = self._meta['background']

    def generate_new_meta(self):
        return project_asset_file_content

    def change_default_background(self, back_type, back_spec):
        background_def = {
            'type': back_type,
        }
        if back_type == "solid":
            background_def['color'] = back_spec
        elif back_type == "image":
            background_def['image_name'] = back_spec
        self.project_def['background'] = background_def

    #def get_resource_dependencies(self):
    #    return cast_id

    def add_character(self, character_id):
        if character_id not in self.characters:
            self.characters.append(character_id)

    def del_character(self, name):
        del self.characters[name]
        index = self.get_index(name)
        del self.indexes[index]

    def set_index(self, name, index):
        self.indexes[index] = self.characters[name]

    def get_index(self, name):
        for index, character in self.indexes.items():
            if character == self.characters[name]:
                return index

        return None

    def reload(self):
        self.characters = {}
        self.active_character = 0
        self.indexes = {}
        for name in self.resources.characters.keys():
            self.characters[name] = self.resources.load_resource(
                'characters', name)


    def get_character(self, name=None, index=None):
        if name is None and index is None:
            index = self.active_character
        if name is not None:
            return self.characters[name]
        if index is not None:
            try:
                return self.indexes[index]
            except KeyError:
                return None
