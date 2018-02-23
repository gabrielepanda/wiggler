import wx

from wiggler.gui.events import Events
from wiggler.gui.resources.manager import GUIResources


class GUIControl(wx.Control):

    def __init__(self, parent):
        wx.Control.__init__(self, parent)
        self.parent = parent
        self.resources = GUIResources()
        self.events = Events()
        self.events.subscribe(self, ['add_costume', 'del_costume',
                                     'add_character', 'del_character',
                                     'add_sheet', 'del_sheet',
                                     'add_image', 'del_image',
                                     'add_sprite', 'del_sprite',
                                     'add_animation', 'del_animation',
                                     'change_background'])
        self.Bind(self.events.EVT_NOTICE, self.resources.notice_handler)

