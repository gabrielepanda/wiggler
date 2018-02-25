import wx
import os

class Selection(wx.ListCtrl):


    def __init__(self, parent, id, resources, single_sel=True):
        if single_sel is True:
            style = wx.LC_REPORT | wx.LC_SINGLE_SEL
        else:
            style = wx.LC_REPORT
        wx.ListCtrl.__init__(self, parent, id, style=style)

        self.resources = resources

    def insert(self, title, item_list):
        self.InsertColumn(0, title, width=wx.LIST_AUTOSIZE_USEHEADER)
        for item_name in item_list:
            num_items = self.GetItemCount()
            self.InsertStringItem(num_items, item_name)


def unsaved_warning(parent):
    if wx.MessageBox("Current content has not been saved! Proceed?",
                     "Please confirm",
                     wx.ICON_QUESTION | wx.YES_NO, parent) == wx.NO:
        return False
    return True

