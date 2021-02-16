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
        
    def play(self):
        if not self.sound is None:
            soundsystem.openStereoPlayer(self.sound, 44100)
            soundsystem.play()
    def draw(self):
        if not self.image is None and not self.pos is None:
            image(self.image, self.pos.x, self.pos.y)
    def setPos(self, pos):
        self.pos = pos
        