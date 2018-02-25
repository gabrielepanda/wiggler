import wx

from wiggler.common.resourcemanager import ResourceManager
from wiggler.common.singleton import Singleton
from wiggler.core.resources.manager import CoreResources
from wiggler.gui.events import guievent, GUICommandHandler
from wiggler.gui.resources.sprites import Sprite
from wiggler.gui.resources.characters import Character
from wiggler.gui.resources.casts import Cast
from wiggler.gui.resources.images import Image
#from wiggler.gui.resources. import


class GUIResources(ResourceManager, wx.Control):
    __metaclass__ = Singleton

    def __init__(self, parent):
        #wx.Control.__init__(self, parent)
        super(GUIResources, self).__init__(parent)
        self.core_resources = CoreResources()
        self.parent = parent
        self._resources_map = {
            "image": Image,
            "sprite": Sprite,
#            "character": Character,
#            "cast": Cast,
        }
        command_map = {
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
        self.command_handler = GUICommandHandler(self, command_map)


    def get_resource(self, resource_type, asset_id, *args, **kwargs):
        print asset_id
        core_resource = self.core_resources.get_resource(resource_type, asset_id, *args, **kwargs)
        gui_resource = super(GUIResources, self).get_resource(resource_type, core_resource, *args, **kwargs)
        return gui_resource

    def change_background(self):
        dlg = dialogs.ChangeBackgroundDialog(self.parent)
        res = dlg.ShowModal()
        if res == wx.ID_OK:
            back_type = dlg.back_type.GetValue()
            back_spec = dlg.back_spec.GetValue()
            self.resources.change_default_background(back_type, back_spec)
        dlg.Destroy()


