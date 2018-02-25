import wx

class Character(object):
    pass

class SelectCharacter(wx.ListCtrl):

    def __init__(self, parent, id, resources, single_sel=True):
        if single_sel is True:
            wx.ListCtrl.__init__(self, parent, id, style=wx.LC_REPORT |
                                 wx.LC_SINGLE_SEL)
        else:
            wx.ListCtrl.__init__(self, parent, id, style=wx.LC_REPORT)

        self.resources = resources
        self.InsertColumn(0, 'Character name',
                          width=wx.LIST_AUTOSIZE_USEHEADER)
        for sheetname in self.resources.characters.keys():
            num_items = self.GetItemCount()
            self.InsertStringItem(num_items, sheetname)


class SelectCharacterSprite(wx.ListCtrl):

    def __init__(self, parent, id, resources, char_name, single_sel=True):
        if single_sel is True:
            wx.ListCtrl.__init__(self, parent, id, style=wx.LC_REPORT |
                                 wx.LC_SINGLE_SEL)
        else:
            wx.ListCtrl.__init__(self, parent, id, style=wx.LC_REPORT)

        self.resources = resources
        self.InsertColumn(0, 'Sprite name',
                          width=wx.LIST_AUTOSIZE_USEHEADER)
        for sheetname in self.resources.characters[char_name]['sprites']:
            num_items = self.GetItemCount()
            self.InsertStringItem(num_items, sheetname)

def add_character(self):
    # dialog with definition, select from existing sprites or add empty
    dia = dialogs.AddCharacterDialog(None, -1, "Add a new character",
                                        self.resources)
    result = dia.ShowModal()
    if result == wx.ID_OK:
        self.settings = dia.GetSettings()
        try:
            self.resources.add_resource('characters',
                                        self.settings['name'],
                                        {'sprites': []})
        except ValueError as e:
            wx.MessageBox(str(e), "Error",
                            wx.OK | wx.ICON_INFORMATION)

    dia.Destroy()
    return True

def del_character(self):
    # LISTCTRK with name + sprite definition
    dia = dialogs.DelCharacterDialog(None, -1, "Delete character",
                                        self.resources)
    result = dia.ShowModal()
    if result == wx.ID_OK:
        self.settings = dia.GetSettings()
        for x in self.resources.find_deps('characters',
                                            self.settings['character']):
            for elem in x:
                try:
                    self.resources.remove_resource(elem[0], elem[1])
                except Exception as e:
                    wx.MessageBox(str(e), "Error", wx.OK |
                                    wx.ICON_INFORMATION)

        try:
            self.resources.remove_resource('characters',
                                            self.settings['character'])
        except Exception as e:
            wx.MessageBox(str(e), "Error", wx.OK | wx.ICON_INFORMATION)

    dia.Destroy()
    return True

class AddSpriteToCharDialog(wx.Dialog):

    def __init__(self, parent, id, title, resources):
        wx.Dialog.__init__(self, parent, id, title, size=(300, 300))
        self.settings = {}
        self.resources = resources

        boxglobal = wx.BoxSizer(wx.VERTICAL)

        boxup = wx.BoxSizer(wx.VERTICAL)
        self.lc = SelectSprite(self, -1, self.resources)
        boxup.Add(wx.StaticText(self, 0,
                                'Select a sprite to copy from:'),
                  0, wx.ALL, 5)
        boxup.Add(self.lc, 1, wx.ALL | wx.EXPAND, 5)

        box1 = wx.BoxSizer(wx.HORIZONTAL)
        box1.Add(wx.StaticText(self, 0, 'Specify sprite name:'), 0,
                 wx.ALL | wx.ALIGN_CENTER, 5)
        self.name = wx.TextCtrl(self, 0, '')
        box1.Add(self.name, -1, wx.RIGHT | wx.ALIGN_CENTER, 5)

        boxdown = wx.BoxSizer(wx.HORIZONTAL)
        self.button_ok = wx.Button(self, 1, 'Ok')
        self.button_cancel = wx.Button(self, 2, 'Cancel')
        self.button_ok.Bind(wx.EVT_BUTTON, self.onOk)
        self.button_cancel.Bind(wx.EVT_BUTTON, self.onCancel)
        boxdown.Add(self.button_ok, -1, wx.ALL | wx.ALIGN_BOTTOM, 5)
        boxdown.Add(self.button_cancel, -1, wx.ALL | wx.ALIGN_BOTTOM, 5)

        boxglobal.Add(boxup, 5, wx.EXPAND, 5)
        boxglobal.Add(box1, 5, wx.EXPAND, 5)
        boxglobal.Add(boxdown, 1, wx.EXPAND, 5)
        self.SetSizer(boxglobal)

    def onCancel(self, e):
        self.EndModal(wx.ID_CANCEL)

    def onOk(self, e):
        sel = self.lc.GetNextSelected(-1)
        if sel == -1:
            pass
        else:
            out = self.lc.GetItemText(sel, 0)
            self.settings['base'] = out
            self.EndModal(wx.ID_OK)
        self.settings['sprite'] = self.name.GetValue()

    def GetSettings(self):
        return self.settings


class DelSpriteFromCharDialog(wx.Dialog):

    def __init__(self, parent, id, title, resources, char_name):
        wx.Dialog.__init__(self, parent, id, title, size=(300, 300))
        self.settings = {}
        self.resources = resources

        boxglobal = wx.BoxSizer(wx.VERTICAL)

        boxup = wx.BoxSizer(wx.VERTICAL)
        self.lc = SelectCharacterSprite(self, -1, self.resources, char_name)
        boxup.Add(wx.StaticText(self, 0,
                                'Select a sprite to remove from character:'),
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
            wx.MessageBox("Select a sprite", "Error",
                          wx.OK | wx.ICON_INFORMATION)
        else:
            out = self.lc.GetItemText(sel, 0)
            self.settings['sprite'] = out
            self.EndModal(wx.ID_OK)

    def GetSettings(self):
        return self.settings


class AddCharacterDialog(wx.Dialog):

    def __init__(self, parent, id, title, resources):
        wx.Dialog.__init__(self, parent, id, title, size=(300, 100))
        self.settings = {}
        self.resources = resources

        boxglobal = wx.BoxSizer(wx.VERTICAL)

        box1 = wx.BoxSizer(wx.HORIZONTAL)
        box1.Add(wx.StaticText(self, 0, 'Define character name:'), 0,
                 wx.ALL | wx.ALIGN_CENTER, 5)
        self.name = wx.TextCtrl(self, 0, '')
        box1.Add(self.name, -1, wx.RIGHT | wx.ALIGN_CENTER, 5)

        box2 = wx.BoxSizer(wx.HORIZONTAL)
        self.button_ok = wx.Button(self, 1, 'Ok')
        self.button_cancel = wx.Button(self, 2, 'Cancel')
        self.button_ok.Bind(wx.EVT_BUTTON, self.onOk)
        self.button_cancel.Bind(wx.EVT_BUTTON, self.onCancel)
        box2.Add(self.button_ok, -1, wx.ALL | wx.ALIGN_BOTTOM, 5)
        box2.Add(self.button_cancel, -1, wx.ALL | wx.ALIGN_BOTTOM, 5)

        boxglobal.Add(box1, 1, wx.EXPAND, 5)
        boxglobal.Add(box2, 1, wx.EXPAND, 5)

        self.SetSizer(boxglobal)

    def onCancel(self, e):
        self.EndModal(wx.ID_CANCEL)

    def onOk(self, e):
        self.settings['name'] = self.name.GetValue()
        if self.settings['name'] == '':
            wx.MessageBox("Insert a name", "Error",
                          wx.OK | wx.ICON_INFORMATION)
        else:
            self.EndModal(wx.ID_OK)

    def GetSettings(self):
        return self.settings


class DelCharacterDialog(wx.Dialog):

    def __init__(self, parent, id, title, resources):
        wx.Dialog.__init__(self, parent, id, title, size=(300, 300))
        self.settings = {}
        self.resources = resources

        boxglobal = wx.BoxSizer(wx.VERTICAL)

        boxup = wx.BoxSizer(wx.VERTICAL)
        self.lc = SelectCharacter(self, -1, self.resources)
        boxup.Add(wx.StaticText(self, 0, 'Select a character to remove:'), 0,
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
            wx.MessageBox("Select a character", "Error",
                          wx.OK | wx.ICON_INFORMATION)
        else:
            out = self.lc.GetItemText(sel, 0)
            self.settings['character'] = out
            self.EndModal(wx.ID_OK)

    def GetSettings(self):
        return self.settings


