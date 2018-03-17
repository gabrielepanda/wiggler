import pygame
import wx

from wiggler.common.singleton import Singleton

class StageEvents(object):

    def __init__(self):
        self.mouse_pos = (0, 0)
        # There's really no sane way to translate wx events into
        # SDL events without using SDL (and it will still be
        # challenging)
        # Add code to this map as needed
        self.keymap = {
            wx.WXK_UP: pygame.K_UP,
            wx.WXK_DOWN: pygame.K_DOWN,
            wx.WXK_RIGHT: pygame.K_RIGHT,
            wx.WXK_LEFT: pygame.K_LEFT,
            wx.WXK_SPACE: pygame.K_SPACE,
            wx.WXK_ALT: pygame.K_LALT,
            wx.WXK_CONTROL: pygame.K_LCTRL,
            wx.WXK_SHIFT: pygame.K_LSHIFT,
            wx.WXK_WINDOWS_LEFT: pygame.K_LMETA,
            wx.WXK_WINDOWS_RIGHT: pygame.K_RMETA,
        }

    @staticmethod
    def pygame_inject_event(p_type, p_attrs):
        if p_type is not None:
            p_event = pygame.event.Event(p_type, p_attrs)
            pygame.event.post(p_event)

    def translate_key(self, wx_event):
        p_type = None
        p_attrs = {}
        p_key = 0
        mod = pygame.KMOD_NONE
        scancode = wx_event.GetRawKeyFlags()
        wx_key = wx_event.GetKeyCode()

        try:
            p_key = self.keymap[wx_key]
        except KeyError:
            try:
                p_key = ord(chr(wx_key).lower())
            except ValueError:
                return
        if wx_event.ShiftDown() and wx_key != wx.WXK_SHIFT:
            mod += pygame.KMOD_SHIFT
        if wx_event.AltDown() and wx_key != wx.WXK_ALT:
            mod += pygame.KMOD_ALT
        if wx_event.ControlDown() and wx_key != wx.WXK_CONTROL:
            mod += pygame.KMOD_CTRL
        if wx_event.MetaDown() and wx_key not in [wx.WXK_WINDOWS_LEFT,
                                                  wx.WXK_WINDOWS_RIGHT]:
            mod += pygame.KMOD_META
        p_attrs = {
            'scancode': scancode,
            'key': p_key,
            'mod': mod,
        }
        wx_type = wx_event.GetEventType()
        if wx_type == wx.EVT_KEY_DOWN.typeId:
            p_type = pygame.KEYDOWN
            p_attrs['unicode'] = unichr(wx_event.GetUnicodeKey())
        elif wx_type == wx.EVT_KEY_UP.typeId:
            p_type = pygame.KEYUP

        self.pygame_inject_event(p_type, p_attrs)

    @staticmethod
    def get_button(wx_event):
        if wx_event.LeftDown() or wx_event.LeftUp():
            button = 1
        elif wx_event.MiddleDown() or wx_event.MiddleUp():
            button = 2
        elif wx_event.RightDown() or wx_event.RightUp():
            button = 3
        return button

    def translate_mouse(self, wx_event):
        p_type = None
        p_attrs = {}
        p_attrs['pos'] = wx_event.GetPositionTuple()
        rel_posx = p_attrs['pos'][0] - self.mouse_pos[0]
        rel_posy = p_attrs['pos'][1] - self.mouse_pos[1]
        p_attrs['rel'] = (rel_posx, rel_posy)
        self.mouse_pos = p_attrs['pos']
        if wx_event.IsButton():
            if wx_event.ButtonDown():
                p_type = pygame.MOUSEBUTTONDOWN
                p_attrs['button'] = self.get_button(wx_event)
            elif wx_event.ButtonUp():
                p_type = pygame.MOUSEBUTTONUP
                p_attrs['button'] = self.get_button(wx_event)
        elif wx_event.Moving() or wx_event.Dragging and  \
                p_attrs['pos'] != self.mouse_pos:
            p_type = pygame.MOUSEMOTION
            buttons = [0, 0, 0]
            if wx_event.LeftIsDown():
                buttons[0] = 1
            if wx_event.MiddleIsDown():
                buttons[1] = 1
            if wx_event.RightIsDown():
                buttons[2] = 1
            p_attrs['buttons'] = tuple(buttons)

        self.pygame_inject_event(p_type, p_attrs)
        wx_event.Skip(True)


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
        callback = self._command_map[event.command_type]

        callback(event)
        event.Skip()

