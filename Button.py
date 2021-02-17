from gpanel import *

class Button:
    all = []
    HOVER_SOUND = None
    def __init__(self, hudPage, image, hoverImage, text, pos, onClick):
        self.hudPage = hudPage
        self.image = image
        self.hoverImage = hoverImage
        self.pos = pos
        self.onClick = onClick
        self.text = text
        self.hovering = False

        self.imgWidth = self.image.getWidth() - self.image.getWidth() / 5 #- 30
        self.imgHeight = self.image.getHeight() - self.image.getHeight() / 5 #- 10

        Button.all.append(self)
    
    def draw(self, hud, mousePos):
        if self.hudPage != hud:
            return
        
        if not self.text is None:
            move(self.pos.x, self.pos.y)
            text(self.text)

        #print("mouse: x: {0} y: {1}".format(mousePos.x, mousePos.y))

        focused = self.focused(hud, mousePos)

        if focused:
            #print("hovering button")
            if not self.hovering and not Button.HOVER_SOUND is None:
                Button.HOVER_SOUND.play()

            self.hovering = True

            if not self.hoverImage is None:
                image(self.hoverImage, self.pos.x, self.pos.y)
            else:
                image(self.image, self.pos.x, self.pos.y)
            
        else:
            self.hovering = False

            image(self.image, self.pos.x, self.pos.y)

        # DEBUG

        # move(self.pos.x, self.pos.y)
        # setColor("green")
        # fillCircle(5)
# 
        # maxMousePosY = self.pos.y - self.imgHeight
        # maxMousePosX = self.pos.x + self.imgWidth
# 
        # move(self.pos.x, maxMousePosY)
        # setColor("green")
        # fillCircle(5)
# 
        # move(maxMousePosX, self.pos.y)
        # setColor("green")
        # fillCircle(5)

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

