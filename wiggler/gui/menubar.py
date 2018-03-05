""" this class create and populate the menu toolbar
References:
    https://wiki.wxpython.org/wxPython%20Style%20Guide
    https://wxpython.org/Phoenix/docs/html/wx.Menu.html#wx.Menu
    https://wxpython.org/Phoenix/docs/html/wx.MenuBar.html#wx.MenuBar

"""
import gettext
import wx

from collections import OrderedDict
from wiggler.gui.resources.manager import guiop, GUIResources

gettext.install("wiggler")

menu_items = {
    wx.ID_NEW: ("&New project", "Create a new project", "projnew"),
    wx.ID_OPEN: ("&Load project", "Load a project from disk",
                    "projopen"),
    wx.ID_SAVE: ("&Save project", "Save a project to disk",
                    "projsave"),
    wx.ID_SAVEAS: ("&Duplicate project",
                    "Save a project to disk changing its name",
                    'projsaveas'),
    wx.ID_EXECUTE: ("&Examples", "Load one of the example projects",
                    'testload'),
    wx.ID_EXIT: ("E&xit", "Close Wiggler", "exit"),
    wx.ID_UNDO: ("&Undo", "Undo the last action", 'undo'),
    wx.ID_REDO: ("&Redo", "Redo the last action", 'redo'),
    wx.ID_COPY: ("&Copy", "Copy selected text to the clipboard",
                    'copy'),
    wx.ID_CUT: ("&Cut", "Move selected text to the clipboard", 'cut'),
    wx.ID_PASTE: ("&Paste", "Paste text from the clipboard", 'paste'),
    wx.ID_PREFERENCES: ("Pr&eferences", "Open the preference dialog",
                        'preferences'),
    wx.ID_SEPARATOR: (),
    guiop.ADD_COSTUME: ('Add costume',
                        'Add a new costume to project library',
                        'add_costume'),
    guiop.DEL_COSTUME: ('Remove costume',
                        'Remove costume from project library',
                        'del_costume'),
    guiop.ADD_SHEET: ('Add sprite sheet',
                    'Add a new sheet to project library',
                    'add_sheet'),
    guiop.DEL_SHEET: ('Remove sprite sheet',
                    'Remove sheet from project library',
                    'del_sheet'),
    guiop.ADD_CHARACTER: ('Add character',
                        'Add a new character to project library',
                        'add_character'),
    guiop.DEL_CHARACTER: ('Remove character',
                        'Remove character from project library',
                        'del_character'),
    guiop.ADD_ANIMATION: ('Add animation',
                        'Add a new animation to project library',
                        'add_animation'),
    guiop.DEL_ANIMATION: ('Remove animation',
                        'Remove animation from project library',
                        'del_animation'),
    guiop.ADD_SPRITE: ('Add sprite',
                    'Add a new sprite to project library',
                    'add_sprite'),
    guiop.DEL_SPRITE: ('Remove sprite',
                    'Remove sprite from project library',
                    'del_sprite'),
    guiop.ADD_IMAGE: ('Add image',
                    'Add a new image to project library',
                    'add_image'),
    guiop.DEL_IMAGE: ('Remove image',
                    'Remove image from project library',
                    'del_image'),
    guiop.ADD_SOUND: ('Add sound',
                    'Add a new sound to project library',
                    'add_sound'),
    guiop.DEL_SOUND: ('Remove sound',
                    'Remove sound from project library',
                    'del_sound'),
    guiop.ADD_MUSIC: ('Add music',
                    'Add a new music to project library',
                    'add_music'),
    guiop.DEL_MUSIC: ('Remove music',
                    'Remove music from project library',
                    'del_music'),
    guiop.ADD_TEXT: ('Add text',
                    'Add a new text box to project library',
                    'add_text'),
    guiop.DEL_TEXT: ('Remove text',
                    'Remove text box from project library',
                    'del_text'),
    guiop.CHANGE_BACKGROUND: ('Change default background',
                            'Change default background for the project',
                            'change_background'),
}

class MenuBar(wx.MenuBar):

    def __init__(self, parent):
        self.parent = parent
        self.resources = GUIResources()
        """Create a menu bar facade to simplify toolbar creation

           Arguments:
               parent - a wx.Frame object containing the menu bar
        """
        wx.MenuBar.__init__(self, wx.ID_ANY)
        self.menu_items = menu_items
        self.menu = OrderedDict()
        self.menu["&File"] = [
            wx.ID_NEW,
            wx.ID_OPEN,
            wx.ID_SAVE,
            wx.ID_SAVEAS,
            wx.ID_SEPARATOR,
            wx.ID_EXECUTE,
            wx.ID_SEPARATOR,
            wx.ID_EXIT,
        ]
        self.menu["&Edit"] = [
            wx.ID_UNDO,
            wx.ID_REDO,
            wx.ID_SEPARATOR,
            wx.ID_COPY,
            wx.ID_CUT,
            wx.ID_PASTE,
            wx.ID_SEPARATOR,
            wx.ID_PREFERENCES,
        ]
        self.menu['&Resources'] = [
            guiop.CHANGE_BACKGROUND,
            wx.ID_SEPARATOR,
            guiop.ADD_SHEET,
            guiop.DEL_SHEET,
            wx.ID_SEPARATOR,
            guiop.ADD_COSTUME,
            guiop.DEL_COSTUME,
            wx.ID_SEPARATOR,
            guiop.ADD_CHARACTER,
            guiop.DEL_CHARACTER,
            wx.ID_SEPARATOR,
            guiop.ADD_SPRITE,
            guiop.DEL_SPRITE,
            wx.ID_SEPARATOR,
            guiop.ADD_IMAGE,
            guiop.DEL_IMAGE,
            wx.ID_SEPARATOR,
            guiop.ADD_ANIMATION,
            guiop.DEL_ANIMATION,
            wx.ID_SEPARATOR,
            guiop.ADD_SOUND,
            guiop.DEL_SOUND,
            wx.ID_SEPARATOR,
            guiop.ADD_MUSIC,
            guiop.DEL_MUSIC,
            wx.ID_SEPARATOR,
            guiop.ADD_TEXT,
            guiop.DEL_TEXT,
        ]
        self.menu["&Appearance"] = []

        for name, item_list in self.menu.items():
            current = wx.Menu()
            for menu_id in item_list:
                if menu_id == wx.ID_SEPARATOR:
                    current.AppendSeparator()
                else:
                    title, description, __ = self.menu_items[menu_id]
                    current.Append(menu_id, _(title), _(description))
            self.Append(current, name)


        self.parent.Bind(wx.EVT_MENU, self.resources.event_handler)

