from wiggler.common.resourcemanager import ResourceManager
from wiggler.core.resources.casts import Cast
from wiggler.core.resources.projects import Project
from wiggler.core.resources.self_sufficiency import SelfSufficiency


class CoreResources(ResourceManager):

    def __init__(self):
        super(CoreResources, self).__init__()
        self.factory_map['project'] = Project

