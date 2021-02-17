from gpanel import *
import soundsystem

class Effect:
    # pos Vector2
    # image tigerjython image
    # sound tigerjython sound
    def __init__(self, pos = None, image = None, sound = None):
        self.pos = pos
        self.image = image
        self.sound = sound
        self.next = None
        if not image is None:
            if isinstance(self.image, list):
                self.next = 0
            else:
                self.next = self.image
        
    def play(self):
        if not self.sound is None:
            soundsystem.openStereoPlayer(self.sound, 44100)
            soundsystem.play()
    def draw(self):
        if not self.image is None and not self.pos is None and not self.next is None:
            if isinstance(self.next, int) and isinstance(self.image, list):
                image(self.image[self.next], self.pos.x, self.pos.y)
                self.next+=1
                if self.next >= len(self.image):
                    self.next = 0
            else:
                image(self.image, self.pos.x, self.pos.y)
    def setPos(self, pos):
        self.pos = pos
        