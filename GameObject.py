from gpanel import *

class GameObject:
    # type int 0=player 1=object 2=item
    # start Vector2
    # end Vector2
    # size int
    # color str
    # static bool
    # pos Vector2
    def __init__(self, otype, start, end, size, color, image = None, static = False, flickering = False, data = None):
        self.type = otype
        self.size = size
        self.color = color
        self.start = start
        self.end = end
        self.static = static
        self.data = data
        self.flickering = flickering
        self.fickerState = True
        self.image = image
        print("created game object with pos: {0}, {1}".format(start.x,start.y))
        self.pos = start

    def setFlickering(self, enabled):
        self.flickering = enabled

    def draw(self):
        move(self.pos.x, self.pos.y)
        setColor(self.color)

        if not self.image is None:
            image(self.image, self.pos.x - self.size, self.pos.y + self.size)
        else:
            fillCircle(self.color)
    