from gpanel import *

LETTER_ARR = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
LETTERS = {}
NUMBER_IMAGES = None
QUEST_IMAGE = None

def loadAlphabet():
    global QUEST_IMAGE
    global LETTERS
    global NUMBER_IMAGES

    QUEST_IMAGE = getImage("images/letter_quest.png")

    for size in [50]:
        LETTERS[size] = {}
        for letter in LETTER_ARR:
            LETTERS[size][letter] = getImage("images/letter_{letter}_{size}.png".format(letter=letter, size=size))

    NUMBER_IMAGES = []
    for i in range(10):
        img = getImage("images/number_{}.png".format(i))
        NUMBER_IMAGES.append(img)
    NUMBER_IMAGES.append(getImage("images/dp.png"))
    

def getLetterImg(letter, size):
    if not size in LETTERS or not letter in LETTERS[size]:
        return QUEST_IMAGE
    else:
        return LETTERS[size][letter]

def hasLetter(letter, size):
    return size in LETTERS and letter in LETTERS[size]

def getNumImg(num):
    if num >= len(NUMBER_IMAGES):
        return QUEST_IMAGE
    else:
        return NUMBER_IMAGES[num]