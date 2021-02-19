from gpanel import *
from Letters import getLetterImg

from Button import *

TEXT_OFFSET = 55
#TEXT_LEFT_START = 250

class TextInput:
    defaultImage = None
    defaultHoverImage = None
    all = []
    def __init__(self, hudPage, pos, val = None, maxLength = 7):
        self.hudPage = hudPage
        self.pos = pos
        self.active = False
        self.hovering = False
        self.letters = []
        self.max = maxLength
        self.setInput(val or "")

        self.imgWidth = TextInput.defaultImage.getWidth() - TextInput.defaultImage.getWidth() / 5 #- 30
        self.imgHeight = TextInput.defaultImage.getHeight() - TextInput.defaultImage.getHeight() / 5 #- 10

        TextInput.all.append(self)

    def getInput(self):
        return self.input

    def setInput(self, text):
        self.input = text

        self.offset = self.pos.x + 2

        for letter in text:
            letterImg = getLetterImg(letter, 50)
            self.letters.append([letterImg, self.offset])
            self.offset += letterImg.getWidth() - 10

    def appendInput(self, letter):
        if self.max <= len(self.input):
            Button.HOVER_SOUND.play()
            return
        self.input += letter
        print("new input: {}".format(self.input))
        letterImg = getLetterImg(letter, 50)
        print("letter img {}".format(letterImg))
        print("offset {}".format(self.offset))
        self.letters.append([letterImg, self.offset])
        self.offset += letterImg.getWidth() - 10

    def deleteLast(self):
        if len(self.input) < 1:
            Button.HOVER_SOUND.play()
            return
        self.input = self.input[:-1]
        [letterImg, offset] = self.letters.pop()
        self.offset -= letterImg.getWidth() - 10

    def draw(self, hud, mousePos):
        if self.hudPage != hud:
            return

        focused = self.focused(hud, mousePos)

        if focused:
            #print("hovering button")
            if not self.hovering and not Button.HOVER_SOUND is None:
                Button.HOVER_SOUND.play()

            self.hovering = True

            if not TextInput.defaultHoverImage is None:
                image(TextInput.defaultHoverImage, self.pos.x, self.pos.y)
            else:
                image(TextInput.defaultImage, self.pos.x, self.pos.y)
            
        else:
            self.hovering = False

            image(TextInput.defaultImage, self.pos.x, self.pos.y)

        for letter, offset in self.letters:
            image(letter, self.pos.x + offset, self.pos.y - 10)

    def focused(self, hud, mousePos):
        if self.hudPage != hud:
            return False

        maxMousePosY = self.pos.y - self.imgHeight
        maxMousePosX = self.pos.x + self.imgWidth

        # print("X Max {}".format(maxMousePosX))
        # print("Y Max {}".format(maxMousePosY))

        isInXRange = mousePos.x >= self.pos.x and mousePos.x <= maxMousePosX
        isInYRange = mousePos.y <= self.pos.y and mousePos.y >= maxMousePosY

        # print("In X Range {}".format(isInXRange))
        # print("In Y Range {}".format(isInYRange))

        #     x in range of button                                                    y in range of button
        return isInXRange and isInYRange

