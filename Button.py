from gpanel import *

class Button:
    all = []
    def __init__(self, image, text, pos, onClick):
        self.image = image
        self.pos = pos
        self.enabled = False
        self.onClick = onClick
        self.text = text
        Button.all.append(self)
    
    def draw(self):
        self.enabled = True
        
        if not self.text is None:
            move(self.pos.x, self.pos.y)
            text(self.text)

        image(self.image, self.pos.x, self.pos.y)

        # DEBUG

        # move(self.pos.x, self.pos.y)
        # setColor("green")
        # fillCircle(5)

        # imgWidth = self.image.getWidth() - 30
        # imgHeight = self.image.getHeight() - 10
# 
        # maxMousePosY = self.pos.y - imgHeight
        # maxMousePosX = self.pos.x + imgWidth
# 
        # move(self.pos.x, maxMousePosY)
        # setColor("green")
        # fillCircle(5)
# 
        # move(maxMousePosX, self.pos.y)
        # setColor("green")
        # fillCircle(5)

    def disable(self):
        self.enabled = False

    def focused(self, mousePos):
        if not self.enabled:
            return False

        imgWidth = self.image.getWidth()
        imgHeight = self.image.getHeight()

        maxMousePosY = self.pos.y - imgHeight
        maxMousePosX = self.pos.x + imgWidth

        print("X Max {}".format(maxMousePosX))
        print("Y Max {}".format(maxMousePosY))

        isInXRange = mousePos.x >= self.pos.x and mousePos.x <= maxMousePosX
        isInYRange = mousePos.y <= self.pos.y and mousePos.y >= maxMousePosY

        print("In X Range {}".format(isInXRange))
        print("In Y Range {}".format(isInYRange))

        #     x in range of button                                                    y in range of button
        return isInXRange and isInYRange

