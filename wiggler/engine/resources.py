

class EngineManager():
        # pygame resources
        self.clock = None
        self.resolution = None
        self.cast = Cast(self)
        self.engine_events = None
        self.background = Background(self)

class Engine():

    def set_pygame_resources(self):
        self.resolution = self.conf['stage_resolution']
        sound_channels = self.conf['sound_channels']
        reserved_channels = self.conf['reserved_channels']
        self.sound_channels = SoundChannels(sound_channels, reserved_channels)
        self.clock = pygame.time.Clock()
        self.engine_events = EventQueue()

