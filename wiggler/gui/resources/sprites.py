import wx

from wiggler.core.resources.sprites import Sprite as CoreSprite

class Sprite(CoreSprite):

    def __init__(self, meta, **kwargs):
        super(Sprite, self).__init__(meta, **kwargs)
        # gui
        code_id = self._meta['code']
        self.code = self._manager.get_resource('code', code_id)

    def add(self):
        pass

    def add_costume(self):
        pass

    def del_costume(self):
        pass

class SelectSpriteCostume(wx.ListCtrl):

    def __init__(self, parent, id, resources, sprite_name, single_sel=False):
        if single_sel is True:
            wx.ListCtrl.__init__(self, parent, id, style=wx.LC_REPORT |
                                 wx.LC_SINGLE_SEL)
        else:
            wx.ListCtrl.__init__(self, parent, id, style=wx.LC_REPORT)

        self.resources = resources
        self.InsertColumn(0, 'Costume name', width=wx.LIST_AUTOSIZE_USEHEADER)
        for sheetname in self.resources.sprites[sprite_name]['costumes']:
            num_items = self.GetItemCount()
            self.InsertStringItem(num_items, sheetname)

class SelectSprite(wx.ListCtrl):

    def __init__(self, parent, id, resources, single_sel=True):
        if single_sel is True:
            wx.ListCtrl.__init__(self, parent, id, style=wx.LC_REPORT |
                                 wx.LC_SINGLE_SEL)
        else:
            wx.ListCtrl.__init__(self, parent, id, style=wx.LC_REPORT)

        self.resources = resources
        self.InsertColumn(0, 'Sprite name', width=wx.LIST_AUTOSIZE_USEHEADER)
        for sheetname in self.resources.sprites.keys():
            num_items = self.GetItemCount()
            self.InsertStringItem(num_items, sheetname)



def add_sprite(self):
    # dialog with definition, select from existing costumes,
    # animations, sounds...
    # or add empty
    dia = dialogs.AddSpriteDialog(None, -1, "Add a new sprite",
                                    self.resources)
    result = dia.ShowModal()
    if result == wx.ID_OK:
        self.settings = dia.GetSettings()
        try:
            self.resources.add_resource('sprites', self.settings['name'],
                                        {'name': self.settings['name'],
                                            'base_class': self.settings
                                            ['base_class'],
                                            'costumes': self.settings
                                            ['costumes'],
                                            'animations': [],
                                            'sounds': [],
                                            'self_sufficiency': 0,
                                            'user_code': {'__init__': ''}})
        except ValueError as e:
            wx.MessageBox(str(e), "Error",
                            wx.OK | wx.ICON_INFORMATION)

    dia.Destroy()
    return True

def del_sprite(self):
    # LISTCTRK with name + sprite definition
    dia = dialogs.DelSpriteDialog(None, -1, "Delete a sprite",
                                    self.resources)
    result = dia.ShowModal()
    if result == wx.ID_OK:
        self.settings = dia.GetSettings()
        for x in self.resources.find_deps('sprites',
                                            self.settings['sprite']):
            for elem in x:
                try:
                    self.resources.remove_resource(elem[0], elem[1])
                except Exception as e:
                    wx.MessageBox(str(e), "Error", wx.OK |
                                    wx.ICON_INFORMATION)

        try:
            self.resources.remove_resource('sprites',
                                            self.settings['sprite'])
        except Exception as e:
            wx.MessageBox(str(e), "Error", wx.OK | wx.ICON_INFORMATION)

    dia.Destroy()
    return True

class AddCostumeToSpriteDialog(wx.Dialog):

    def __init__(self, parent, id, title, resources):
        wx.Dialog.__init__(self, parent, id, title, size=(300, 300))
        self.settings = {}
        self.resources = resources

        boxglobal = wx.BoxSizer(wx.VERTICAL)

        boxup = wx.BoxSizer(wx.VERTICAL)
        self.lc = SelectCostume(self, -1, self.resources)
        boxup.Add(wx.StaticText(self, 0,
                                'Select a costume to add to sprite:'),
                  0, wx.ALL, 5)
        boxup.Add(self.lc, 1, wx.ALL | wx.EXPAND, 5)

        boxdown = wx.BoxSizer(wx.HORIZONTAL)
        self.button_ok = wx.Button(self, 1, 'Ok')
        self.button_cancel = wx.Button(self, 2, 'Cancel')
        self.button_ok.Bind(wx.EVT_BUTTON, self.onOk)
        self.button_cancel.Bind(wx.EVT_BUTTON, self.onCancel)
        boxdown.Add(self.button_ok, -1, wx.ALL | wx.ALIGN_BOTTOM, 5)
        boxdown.Add(self.button_cancel, -1, wx.ALL | wx.ALIGN_BOTTOM, 5)

        boxglobal.Add(boxup, 5, wx.EXPAND, 5)
        boxglobal.Add(boxdown, 1, wx.EXPAND, 5)
        self.SetSizer(boxglobal)

    def onCancel(self, e):
        self.EndModal(wx.ID_CANCEL)

    def onOk(self, e):
        sel = self.lc.GetNextSelected(-1)
        if sel == -1:
            wx.MessageBox("Select a costume", "Error",
                          wx.OK | wx.ICON_INFORMATION)
        else:
            out = self.lc.GetItemText(sel, 0)
            out2 = self.resources.costumes[out]
            self.settings['costume'] = out2['name']
            self.EndModal(wx.ID_OK)

    def GetSettings(self):
        return self.settings


class DelCostumeFromSpriteDialog(wx.Dialog):

    def __init__(self, parent, id, title, resources, sprite_name):
        wx.Dialog.__init__(self, parent, id, title, size=(300, 300))
        self.settings = {}
        self.resources = resources

        boxglobal = wx.BoxSizer(wx.VERTICAL)

        boxup = wx.BoxSizer(wx.VERTICAL)
        self.lc = SelectSpriteCostume(self, -1, self.resources, sprite_name)
        boxup.Add(wx.StaticText(self, 0,
                                'Select a costume to remove from sprite:'),
                  0, wx.ALL, 5)
        boxup.Add(self.lc, 1, wx.ALL | wx.EXPAND, 5)

        boxdown = wx.BoxSizer(wx.HORIZONTAL)
        self.button_ok = wx.Button(self, 1, 'Ok')
        self.button_cancel = wx.Button(self, 2, 'Cancel')
        self.button_ok.Bind(wx.EVT_BUTTON, self.onOk)
        self.button_cancel.Bind(wx.EVT_BUTTON, self.onCancel)
        boxdown.Add(self.button_ok, -1, wx.ALL | wx.ALIGN_BOTTOM, 5)
        boxdown.Add(self.button_cancel, -1, wx.ALL | wx.ALIGN_BOTTOM, 5)

        boxglobal.Add(boxup, 5, wx.EXPAND, 5)
        boxglobal.Add(boxdown, 1, wx.EXPAND, 5)
        self.SetSizer(boxglobal)

    def onCancel(self, e):
        self.EndModal(wx.ID_CANCEL)

    def onOk(self, e):
        sel = self.lc.GetNextSelected(-1)
        if sel == -1:
            wx.MessageBox("Select a costume", "Error",
                          wx.OK | wx.ICON_INFORMATION)
        else:
            out = self.lc.GetItemText(sel, 0)
            out2 = self.resources.costumes[out]
            self.settings['costume'] = out2['name']
            self.EndModal(wx.ID_OK)

    def GetSettings(self):
        return self.settings

class AddSpriteDialog(wx.Dialog):

    def __init__(self, parent, id, title, resources):
        wx.Dialog.__init__(self, parent, id, title, size=(300, 330))
        self.settings = {}
        self.resources = resources

        boxglobal = wx.BoxSizer(wx.VERTICAL)

        boxup = wx.BoxSizer(wx.VERTICAL)

        self.lc = SelectCostume(self, -1, self.resources, False)
        boxup.Add(wx.StaticText(self, 0, 'Select costumes:'), 0,
                  wx.ALL, 5)
        boxup.Add(self.lc, 0, wx.ALL, 5)

        boxdown = wx.BoxSizer(wx.VERTICAL)

        boxdown1 = wx.BoxSizer(wx.HORIZONTAL)
        boxdown1.Add(wx.StaticText(self, 0, 'Insert sprite name:'), 0,
                     wx.ALL, 5)
        self.name = wx.TextCtrl(self, 0, '')
        boxdown1.Add(self.name, -1, wx.RIGHT, 5)

        boxdown2 = wx.BoxSizer(wx.HORIZONTAL)
        boxdown2.Add(wx.StaticText(self, 0, 'Insert base class name:'), 0,
                     wx.ALL, 5)
        self.classname = wx.TextCtrl(self, 0, '')
        boxdown2.Add(self.classname, -1, wx.RIGHT, 5)

        boxdown3 = wx.BoxSizer(wx.HORIZONTAL)
        self.button_ok = wx.Button(self, 1, 'Ok')
        self.button_cancel = wx.Button(self, 2, 'Cancel')
        self.button_ok.Bind(wx.EVT_BUTTON, self.onOk)
        self.button_cancel.Bind(wx.EVT_BUTTON, self.onCancel)
        boxdown3.Add(self.button_ok, -1, wx.ALL | wx.ALIGN_BOTTOM, 5)
        boxdown3.Add(self.button_cancel, -1, wx.ALL | wx.ALIGN_BOTTOM, 5)

        boxdown.Add(boxdown1, 1, wx.EXPAND, 5)
        boxdown.Add(boxdown2, 1, wx.EXPAND, 5)
        boxdown.Add(boxdown3, 1, wx.EXPAND, 5)

        boxglobal.Add(boxup, 1, wx.EXPAND, 5)
        boxglobal.Add(boxdown, 1, wx.EXPAND, 5)
        self.SetSizer(boxglobal)

    def onCancel(self, e):
        self.EndModal(wx.ID_CANCEL)

    def onOk(self, e):
        self.settings['name'] = self.name.GetValue()
        self.settings['base_class'] = self.classname.GetValue()
        sel = self.lc.GetNextSelected(-1)
        if self.settings['name'] == '' or \
                self.settings['base_class'] == '' or \
                sel == -1:
            wx.MessageBox("Values must not be null", "Error",
                          wx.OK | wx.ICON_INFORMATION)
        else:
            out = []
            out.append(self.lc.GetItemText(sel, 0))
            for i in range(0, self.lc.GetSelectedItemCount() - 1):
                sel = self.lc.GetNextSelected(sel)
                out.append(self.lc.GetItemText(sel, 0))
            self.settings['costumes'] = out
            self.EndModal(wx.ID_OK)

    def GetSettings(self):
        return self.settings

class DelSpriteDialog(wx.Dialog):

    def __init__(self, parent, id, title, resources):
        wx.Dialog.__init__(self, parent, id, title, size=(300, 300))
        self.settings = {}
        self.resources = resources

        boxglobal = wx.BoxSizer(wx.VERTICAL)

        boxup = wx.BoxSizer(wx.VERTICAL)
        self.lc = SelectSprite(self, -1, self.resources)
        boxup.Add(wx.StaticText(self, 0, 'Select a sprite to remove:'), 0,
                  wx.ALL, 5)
        boxup.Add(self.lc, 1, wx.ALL | wx.EXPAND, 5)

        boxdown = wx.BoxSizer(wx.HORIZONTAL)
        self.button_ok = wx.Button(self, 1, 'Ok')
        self.button_cancel = wx.Button(self, 2, 'Cancel')
        self.button_ok.Bind(wx.EVT_BUTTON, self.onOk)
        self.button_cancel.Bind(wx.EVT_BUTTON, self.onCancel)
        boxdown.Add(self.button_ok, -1, wx.ALL | wx.ALIGN_BOTTOM, 5)
        boxdown.Add(self.button_cancel, -1, wx.ALL | wx.ALIGN_BOTTOM, 5)

        boxglobal.Add(boxup, 5, wx.EXPAND, 5)
        boxglobal.Add(boxdown, 1, wx.EXPAND, 5)
        self.SetSizer(boxglobal)

    def onCancel(self, e):
        self.EndModal(wx.ID_CANCEL)

    def onOk(self, e):
        sel = self.lc.GetNextSelected(-1)
        if sel == -1:
            wx.MessageBox("Select a sprite", "Error",
                          wx.OK | wx.ICON_INFORMATION)
        else:
            out = self.lc.GetItemText(sel, 0)
            self.settings['sprite'] = out
            self.EndModal(wx.ID_OK)

    def GetSettings(self):
        return self.settings

