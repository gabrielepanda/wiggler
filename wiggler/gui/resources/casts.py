import wx

class Cast(object):
    pass

class AddCharToProjDialog(wx.Dialog):

    def __init__(self, parent, id, title, resources):
        wx.Dialog.__init__(self, parent, id, title, size=(300, 300))
        self.settings = {}
        self.resources = resources

        boxglobal = wx.BoxSizer(wx.VERTICAL)

        boxup = wx.BoxSizer(wx.VERTICAL)
        self.lc = SelectCharacter(self, -1, self.resources)
        boxup.Add(wx.StaticText(self, 0,
                                'Select a character to copy from:'),
                  0, wx.ALL, 5)
        boxup.Add(self.lc, 1, wx.ALL | wx.EXPAND, 5)

        box1 = wx.BoxSizer(wx.HORIZONTAL)
        box1.Add(wx.StaticText(self, 0, 'Specify character name:'), 0,
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
        self.settings['character'] = self.name.GetValue()

    def GetSettings(self):
        return self.settings


class DelCharFromProjDialog(wx.Dialog):

    def __init__(self, parent, id, title, resources, char_name):
        wx.Dialog.__init__(self, parent, id, title, size=(300, 300))
        self.settings = {}
        self.resources = resources

        boxglobal = wx.BoxSizer(wx.VERTICAL)

        boxup = wx.BoxSizer(wx.VERTICAL)
        self.lc = SelectCharacterSprite(self, -1, self.resources, char_name)
        boxup.Add(wx.StaticText(self, 0,
                                'Select a chracter to remove from project:'),
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
            wx.MessageBox("Select a character", "Error",
                          wx.OK | wx.ICON_INFORMATION)
        else:
            out = self.lc.GetItemText(sel, 0)
            self.settings['character'] = out
            self.EndModal(wx.ID_OK)

    def GetSettings(self):
        return self.settings

