import os
import pygame
import sys
import wx
import subprocess

from multiprocessing.connection import Listener
from wiggler.gui.events import EventQueue, guievent, GUICommandHandler
#from wiggler.engine.stage import Stage

tilemap = dict()


class StagePane(wx.Control):

    def __init__(self, parent, id, **options):
        wx.Control.__init__(*(self, parent, id), **options)
        self.parent = parent
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

        self._initialized = 0
        self._resized = 0
        self._surface = None
        self.__needsDrawing = 1
        self.size = self.GetSizeTuple()

        wx.EVT_IDLE(self, self.OnIdle)
        wx.EVT_SIZE(self, self.OnSize)
        self.address = ('localhost', 6000)
        self.listener = Listener(self.address, authkey='secret password')
        self.conn = None
        self.command_map = {
            guievent.PROJECT_RUN:
                self.project_launch,
            guievent.PROJECT_STOP:
                self.project_stop,
        }
        self.events = GUICommandHandler(self, self.command_map)
        self._project_running = False
        #self.parent.Bind(wx.EVT_MENU, self.resources.event_handler)
        self.Bind(wx.EVT_KEY_DOWN, self.translate_key)
        self.Bind(wx.EVT_KEY_UP, self.translate_key)
        self.Bind(wx.EVT_MOUSE_EVENTS, self.translate_mouse)
        return
        self.stage = Stage(self.resources)
        self.events = EventQueue()
        self.timer = wx.Timer(self)
        self.events.subscribe(self, ['projload', 'play', 'stop'])
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_TIMER, self.Update, self.timer)
        self.Bind(self.events.EVT_NOTICE, self.notice_handler)

        self.max_fps = 25.0
        self.timespacing = 1000.0 / self.max_fps
        self.timer.Start(self.timespacing, False)
        self.default_backcolor = (255, 255, 255)

    def notice_handler(self, event):
        if event.notice == 'projload':
            self.clear()
        elif event.notice == 'play':
            self.play()
        elif event.notice == 'stop':
            self.stop()
        event.Skip()

    def OnIdle(self, ev):
        if not self._initialized or self._resized:
            if not self._initialized:
                hwnd = self.GetHandle()
                os.environ['SDL_WINDOWID'] = str(hwnd)
                if sys.platform == 'win32':
                    os.environ['SDL_VIDEODRIVER'] = 'windib'
                self._initialized = 1
        else:
            self._resized = 0

        if self._project_running:
            if self.conn.poll():
                print "poll returned"
                try:
                    msg= self.conn.recv()
                    print msg
                except EOFError:
                    print "EOF"

    def project_launch(self, event):

        self._project_running = True
        self.game_process = subprocess.Popen("/usr/bin/python /workspace/gabriele/wiggler/wiggler/pygame_test.py", shell=True, close_fds=True, stdout=subprocess.PIPE)
        self.conn = self.listener.accept()
        print 'connection accepted from', self.listener.last_accepted

    def project_stop(self, event):
        self._project_running = False
        self.conn.send((pygame.QUIT, {}))
        out, err = self.game_process.communicate()
        #self.game_process.terminate()
        print out, err
        self.conn.close()
        #self.listener.close()

    def translate_key(self, wx_event):
        if not self._project_running:
            wx_event.Skip(True)
            return
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

        if p_type is not None:
            self.conn.send((p_type, p_attrs))

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
        if not self._project_running:
            wx_event.Skip(True)
            return
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

        if p_type is not None:
            self.conn.send((p_type, p_attrs))
        wx_event.Skip(True)

    def clear(self):
        self.stage.sweep()

    def OnPaint(self, ev):
        self.Redraw()

    def OnSize(self, ev):
        self.size = self.GetSizeTuple()

    def Kill(self, event):
        # Make sure Pygame can't be asked to redraw /before/ quitting
        # by unbinding all methods which call the Redraw() method
        # (Otherwise wx seems to call Draw between quitting Pygame
        # and destroying the frame)
        self.Unbind(event=wx.EVT_PAINT, handler=self.OnPaint)
        self.Unbind(event=wx.EVT_TIMER, handler=self.Update, source=self.timer)
        pygame.quit()

    def Update(self, event):
        # loop = main_event_queue.handle_events()
        self.Redraw()

    def Redraw(self):
        if not self.stage.screen:
            return
        self.stage.update()

    def play(self):
        # if self.code_status == "undef":
        #  self.events.send('play')
        # else:
        # TODO(panda): warn about errors in the code
        #     pass
        self.stage.pause = False
        self.stage.reset()

    def stop(self):
        self.stage.pause = True
