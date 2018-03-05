from wiggler.common.resourcemanager import ResourceManager
from wiggler.core.resources.projects import Project
from wiggler.core.resources.images import Image
from wiggler.core.resources.sprites import Sprite
from wiggler.core.resources.self_sufficiency import SelfSufficiency


class CoreResources(ResourceManager):

    def __init__(self, *args, **kwargs):
        super(CoreResources, self).__init__(*args, **kwargs)
        self._factory_map = {
            "image": Image,
            "sprite": Sprite,
            "project": Project,
        }
        self.project = None

    def new_project(self):
        self.project = self.new_resource('project')
