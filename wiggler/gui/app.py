import os
import sys
import traceback
import wx

from wiggler.gui.events import Events
from wiggler.gui.resources.manager import ResourcesManager
from wiggler.gui.root import RootWindow
from wiggler.core.core import Core

class Wiggler(wx.App):

    def __init__(self, filename=None):
        wx.App.__init__(self, filename)
        sys.excepthook = self.except_hook

    def OnInit(self):
        self.core = Core()
        self.resman = ResourcesManager()
        #self.engine = Engine(self.conf)
        self.events = Events()
        frame = RootWindow(self.core, self.resman, self.events, self.project)
        frame.Show(True)
        self.SetTopWindow(frame)
        self.events.send('projload')
        return True

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
