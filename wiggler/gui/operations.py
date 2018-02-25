import wx

from wiggler.gui.resources.manager import GUIResources

class OperationIDs(object):

    def __init__(self):
        self.CHANGE_BACKGROUND = wx.NewId()
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

class Operations(object):

    def __init__(self, parent):
        self.resources = GUIResources(parent)


    def handler(self, event):
        print guiop.ADD_SPRITE
        print event.GetId()

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
