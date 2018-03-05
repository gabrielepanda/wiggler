import wx
import wx.py

import wiggler.gui.dialogs as dialogs

from wiggler.common.configuration import Configuration
from wiggler.gui.events import guievent, GUICommandHandler, EventQueue
from wiggler.gui.panes.characters import CharactersPane
from wiggler.gui.panes.costumes import CostumesPane
from wiggler.gui.panes.code import CodePane
from wiggler.gui.menubar import MenuBar
from wiggler.gui.panes.sprites import SpritesPane
from wiggler.gui.panes.stage import StagePane
from wiggler.gui.toolbar import ToolBar
from wiggler.gui.panes.traceback import TracebackPane


class RootWindow(wx.Frame):

    def __init__(self):
        wx.Frame.__init__(self, None, -1, "Menu")
        self.conf = Configuration()
        self.SetMinSize((100, 100))
        self.stage_resolution = tuple(map(int, self.conf.stage_resolution.split(",")))
        command_map = {
#            'projnew', 'projopen', 'projsave',
#            'projsaveas', 'testload', 'exit',
#            'modified', 'addcostume'])
#        if event.notice == 'projnew':
#            self.new_project()
#        elif event.notice == 'projopen':
#            self.open_project()
#        elif event.notice == 'projsave':
#            self.save_project()
#        elif event.notice == 'projsaveas':
#            self.save_project_as()
#        elif event.notice == 'testload':
#            self.project.load("tests/fixtures/test_project.wig")
#        elif event.notice == 'modified':
#            self.project.needs_save = True
#        elif event.notice == 'exit':
#            self.close()
#        elif event.notice == 'addcostume':
#            self.add_costume(event)
        }
        self.command_handler = GUICommandHandler(self, command_map)


    def setup(self):
        # Frame Elements
        self.menubar = MenuBar(self)
        self.toolbar = ToolBar(self)
        self.code_pane = CodePane(self)
        self.characters_pane = CharactersPane(self)
        #self.costumes_pane = CostumesPane(
        #    self, self.resources, self.events)
        #self.sprites_pane = SpritesPane(self, self.resources, self.events)
        #self.traceback = TracebackPane(self, self.resources, self.events)
        #self.stage_pane = StagePane(
        #    self, wx.ID_ANY, self.resources, self.events,
        #    size=self.stage_resolution)
        self.setup_basket_classes()
        self.setup_basket_members()

        self.statusbar = self.CreateStatusBar(2)
        #self.statusbar.SetStatusText("Self-Sufficiency Level: 0")
        self.SetMenuBar(self.menubar)

        self.widget_placement()
        self.Layout()


    def widget_placement(self):
        sizer = wx.GridBagSizer(hgap=1, vgap=1)
        #sizer.Add(self.stage_pane, (0, 0))
        sizer.Add(self.basket_classes, (0, 1), span=(1, 1), flag=wx.EXPAND)
        sizer.Add(self.basket_functions, (1, 1), span=(1, 1), flag=wx.EXPAND)
        #sizer.Add(self.costumes_pane, (0, 2), span=(2, 1), flag=wx.EXPAND)
        sizer.Add(self.code_pane, (0, 3), span=(2, 1), flag=wx.EXPAND)
        #sizer.Add(self.characters_pane, (1, 0), flag=wx.EXPAND)
        #sizer.Add(self.traceback, (2, 0), span=(1, 4), flag=wx.EXPAND)
        sizer.Fit(self)
        #sizer.AddGrowableCol(3)
        #sizer.AddGrowableRow(2)
        self.SetSizer(sizer)

    def setup_basket_members(self):
        self.basket_functions = wx.ListCtrl(
            self, wx.ID_ANY, style=wx.LC_REPORT)
        self.basket_functions.InsertColumn(0, "Available attributes",
                                           width=wx.LIST_AUTOSIZE_USEHEADER)

    def setup_basket_classes(self):
        self.basket_classes = wx.ListCtrl(
            self, wx.ID_ANY, style=wx.LC_REPORT)
        self.basket_classes.InsertColumn(0, "Available Classes",
                                         width=wx.LIST_AUTOSIZE_USEHEADER)
        self.basket_classes.InsertStringItem(0, "MovingSprite")
        self.basket_classes.InsertStringItem(1, "StaticSprite")

    def load(self, event):
        # FIXME get filenam from event
        filename = None
        self.project.load(filename)

    def close(self):
        # if self.project.needs_save:
        if True:
            proceed = dialogs.unsaved_warning(self)
            if not proceed:
                return
        self.resources.cleanup()
        self.Close(True)

    def open_project(self):
        # if self.project.needs_save:
        if True:
            proceed = dialogs.unsaved_warning(self)
            if not proceed:
                return
        filename = dialogs.open_project(self)
        if filename is not None:
            self.project.load(filename)

    def save_project(self):
        if self.project.abspath is None:
            self.save_project_as()
        else:
            self.project.save(self.project.abspath)

    def save_project_as(self):
        filename = dialogs.save_project(self)
        if filename is not None:
            self.project.save(filename)

    def new_project(self):
        # if self.project.needs_save:
        if True:
            proceed = dialogs.unsaved_warning(self)
            if not proceed:
                return
        self.project.new()

    def add_costume(self, event):
        self.toolbar.add_costume(event)
