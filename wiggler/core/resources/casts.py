class Cast(object):

    def __init__(self, resources):
        self.resources = resources
        self.characters = {}
        self.indexes = {}
        self.active_character = 0
        self.reload()

