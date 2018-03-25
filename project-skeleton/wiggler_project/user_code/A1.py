import pygame

from wiggler_project.engine.sprites import MovingSprite

class Sprite(MovingSprite):

    def __init__(self, resources, events, initdata, *group):
        self.custom_update = self.update_generator()
        super(Sprite, self).__init__(resources, events, initdata, *group)
        # let user add events subscriptions here
        if self.events_subs:
            events.subscribe(self, self.events_subs)

    def update_generator(self):
        yield

    def update(self):
        self.events_handler()
        try:
            next(self.custom_update)
        except StopIteration:
            pass
        super(Sprite, self).update()

    def events_handler(self):
        while self.events:
            event = self.events.pop()
