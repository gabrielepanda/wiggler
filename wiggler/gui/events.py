import wx

from wiggler.core.singleton import Singleton


class Data(object):
    ''' Generic Empty Data Object'''
    pass


class GuiCommandEvent(wx.PyCommandEvent):

    def __init__(self, evtType, command_type, **data):
        wx.PyCommandEvent.__init__(self, evtType)
        self.command_type = command_type
        self.data = Data()
        for key, value in data.items():
            setattr(self.data, key, value)

class Event(object):

    def __init__(self):
        self.binders = {}

        self.GUI_READY = wx.NewId()
        self.CHARACTER_RESOURCE_LOADED = wx.NewId()
        self.TEST_EVENT = self.new_event()
        self.CHARACTER_SELECTED = wx.NewId()


        # TO FIX
        self.PLAY_GAME = wx.NewId()
        self.SUFFICIENCY_INCREASE = wx.NewId()
        self.SUFFICIENCY_DECREASE = wx.NewId()
        self.LINK_SPRITE_COSTUME = wx.NewId()
        self.UNLINK_SPRITE_COSTUME = wx.NewId()
        self.LINK_CHARACTER_SPRITE = wx.NewId()
        self.UNLINK_CHARACTER_SPRITE = wx.NewId()
        self.LINK_CAST_CHARACTER = wx.NewId()
        self.UNLINK_CAST_CHARACTER = wx.NewId()
        self.ADD_COSTUME = wx.NewId()
        self.DEL_COSTUME = wx.NewId()
        self.ADD_SHEET = wx.NewId()
        self.DEL_SHEET = wx.NewId()
        self.ADD_IMAGE = wx.NewId()
        self.DEL_IMAGE = wx.NewId()
        self.ADD_CHARACTER = wx.NewId()
        self.DEL_CHARACTER = wx.NewId()
        self.ADD_ANIMATION = wx.NewId()
        self.DEL_ANIMATION = wx.NewId()
        self.ADD_SPRITE = wx.NewId()
        self.DEL_SPRITE = wx.NewId()
        self.CHANGE_BACKGROUND = wx.NewId()
        self.SPRITE_SELECTED = wx.NewId()
        self.PROJECT_RUN = wx.NewId()
        self.PROJECT_STOP = wx.NewId()

    def new_event(self):
        event_type = wx.NewEventType()
        self.binders[event_type] = wx.PyEventBinder(event_type, 1)
        return event_type

guievent = Event()

class EventQueue(object):
    __metaclass__ = Singleton

    def __init__(self):
        self.EVT_TYPE_NOTICE = wx.NewEventType()
        self.EVT_NOTICE = wx.PyEventBinder(self.EVT_TYPE_NOTICE, 1)
        self.subscribers = {}

    # FIXME: Broadcast to send events to root, remove subscribe
    def broadcast(self, command_type, **data):
        event = GuiCommandEvent(self.EVT_TYPE_NOTICE, command_type, **data)
        try:
            for window in self.subscribers[command_type]:
                print window, event
                wx.PostEvent(window.GetEventHandler(), event)
        except KeyError:
            pass

    def subscribe(self, window, commands):
        for command in commands:
            if command not in self.subscribers.keys():
                self.subscribers[command] = []
            self.subscribers[command].append(window)


class GUICommandHandler(object):

    def __init__(self, window, command_map):
        self.window = window
        self._command_map = {}
        if command_map is not None:
            self._command_map = command_map
        self.event_queue = EventQueue()
        subscriptions = self._command_map.keys()
        self.event_queue.subscribe(self.window, subscriptions)
        self.window.Bind(self.event_queue.EVT_NOTICE, self.service)

    def service(self, event):
        print event
        callback = self._command_map[event.command_type]

        callback(event)
        event.Skip()

