import wx

from wiggler.gui.events import GUICommandHandler
from wiggler.gui.operations import guiop, Operations
from wiggler.gui.resources.manager import GUIResources

class ToolBar(object):

    def __init__(self, parent):
        self.parent = parent
        self.width = 30
        self.height = 30
        self.resources = GUIResources(parent)
        self.tools = parent.CreateToolBar()
        buttons = [
            ('f3006821-3470-452f-967b-8a0cd9b88039',
             "Add Sprite to project library",
             guiop.ADD_SPRITE)
#            ('play', 'Play'),
#            ('stop', 'Stop'),
#            ('incss', 'Increase Sufficiency Level', self.incss),
#            ('decss', 'Decrease Sufficiency Level', self.decss),
#            ('costume', 'Add costume to sprite'),
#            ('nocostume', 'Remove costume from sprite'),
#            ('sprite', 'Add sprite to character',
#                self.resources['character'].add_sprite),
#            ('nosprite', 'Remove sprite from character',
#                self.resources['character'].del_sprite),
#            ('character', 'Add character to project',
#                self.resources['project'].add_character),
#            ('nocharacter', 'Remove character from project',
#                self.resources['project'].del_character),
        ]

        for button in buttons:
            image_asset_id, label_text, guiop_id = button
            image = self.resources.get_resource('image', image_asset_id)
            bitmap = image.get_bitmap(scale=(self.width, self.height))
            tool = self.tools.AddLabelTool(guiop_id, label_text, bitmap)


        self.tools.Realize()
