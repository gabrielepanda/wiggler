import os
import sys
import traceback
import wx

from wiggler.common.configuration import Configuration
from wiggler.gui.events import guievent, EventQueue
from wiggler.gui.resources.manager import GUIResources
from wiggler.gui.root import RootWindow

class Wiggler(wx.App):

    def __init__(self, filename=None):
        wx.App.__init__(self, filename)
        #sys.excepthook = self.except_hook

    def OnInit(self):
        #self.engine = Engine(self.conf)
        self.conf = Configuration()
        self.events = EventQueue()
        root_frame = RootWindow()
        self.resources = GUIResources(root_frame)
        root_frame.setup()
        root_frame.Show(True)
        self.SetTopWindow(root_frame)
        self.events.broadcast(guievent.GUI_READY)
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
