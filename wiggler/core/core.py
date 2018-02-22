from wiggler.core.resources.manager import ResourcesManager


class Core(object):

    def __init__(self):
        self.load_conf()
        self.resman = ResourcesManager(self.conf)
        self.project = ResourcesManager.new('project')

    def load_conf(self):
        self.conf = default_conf
        # conf_filename = os.path.join(self.project_basepath, "conf.yaml")
        # try:
        #    with open(conf_filename) as conf_file:
        #        self.conf = yaml.load(conf_file.read())
        # except IOError:
        #    pass
