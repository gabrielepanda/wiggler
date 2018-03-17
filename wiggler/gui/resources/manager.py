import wx

from wiggler.common.resourcemanager import ResourceManager
from wiggler.common.singleton import Singleton
from wiggler.core.resources.manager import CoreResources
from wiggler.gui.events import guievent, GUICommandHandler, EventQueue
from wiggler.gui.resources.sprites import Sprite
from wiggler.gui.resources.characters import Character
from wiggler.gui.resources.images import Image
from wiggler.gui.resources.projects import Project
from wiggler.gui.resources.costumes import Costume
from wiggler.gui.resources.sheets import Sheet
from wiggler.gui.resources.code import Code
from wiggler.gui.resources.templates import Template
#from wiggler.gui.resources. import

class OperationIDs(object):

    def __init__(self):
        self.CHANGE_BACKGROUND = wx.NewId()
        self.LOAD_PROJECT = wx.NewId()
        self.ADD_COSTUME = wx.NewId()
        self.DEL_COSTUME = wx.NewId()
        self.ADD_SHEET = wx.NewId()
        self.DEL_SHEET = wx.NewId()
        self.ADD_CHARACTER = wx.NewId()
        self.DEL_CHARACTER = wx.NewId()
        self.ADD_ANIMATION = wx.NewId()
        self.DEL_ANIMATION = wx.NewId()
        self.ADD_SPRITE = wx.NewId()
        self.DEL_SPRITE = wx.NewId()
        self.ADD_IMAGE = wx.NewId()
        self.DEL_IMAGE = wx.NewId()
        self.ADD_SOUND = wx.NewId()
        self.DEL_SOUND = wx.NewId()
        self.ADD_MUSIC = wx.NewId()
        self.DEL_MUSIC = wx.NewId()
        self.ADD_TEXT = wx.NewId()
        self.DEL_TEXT = wx.NewId()

guiop = OperationIDs()

class GUIResources(CoreResources, wx.Control):
    __metaclass__ = Singleton

    def __init__(self, parent):
        super(GUIResources, self).__init__(parent)
        self._factory_map = {
            "image": Image,
            "sprite": Sprite,
            "project": Project,
            "character": Character,
            "costume": Costume,
            "sheet": Sheet,
            "code": Code,
            "template": Template,
        }
        self.events = EventQueue()
        event_map = {
            guievent.GUI_READY:
                self.test_project,
#            guiop.PROJECT_LOADED:
#                self.load_all_resources
#            guievent.CHANGE_BACKGROUND:
#                self.resources.change_background,
#            guievent.ADD_COSTUME:
#                self.add_costume,
#            guievent.DEL_COSTUME:
#                self.del_costume,
#            guievent.ADD_SHEET:
#                self.add_sheet,
#            guievent.DEL_SHEET:
#                self.del_sheet,
#            guievent.ADD_IMAGE:
#                self.resources.null,
#            guievent.DEL_IMAGE:
#                self.resources.null,
#            guievent.ADD_CHARACTER:
#                self.add_character,
#            guievent.DEL_CHARACTER:
#                self.del_character,
#            guievent.ADD_ANIMATION:
#                self.resources.null,
#            guievent.DEL_ANIMATION:
#                self.resources.null,
#            guievent.ADD_SPRITE:
#                self.add_sprite,
#            guievent.DEL_SPRITE:
#                self.del_sprite,
        }
        self.command_handler = GUICommandHandler(self, event_map)


#    def get_resource(self, resource_type, asset_id, *args, **kwargs):
#        core_resource = self.core_resources.get_resource(resource_type, asset_id, *args, **kwargs)
#        gui_resource = super(GUIResources, self).get_resource(resource_type, core_resource, *args, **kwargs)
#        return gui_resource

    def set_root_frame(self, root_frame):
        self.root_frame = root_frame

    def test_project(self, event):
        self.new_project(event)
        character = self.get_resource('character', "6e5edb1f-6afa-437e-b3c1-a96cc5f5c7be")
        data = {}
        data['asset_id'] = "6e5edb1f-6afa-437e-b3c1-a96cc5f5c7be"
        self.events.broadcast(guievent.CHARACTER_RESOURCE_LOADED, **data)

    def new_project(self, event):
        super(GUIResources, self).new_project()

    def change_background(self):
        dlg = dialogs.ChangeBackgroundDialog(self.parent)
        res = dlg.ShowModal()
        if res == wx.ID_OK:
            back_type = dlg.back_type.GetValue()
            back_spec = dlg.back_spec.GetValue()
            self.resources.change_default_background(back_type, back_spec)
        dlg.Destroy()

    def event_handler(self, event):
        pass
        #print guiop.ADD_SPRITE
        #print event.GetId()

    def notice_dispatcher(self, event):
        menu_id = event.GetId()
        __, __, notice = self.menu_items[menu_id]
        self.events.send(notice)

    def button_sprite(self, event):
        pass


    def play(self, event):
        self.events.send('preplay')
        self.events.send('play')

    def stop(self, event):
        self.events.send('stop')

    def decss(self, event):
        self.resources.selfsuff.decrease_level()
        self.events.send('selfsuff_change')

    def incss(self, event):
        self.resources.selfsuff.increase_level()
        self.events.send('selfsuff_change')

    def add_costume_sprite(self, event):
        self.events.send('add_sprite_costume')

    def del_costume_sprite(self, event):
        self.events.send('del_sprite_costume')

    def add_sprite_character(self, event):
        self.events.send('add_char_sprite')

    def del_sprite_character(self, event):
        self.events.send('del_char_sprite')

    def add_character_project(self, event):
        self.events.send('add_char_proj')

    def del_character_project(self, event):
        self.events.send('del_char_proj')

    def load_project(self):
        self.events.broadcast('projload')

