import pygame

from stage import Stage
from multiprocessing.connection import Client


class Configuration(object):

    def __init__(self):
        self.size = (700, 500)
        self.max_fps = 25

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

pygame.init()
conf = Configuration()
# Set the width and height of the screen [width, height]
# This should be a parameter
screen = pygame.display.set_mode(conf.size)

pygame.display.set_caption("My Game")

# Loop until the user clicks the close button.
done = False

# Used to manage how fast the screen updates
clock = pygame.time.Clock()

address = ('localhost', 6000)
print "bc"
#conn = Client(address, authkey='secret password')
conn = None
print "ac"
#conn.send('close')

# Two clock spins needed for better calibration of timings.
clock.tick(conf.max_fps)
clock.tick(conf.max_fps)


resources = ResourceManager()
events = EventQueue()
stage = Stage()
# -------- Main Program Loop -----------

while events.update():
    # --- Main event loop
    # conn object should not be available to the general code
    # recv unpickles data automatically an can unpikle malicious objects.
    # maybe create another thread layer for communication with outside ?
    if conn is not None:
        if conn.poll():
            print "poll returned"
            try:
                msg = conn.recv()
                event = pygame.event.Event(msg[0],msg[1])
                print event
                pygame.event.post(event)
            except EOFError:
                print "EOF"
                pass

    stage.update()


if conn is not None:
    conn.close()
screen.fill(BLACK)
pygame.display.flip()
# Close the window and quit.
pygame.quit()
