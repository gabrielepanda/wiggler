import wx

from wiggler.core.resources.projects import Project as CoreProject

class Project(CoreProject):

    def __init__(self, asset_id):
        super(Project, self).__init__(asset_id)

    def open_project(parent):
        open_file = wx.FileDialog(parent, "Open wiggler project", "", "",
                                "wig files (*.wig)|*.wig",
                                wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)
        if open_file.ShowModal() == wx.ID_CANCEL:
            return None
        return open_file.GetPath()


    def save_project(parent):
        save_file = wx.FileDialog(parent, "Save wiggler project", "", "",
                                "wig files (*.wig)|*.wig",
                                wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT)
        if save_file.ShowModal() == wx.ID_CANCEL:
            return None
        return save_file.GetPath()

    def set_active_character(self, name=None, index=None):
        if name is not None:
            for index in self.indexes:
                if self.indexes[index] == self.characters[name]:
                    break
        if index is not None:
            self.active_character = index
        return self.indexes[index]

class ChangeBackgroundDialog(wx.Dialog):

    def __init__(self, parent):
        wx.Dialog.__init__(self, parent, wx.ID_ANY,
                           "background", size=(300, 300))

        boxglobal = wx.BoxSizer(wx.VERTICAL)
        boxdown = wx.BoxSizer(wx.VERTICAL)

        boxdown1 = wx.BoxSizer(wx.HORIZONTAL)
        boxdown1.Add(wx.StaticText(self, 0, 'Insert background type'), 0,
                     wx.ALL, 5)
        self.back_type = wx.TextCtrl(self, 0, '')
        boxdown1.Add(self.back_type, -1, wx.Right, 5)

        boxdown2 = wx.BoxSizer(wx.HORIZONTAL)
        boxdown2.Add(wx.StaticText(self, 0, 'Insert background specs'), 0,
                     wx.ALL, 5)
        self.back_spec = wx.TextCtrl(self, 0, '')
        boxdown2.Add(self.back_spec, -1, wx.Right, 5)

        boxdown4 = wx.BoxSizer(wx.HORIZONTAL)
        self.button_ok = wx.Button(self, 1, 'Ok')
        self.button_cancel = wx.Button(self, 2, 'Cancel')
        self.button_ok.Bind(wx.EVT_BUTTON, self.onOk)
        self.button_cancel.Bind(wx.EVT_BUTTON, self.onCancel)
        boxdown4.Add(self.button_ok, -1, wx.ALL | wx.ALIGN_BOTTOM, 5)
        boxdown4.Add(self.button_cancel, -1, wx.ALL | wx.ALIGN_BOTTOM, 5)

        boxdown.Add(boxdown1, 1, wx.EXPAND, 5)
        boxdown.Add(boxdown2, 1, wx.EXPAND, 5)
        boxdown.Add(boxdown4, 1, wx.EXPAND, 5)

        boxglobal.Add(boxdown, 1, wx.EXPAND, 5)
        self.SetSizer(boxglobal)

    def onOk(self, e):
        self.EndModal(wx.ID_OK)

    def onCancel(self, e):
        self.EndModal(wx.ID_CANCEL)
