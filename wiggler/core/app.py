import os
import sys
import traceback
import wx

from wiggler.core.events import Events
from wiggler.core.project import Project
from wiggler.common import AssetInstance
from wiggler.ui.root import RootWindow

class Wiggler(wx.App):

    def __init__(self, filename=None):
        wx.App.__init__(self, filename)
        sys.excepthook = self.except_hook

    def OnInit(self):
        self.load_conf()
        self.resman = ResourcesManager(self.conf)
        self.engine = Engine(self.conf)
        self.ui_events = Events()
        self.project = Project(self.resman)
        frame = RootWindow(self.resman, self.events, self.project)
        frame.Show(True)
        self.SetTopWindow(frame)
        self.ui_events.send('projload')
        return True

    def load_conf(self):
        self.conf = default_conf
        # conf_filename = os.path.join(self.project_basepath, "conf.yaml")
        # try:
        #    with open(conf_filename) as conf_file:
        #        self.conf = yaml.load(conf_file.read())
        # except IOError:
        #    pass

    def except_hook(self, exc_type, exc_value, tb):
        """
        This method catches all errors raised and tries to handle
        """
        sys.__excepthook__(exc_type, exc_value, tb)
        code_handler = None
        if exc_type != SyntaxError:
            filename = traceback.extract_tb(tb)[-1][0]
            module_id = os.path.relpath(filename,
                                        start=self.resources.modules_dir)
            resource_type, module_filename = os.path.split(module_id)
            resource_name, __ = os.path.splitext(module_filename)
            instance = self.resources.instances[resource_type][resource_name]
            code_handler = instance.code_handler
            code_handler.handle_exception(exc_type, exc_value, tb)
        self.events.send('traceback', code_handler=code_handler,
                         exc_type=exc_type, exc_value=exc_value, tb=tb)


def main():
    app = Wiggler()
    app.MainLoop()
