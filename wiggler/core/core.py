from wiggler.core.resources.manager import CoreResources


class CoreOperations(object):

    def __init__(self):
        #self.load_conf()
        #self.resman = CoreResources(self.conf)
        self.resources = CoreResources()
        self.project = self.resman.new_resource('project')

    def load_conf(self):
        pass
        #self.conf = default_conf
        # conf_filename = os.path.join(self.project_basepath, "conf.yaml")
        # try:
        #    with open(conf_filename) as conf_file:
        #        self.conf = yaml.load(conf_file.read())
        # except IOError:
        #    pass
