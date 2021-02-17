from gpanel import *

from Vector2 import *
from Letters import getLetterImg, getNumImg

ITEM_OFFSET = 78

class ScoreboardItem:
    all = []
    topOffset = 200
    defaultImg = None
    def __init__(self, rank, text):
        self.pos = Vector2(60, ScoreboardItem.topOffset if len(ScoreboardItem.all) == 0 else ScoreboardItem.topOffset + ITEM_OFFSET * len(ScoreboardItem.all))
        self.text = text
        self.rank = rank
        self.letters = []

        self.letters.append([getNumImg(rank), 10])
        letterOffset = 60

        for letter in text.lower():
            img = getLetterImg(letter, 50)
            self.letters.append([img, letterOffset])
            letterOffset += img.getWidth() - 10

        #self.imgWidth = self.image.getWidth() - self.image.getWidth() / 5 #- 30
        #self.imgHeight = self.image.getHeight() - self.image.getHeight() / 5 #- 10

        #ScoreboardItem.topOffset += ITEM_OFFSET
        ScoreboardItem.all.append(self)
    
    def draw(self):
        
        image(ScoreboardItem.defaultImg, self.pos.x, self.pos.y)
        for idx, [letter, offset] in enumerate(self.letters):
            image(letter, self.pos.x + offset, (self.pos.y - 10) if idx > 0 else (self.pos.y - 5))

        #if not self.text is None:
        #    move(self.pos.x, self.pos.y)
        #    text(self.text)

