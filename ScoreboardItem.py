from gpanel import *
import math

from Vector2 import *
from Letters import getLetterImg, getNumImg

ITEM_OFFSET = 78
TIME_OFFSET = 42

class ScoreboardItem:
    all = []
    topOffset = 200
    defaultImg = None
    def __init__(self, rank, text, time):
        self.pos = Vector2(60, ScoreboardItem.topOffset if len(ScoreboardItem.all) == 0 else ScoreboardItem.topOffset + ITEM_OFFSET * len(ScoreboardItem.all))
        self.text = text
        self.rank = rank
        self.letters = []
        self.timeLetters = []

        self.letters.append([getNumImg(rank), 10])
        letterOffset = 60

        for letter in text.lower():
            img = getLetterImg(letter, 50)
            self.letters.append([img, letterOffset])
            letterOffset += img.getWidth() - 10

        print("formatting scoreboard item time")

        days = math.floor(time / (1000 * 60 * 60 * 24))
        hours = math.floor((time % (1000 * 60 * 24)) / (1000 * 60 * 60))
        minutes = math.floor((time % (1000 * 60 * 60)) / (1000 * 60))
        seconds = math.floor((time % (1000 * 60)) / 1000)

        data = [days, hours, minutes, seconds]

        print(data)

        #data = list(filter(lambda item: item > 0, data))

        dataFilteredForZero = filter(lambda item: item > 0, data)

        amountToDraw = (len(dataFilteredForZero) * 3)  - 1

        timeOffset = 245 - TIME_OFFSET * amountToDraw

        print("calculated timeOffset")

        if len(dataFilteredForZero) == 0:
            self.timeLetters.append([getNumImg(0), timeOffset])
            self.timeLetters.append([getLetterImg('s', 50), timeOffset+TIME_OFFSET])
        else:
            for idx, num in enumerate(data):
                print("Score time: idx: {0}, time: {1}".format(idx, num))
                if num == 0:
                    continue
                
                print("calc time")
        
                # if idx > 0:
                #     self.timeLetters.append([getNumImg(10), timeOffset])
                #     timeOffset += TIME_OFFSET

                if num > 9:
                    print("more than one num")
                    for num_mem in str(num):
                        if num_mem == '.':
                            continue
                        self.timeLetters.append([getNumImg(int(num_mem)), timeOffset])
                        timeOffset += TIME_OFFSET
                else:
                    self.timeLetters.append([getNumImg(int(num)), timeOffset])
                    timeOffset += TIME_OFFSET

                timeLabelLetter = 'd' if idx == 0 else ('h' if idx == 1 else ('m' if idx == 2 else 's'))
                timeLabel = getLetterImg(timeLabelLetter, 50)

                if timeLabel is None:
                    print("could not get label for idx: {0}, letter: {1}".format(idx, timeLabelLetter))
                    timeLabel = getLetterImg('#', 50)

                self.timeLetters.append([timeLabel, timeOffset])
                timeOffset += TIME_OFFSET

        print("formatted scoreboard item time")

        #self.imgWidth = self.image.getWidth() - self.image.getWidth() / 5 #- 30
        #self.imgHeight = self.image.getHeight() - self.image.getHeight() / 5 #- 10

        #ScoreboardItem.topOffset += ITEM_OFFSET
        ScoreboardItem.all.append(self)
    
    def draw(self):
        
        image(ScoreboardItem.defaultImg, self.pos.x, self.pos.y)
        for idx, [letter, offset] in enumerate(self.letters):
            image(letter, self.pos.x + offset, (self.pos.y - 10) if idx > 0 else (self.pos.y - 5))

        for letter, offset in self.timeLetters:
            if letter is None:
                print("Could not draw scoreboard item {} correctly".format(self.text))
                continue
            image(letter, self.pos.x + offset, self.pos.y -5)

        #if not self.text is None:
        #    move(self.pos.x, self.pos.y)
        #    text(self.text)

