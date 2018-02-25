from wiggler.gui.dialogs import Selection

class SelectSheet(Selection):

    def __init__(self, parent, id, resources, single_sel=True):
        if single_sel is True:
            wx.ListCtrl.__init__(self, parent, id, style=wx.LC_REPORT |
                                 wx.LC_SINGLE_SEL)
        else:
            wx.ListCtrl.__init__(self, parent, id, style=wx.LC_REPORT)

        self.resources = resources
        self.InsertColumn(0, 'Sheet file', width=wx.LIST_AUTOSIZE_USEHEADER)
        for sheetname in self.resources.sheets.keys():
            num_items = self.GetItemCount()
            self.InsertStringItem(num_items, sheetname)

def open_sheet(parent):
    options = wx.FD_OPEN | wx.FD_FILE_MUST_EXIST | wx.FD_PREVIEW
    open_file = wx.FileDialog(parent, "Select sheet file", "", "",
                              "", options)
    if open_file.ShowModal() == wx.ID_CANCEL:
        return None
    return open_file.GetPath()

def add_sheet(self):
    # definition_fields = Factory_sheet.definition_fields
    # dialog with definition fields, source file with browse button
    # resource with same name , overwrite ?
    filename = dialogs.open_sheet(self.parent)
    if filename is not None:
        dia = dialogs.AddSheetDialog(None, -1, "Insert sheet details",
                                        self.resources)
        result = dia.ShowModal()
        if result == wx.ID_OK:
            self.settings = dia.GetSettings()
            try:
                self.resources.add_resource(
                    'sheets', self.settings['name'],
                    {'colorkey': self.settings['colorkey'],
                        'abs_path': filename})
            except ValueError as e:
                wx.MessageBox(str(e), "Error",
                                wx.OK | wx.ICON_INFORMATION)
        dia.Destroy()
    return True

def del_sheet(self):
    # LISTCTR with very large icons ?
    # use resources.find_deps
    # print self.resources.find_deps('sheets', 'master')
    # name = 'testsheet'
    # self.resources.remove_resource('sheets', name)
    # and everything associated to IT!!!
    dia = dialogs.DelSheetDialog(None, -1, "Delete sheet",
                                    self.resources)
    result = dia.ShowModal()
    if result == wx.ID_OK:
        self.settings = dia.GetSettings()
        for x in self.resources.find_deps('sheets',
                                            self.settings['sheet']):
            for elem in x:
                try:
                    self.resources.remove_resource(elem[0], elem[1])
                except Exception as e:
                    wx.MessageBox(str(e), "Error", wx.OK |
                                    wx.ICON_INFORMATION)

        try:
            self.resources.remove_resource('sheets',
                                            self.settings['sheet'])
        except Exception as e:
            wx.MessageBox(str(e), "Error", wx.OK | wx.ICON_INFORMATION)

    dia.Destroy()
    return True

class AddSheetDialog(wx.Dialog):

    def __init__(self, parent, id, title, resources):
        wx.Dialog.__init__(self, parent, id, title, size=(270, 180))
        self.settings = {}
        self.resources = resources

        boxglobal = wx.BoxSizer(wx.VERTICAL)

        box1 = wx.BoxSizer(wx.HORIZONTAL)
        box1.Add(wx.StaticText(self, 0, 'Define sheet name:'), 0,
                 wx.ALL | wx.ALIGN_CENTER, 5)
        self.name = wx.TextCtrl(self, 0, '')
        box1.Add(self.name, -1, wx.RIGHT | wx.ALIGN_CENTER, 5)

        box2 = wx.BoxSizer(wx.HORIZONTAL)
        box2.Add(wx.StaticText(self, -1, 'Set colorkey:'), 0,
                 wx.ALL | wx.ALIGN_BOTTOM, 5)

        box3 = wx.GridSizer(1, 6, 0, 0)
        box3.Add(wx.StaticText(self, -1, 'R:'), 0,
                 wx.ALL | wx.ALIGN_RIGHT, 5)
        self.rvalue = wx.SpinCtrl(self, -1, '0', size=wx.Size(48, -1),
                                  min=0, max=255)
        box3.Add(self.rvalue, 0, 0, 5)
        box3.Add(wx.StaticText(self, -1, 'G:'), 0,
                 wx.ALL | wx.ALIGN_RIGHT, 5)
        self.gvalue = wx.SpinCtrl(self, -1, '0', size=wx.Size(48, -1),
                                  min=0, max=255)
        box3.Add(self.gvalue, 0, 0, 5)
        box3.Add(wx.StaticText(self, -1, 'B:'), 0,
                 wx.ALL | wx.ALIGN_RIGHT, 5)
        self.bvalue = wx.SpinCtrl(self, -1, '0', size=wx.Size(48, -1),
                                  min=0, max=255)
        box3.Add(self.bvalue, 0, 0, 5)

        box4 = wx.BoxSizer(wx.HORIZONTAL)
        self.button_ok = wx.Button(self, 1, 'Ok')
        self.button_cancel = wx.Button(self, 2, 'Cancel')
        self.button_ok.Bind(wx.EVT_BUTTON, self.onOk)
        self.button_cancel.Bind(wx.EVT_BUTTON, self.onCancel)
        box4.Add(self.button_ok, -1, wx.ALL | wx.ALIGN_BOTTOM, 5)
        box4.Add(self.button_cancel, -1, wx.ALL | wx.ALIGN_BOTTOM, 5)

        boxglobal.Add(box1, 1, wx.EXPAND, 5)
        boxglobal.Add(box2, 1, wx.EXPAND, 5)
        boxglobal.Add(box3, 1, wx.EXPAND | wx.ALL, 5)
        boxglobal.Add(box4, 1, wx.EXPAND, 5)

        self.SetSizer(boxglobal)

    def onCancel(self, e):
        self.EndModal(wx.ID_CANCEL)

    def onOk(self, e):
        self.settings['name'] = self.name.GetValue()
        self.settings['colorkey'] = str(self.rvalue.GetValue()) + \
            ',' + str(self.gvalue.GetValue()) + \
            ',' + str(self.bvalue.GetValue())
        if self.settings['name'] == '':
            wx.MessageBox("Insert a name", "Error",
                          wx.OK | wx.ICON_INFORMATION)
        else:
            self.EndModal(wx.ID_OK)

    def GetSettings(self):
        return self.settings


class DelSheetDialog(wx.Dialog):

    def __init__(self, parent, id, title, resources):
        wx.Dialog.__init__(self, parent, id, title, size=(300, 300))
        self.settings = {}
        self.resources = resources

        boxglobal = wx.BoxSizer(wx.VERTICAL)

        boxup = wx.BoxSizer(wx.VERTICAL)
        self.lc = SelectSheet(self, -1, self.resources)
        boxup.Add(wx.StaticText(self, 0, 'Select a sheet to remove:'), 0,
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
            wx.MessageBox("Select a sheet", "Error",
                          wx.OK | wx.ICON_INFORMATION)
        else:
            out = self.lc.GetItemText(sel, 0)
            self.settings['sheet'] = out
            self.EndModal(wx.ID_OK)

    def GetSettings(self):
        return self.settings

