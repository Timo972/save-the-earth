from java.lang import System
from gpanel import *
from random import *
import soundsystem
import time
import platform

from Vector2 import *
from GameObject import *
from VectorMath import *
from Effect import *

DEBUG = False
PROD = False
STANDALONE = True

MAX_X = 500
MIN_X = 0
MAX_Y = 500
MIN_Y = 0
STATUS_H = 50
TITLE = "Save the Earth"

PLAYER_COLOR = "blue"
PLAYER_SIZE = 15
PLAYER_SPEED = 3

MAX_OBJECT_SIZE = 3
MIN_OBJECT_SIZE = 0.5
OBJECT_COLORS = ["green"]
OBJECT_SPAWN_TIME = 5 # in seconds
OBJECT_SPEED = 1
OBJECT_SPEED_MULTIPLIER = 1.1

ITEM_SPAWN_TIME = 5 # in seconds
ITEM_SIZE = 15

OBJECT_IMAGE = None
PLAYER_IMAGE = None
BACKGROUND_IMAGE = None
EXPLOSION_IMAGE = None
#BACKGROUND_IMAGE = None
ITEM_IMAGE = None
BUBBLE_IMAGE = None

BACKGROUND_SOUND = None
EXPLOSION_SOUND = None
ITEMCOLLECT_SOUND = None

EXPLOSION_EFFECT = None
ITEMCOLLECT_EFFECT = None

ITEM_INVINCIBLE_TIME = 2 # in seconds

gameObjectList = []
playerObject = False
playerAblilities = []

lastAddedObject = 0
lastAddedItem = 0

mousePos = Vector2(0,0)
mouseDown = False

isInvincible = 0
inGame = True

def init():
    global OBJECT_IMAGE
    global PLAYER_IMAGE
    global BACKGROUND_IMAGE
    global EXPLOSION_IMAGE
    #global BACKGROUND_IMAGE
    global ITEM_IMAGE
    global BUBBLE_IMAGE

    global BACKGROUND_SOUND
    global EXPLOSION_SOUND
    global ITEMCOLLECT_SOUND

    global EXPLOSION_EFFECT
    global ITEMCOLLECT_EFFECT

    addStatusBar(STATUS_H)
    setStatusText("Lade {}...".format(TITLE))

    OBJECT_IMAGE = getImage("images/komet.png")
    PLAYER_IMAGE = getImage("images/player_40.png")
    BACKGROUND_IMAGE = getImage("images/anotherbg.jpg")
    EXPLOSION_IMAGE = getImage("images/explosion.png")
    #BACKGROUND_IMAGE = getImage("images/bg.gif")
    ITEM_IMAGE = getImage("images/item.png")
    BUBBLE_IMAGE = getImage("images/bubble_small.png")
    
    BACKGROUND_SOUND = soundsystem.getWavStereo("sounds/sound.WAV")
    EXPLOSION_SOUND = soundsystem.getWavStereo("sounds/explosion.wav")
    ITEMCOLLECT_SOUND = soundsystem.getWavStereo("sounds/itemcollect.WAV")

    EXPLOSION_EFFECT = Effect(None, EXPLOSION_IMAGE, EXPLOSION_SOUND)
    ITEMCOLLECT_EFFECT = Effect(None, None, ITEMCOLLECT_SOUND)
    
    preloadSounds()

    return True

def preloadSounds():
    # TODO: set Volume to 0 and play every sound one time that its loaded
    return

def main():
    print("executed main")
    print(platform.python_version())
    setStatusText("Willkommen in {}".format(TITLE))
    generatePlayer()
    if PROD:
        soundsystem.openStereoPlayer(BACKGROUND_SOUND, 44100)
        soundsystem.setVolume(600)
        soundsystem.playLoop()
    
def onExit():
    print("exiting")
    try:
        soundsystem.stop()
    except e:
        print("no sound played")
    System.exit(0)
    
def generatePlayer():
    global playerObject
    start = Vector2(MAX_X/2,MAX_Y/2)
    end = Vector2(0, 0)
    playerObject = GameObject(0, start, end, PLAYER_SIZE, PLAYER_COLOR)

def diePlayer(gameObject):
    global playerObject
    print("OnPlayerDie")
    collisionPos = getMidPos(playerObject.pos, gameObject.pos)
    EXPLOSION_EFFECT.setPos(Vector2(collisionPos.x - 10, collisionPos.y + 10))
    print("setted effect pos")
    EXPLOSION_EFFECT.draw()
    EXPLOSION_EFFECT.play()
    playerObject = False
    if PROD:
        if soundsystem.isPlayerValid() and soundsystem.isPlaying():
            soundsystem.stop()
    setStatusText("Die Erde wurde zerstoert")

def setInvincible(invincible):
    global isInvincible
    if invincible:
        isInvincible = time.clock()
    else:
        isInvincible = 0

def clearItemAffect(item):
    for i, o in enumerate(playerAblilities):
        if o[0] == item:
            print(playerAblilities[i])
            del playerAblilities[i]
            break

def hasItemEffect(item):
    for i, o in enumerate(playerAblilities):
        if o[0] == item:
            return True


def collectItem(gameObject):
    global gameObjectList
    global playerAblilities

    ITEMCOLLECT_EFFECT.play()

    if gameObject.data == 0:
        gameObjectList = []
    else:
        if hasItemEffect(gameObject.data):
            clearItemAffect(gameObject.data)
        playerAblilities.append([gameObject.data, 5, time.clock()])
        deleteGameObject(gameObject)

def generateObject():
    print("generateObject")
    
    startSide = randrange(0, 3)
    
    startX = 0
    startY = 0
    endX = 0
    endY = 0
    
    print("object generated at side: {}".format(startSide))
    
    if startSide <= 1:
        startX = MIN_X if startSide < 1 else MAX_X
        endX = MAX_X if startSide < 1 else MIN_X
        startY = randrange(MIN_Y, MAX_Y)
        endY = randrange(MIN_Y, MAX_Y)
    else:
        startY = MIN_Y if startSide > 2 else MAX_Y
        endY = MAX_Y if startSide > 2 else MIN_Y
        startX = randrange(MIN_X, MAX_X)
        endX = randrange(MIN_X, MAX_X)
    
    # TODO: randomize size between MAX_OBJECT_SIZE and MIN_OBJECT_SIZE
    size = 20
    
    colorIdx = randrange(0, len(OBJECT_COLORS))
    color = OBJECT_COLORS[colorIdx]

    start = Vector2(startX, startY)
    end = Vector2(endX, endY)
    
    gameObject = GameObject(1, start, end, size, color, OBJECT_IMAGE)    

    gameObjectList.append(gameObject)
    
def deleteGameObject(gameObj):
    print("remove game object")
    gameObjectList.remove(gameObj)
    
def addGameObject():
    global lastAddedObject
    if lastAddedObject + OBJECT_SPAWN_TIME > time.clock():
        return
    lastAddedObject = time.clock()
    generateObject()
    
def addItem():
    global lastAddedItem
    if lastAddedItem + ITEM_SPAWN_TIME > time.clock():
        return
    lastAddedItem = time.clock()
    randPos = Vector2(randrange(MIN_X, MAX_X), randrange(MIN_Y, MAX_X))
    itemObject = GameObject(2, randPos, None, ITEM_SIZE, "yellow", ITEM_IMAGE, True, False, 1)
    gameObjectList.append(itemObject)
    
def drawPlayer():
    if mouseDown:
        angle = getAngle(mousePos, playerObject.pos)    
        playerObject.pos = getPositionInFront(playerObject.pos, PLAYER_SPEED, angle)
        
    move(playerObject.pos.x, playerObject.pos.y)
    setColor(PLAYER_COLOR)
    fillCircle(PLAYER_SIZE)
    image(PLAYER_IMAGE, playerObject.pos.x - 15, playerObject.pos.y + 15)

    if hasItemEffect(1):
        image(BUBBLE_IMAGE, playerObject.pos.x - 17, playerObject.pos.y + 17)

    if isInvincible and not playerObject.flickering:
        playerObject.setFlickering(True)
    elif not isInvincible and playerObject.flickering:
        playerObject.setFlickering(False)


def drawGameObjects():
    for obj in gameObjectList:
        if not obj.static:
            angle = getAngle(obj.end, obj.pos)    
            obj.pos = getPositionInFront(obj.pos, OBJECT_SPEED, angle)
            
        #move(obj.pos.x, obj.pos.y)
        #setColor(obj.color)
        
        #if obj.type == 1:
        #    image(OBJECT_IMAGE, obj.pos.x - 20, obj.pos.y + 20)
        #elif obj.type == 2:
        #    fillCircle(obj.size)
        #    image(ITEM_IMAGE, obj.pos.x - 16, obj.pos.y + 16)
            
        obj.draw()

        if DEBUG:
            move(obj.end.x, obj.end.y)
            setColor(obj.color)
            fillCircle(obj.size)
        
        if distance(playerObject.pos, obj.pos) < playerObject.size + obj.size:
            if obj.type == 1:
                if hasItemEffect(1):
                    clearItemAffect(1)
                    setInvincible(True)
                elif not isInvincible:
                    diePlayer(obj)
                    break;
            elif obj.type == 2 and not obj.data is None:
                collectItem(obj)
            
        
        if obj.type == 1:
            distToEnd = distance(obj.pos, obj.end)
            
            if distToEnd < 1 + obj.size:
                deleteGameObject(obj)

def checkAbilities():
    if isInvincible > 0 and isInvincible + ITEM_INVINCIBLE_TIME < time.clock():
        setInvincible(False)

    for ability in playerAblilities:
        if ability[1] + ability[2] < time.clock():
            clearItemAffect(ability[0])
        
def tick():
    clear()
    checkAbilities()
    addGameObject()
    addItem()
    image(BACKGROUND_IMAGE, MIN_X, MAX_Y)
    #image(BACKGROUND_IMAGE, 0, 0)
    drawPlayer()
    drawGameObjects()
    repaint()


def mousePressed(x,y):
    global mousePos
    global mouseDown 
    mousePos = Vector2(x, y)
    mouseDown = True
    
def mouseReleased(x,y):
    global mouseDown 
    mouseDown = False
  
def mouseDrag(x, y):
    global mousePos
    mousePos = Vector2(x, y)

if PROD or STANDALONE:
    makeGPanel(TITLE, MIN_X, MAX_X, MIN_Y, MAX_Y, mouseDragged = mouseDrag, mousePressed = mousePressed, mouseReleased = mouseReleased, closeClicked=onExit)
else:
    makeGPanel(TITLE, MIN_X, MAX_X, MIN_Y, MAX_Y, mouseDragged = mouseDrag, mousePressed = mousePressed, mouseReleased = mouseReleased)
enableRepaint(False)
window(0, MAX_X, MAX_Y, 0)

init()

main()

while isinstance(playerObject, GameObject) and inGame:
    delay(20)
    tick()