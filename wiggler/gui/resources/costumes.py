
class SelectCostume(wx.ListCtrl):

    def __init__(self, parent, id, resources, single_sel=True):
        if single_sel is True:
            wx.ListCtrl.__init__(self, parent, id, style=wx.LC_REPORT |
                                 wx.LC_SINGLE_SEL)
        else:
            wx.ListCtrl.__init__(self, parent, id, style=wx.LC_REPORT)

        self.resources = resources
        self.InsertColumn(0, 'Costume name', width=wx.LIST_AUTOSIZE_USEHEADER)
        for sheetname in self.resources.costumes.keys():
            num_items = self.GetItemCount()
            self.InsertStringItem(num_items, sheetname)

def add_costume(self):
    # dialog with definitions and a area selection on the sheet
    dia = dialogs.AddCostumeDialog(None, -1, "Add a new costume",
                                    self.resources)
    result = dia.ShowModal()
    if result == wx.ID_OK:
        self.settings = dia.GetSettings()
        # print self.settings['name'], self.settings['rect'], \
        #    self.settings['sheet']
        try:
            self.resources.add_resource(
                'costumes', self.settings['name'],
                {'name': self.settings['name'],
                    'sheet': self.settings['sheet'],
                    'rect': self.settings['rect']})
        except ValueError as e:
            wx.MessageBox(str(e), "Error",
                            wx.OK | wx.ICON_INFORMATION)
    dia.Destroy()
    return True

def del_costume(self):
    # LISTCTRL with large icons
    dia = dialogs.DelCostumeDialog(None, -1, "Delete costume",
                                    self.resources)
    result = dia.ShowModal()
    if result == wx.ID_OK:
        self.settings = dia.GetSettings()
        for x in self.resources.find_deps('costumes',
                                            self.settings['costume']):
            for elem in x:
                try:
                    self.resources.remove_resource(elem[0], elem[1])
                except Exception as e:
                    wx.MessageBox(str(e), "Error", wx.OK |
                                    wx.ICON_INFORMATION)

        try:
            self.resources.remove_resource('costumes',
                                            self.settings['costume'])
        except Exception as e:
            wx.MessageBox(str(e), "Error", wx.OK | wx.ICON_INFORMATION)

    dia.Destroy()
    return True
class DelCostumeDialog(wx.Dialog):

    def __init__(self, parent, id, title, resources):
        wx.Dialog.__init__(self, parent, id, title, size=(300, 300))
        self.settings = {}
        self.resources = resources

        boxglobal = wx.BoxSizer(wx.VERTICAL)

        boxup = wx.BoxSizer(wx.VERTICAL)
        self.lc = SelectCostume(self, -1, self.resources)
        boxup.Add(wx.StaticText(self, 0, 'Select a costume to remove:'), 0,
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
            wx.MessageBox("Select a costume", "Error",
                          wx.OK | wx.ICON_INFORMATION)
        else:
            out = self.lc.GetItemText(sel, 0)
            out2 = self.resources.costumes[out]
            self.settings['costume'] = out2['name']
            self.EndModal(wx.ID_OK)

    def GetSettings(self):
        return self.settings

class AddCostumeDialog(wx.Dialog):

    def __init__(self, parent, id, title, resources):
        wx.Dialog.__init__(self, parent, id, title, size=(300, 380))
        self.settings = {}
        self.resources = resources

        boxglobal = wx.BoxSizer(wx.VERTICAL)

        boxup = wx.BoxSizer(wx.VERTICAL)

        self.lc = SelectSheet(self, -1, self.resources)
        boxup.Add(wx.StaticText(self, 0, 'Select source sheet file:'), 0,
                  wx.ALL, 5)
        boxup.Add(self.lc, 0, wx.ALL, 5)

        boxdown = wx.BoxSizer(wx.VERTICAL)

        boxdown1 = wx.BoxSizer(wx.HORIZONTAL)
        boxdown1.Add(wx.StaticText(self, 0, 'Insert costume name:'), 0,
                     wx.ALL, 5)
        self.name = wx.TextCtrl(self, 0, '')
        boxdown1.Add(self.name, -1, wx.RIGHT, 5)

        boxdown2 = wx.BoxSizer(wx.HORIZONTAL)
        boxdown2.Add(wx.StaticText(self, -1, 'Define costume RECT:'), 0,
                     wx.ALL | wx.ALIGN_BOTTOM, 5)

        boxdown3 = wx.GridSizer(2, 5, 0, 0)
        boxdown3.Add(wx.StaticText(self, -1, 'Origin point:'), 0, wx.ALL, 5)
        boxdown3.Add(wx.StaticText(self, -1, 'X:'), 0,
                     wx.ALL | wx.ALIGN_RIGHT, 5)
        self.originx = wx.SpinCtrl(self, -1, '0', size=wx.Size(55, -1),
                                   min=0, max=4000)
        boxdown3.Add(self.originx, 0, 0, 5)
        boxdown3.Add(wx.StaticText(self, -1, 'Y:'), 0,
                     wx.ALL | wx.ALIGN_RIGHT, 5)
        self.originy = wx.SpinCtrl(self, -1, '0', size=wx.Size(55, -1),
                                   min=0, max=4000)
        boxdown3.Add(self.originy, 0, 0, 5)
        boxdown3.Add(wx.StaticText(self, -1, 'Side size:'), 0, wx.ALL, 5)
        boxdown3.Add(wx.StaticText(self, -1, 'X:'), 0,
                     wx.ALL | wx.ALIGN_RIGHT, 5)
        self.sidex = wx.SpinCtrl(self, -1, '0', size=wx.Size(55, -1),
                                 min=0, max=4000)
        boxdown3.Add(self.sidex, 0, 0, 5)
        boxdown3.Add(wx.StaticText(self, -1, 'Y:'), 0,
                     wx.ALL | wx.ALIGN_RIGHT, 5)
        self.sidey = wx.SpinCtrl(self, -1, '0', size=wx.Size(55, -1),
                                 min=0, max=4000)
        boxdown3.Add(self.sidey, 0, 0, 5)

        boxdown4 = wx.BoxSizer(wx.HORIZONTAL)
        self.button_ok = wx.Button(self, 1, 'Ok')
        self.button_cancel = wx.Button(self, 2, 'Cancel')
        self.button_ok.Bind(wx.EVT_BUTTON, self.onOk)
        self.button_cancel.Bind(wx.EVT_BUTTON, self.onCancel)
        boxdown4.Add(self.button_ok, -1, wx.ALL | wx.ALIGN_BOTTOM, 5)
        boxdown4.Add(self.button_cancel, -1, wx.ALL | wx.ALIGN_BOTTOM, 5)

        boxdown.Add(boxdown1, 1, wx.EXPAND, 5)
        boxdown.Add(boxdown2, 1, wx.EXPAND, 5)
        boxdown.Add(boxdown3, 1, wx.EXPAND, 5)
        boxdown.Add(boxdown4, 1, wx.EXPAND, 5)

        boxglobal.Add(boxup, 1, wx.EXPAND, 5)
        boxglobal.Add(boxdown, 1, wx.EXPAND, 5)
        self.SetSizer(boxglobal)

    def onCancel(self, e):
        self.EndModal(wx.ID_CANCEL)

    def onOk(self, e):
        self.settings['name'] = self.name.GetValue()
        self.settings['rect'] = str(self.originx.GetValue()) + \
            ', ' + str(self.originy.GetValue()) + \
            ', ' + str(self.sidex.GetValue()) + \
            ', ' + str(self.sidey.GetValue())
        sel = self.lc.GetNextSelected(-1)
        if self.settings['name'] == '' or \
                self.settings['rect'] == '0, 0, 0, 0' or \
                sel == -1:
            wx.MessageBox("Values must not be null", "Error",
                          wx.OK | wx.ICON_INFORMATION)
        else:
            out = self.lc.GetItemText(sel, 0)
            out2 = self.resources.sheets[out]
            self.settings['sheet'] = os.path.basename(out2['abs_path'])
            self.EndModal(wx.ID_OK)

    def GetSettings(self):
        return self.settings
