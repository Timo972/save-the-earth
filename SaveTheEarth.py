#from javax.swing import JFrame, JMenuBar, JMenu, JMenuItem, JTextField, ImageIcon, JButton
from java.lang import System
from gpanel import *
from random import *
from enum import Enum
import sys
import time
import platform

sys.path.insert(1, './src/util')
sys.path.insert(1, './src/classes')
sys.path.insert(1, './src/components')

# better sound api than soundsystem
#from javax.sound.sampled import AudioInputStream, AudioFormat, DataLine, AudioSystem, Clip
from java.applet.Applet import newAudioClip
from java import io

# eigene Klassen
from Vector2 import *

# Hud / Visual Items
from Button import *
from TextInput import *
from ScoreboardItem import *
from GameObject import *
from Effect import *

# functionen
from Timer import *
from Letters import hasLetter, loadAlphabet
from VectorMath import *
from File import *
import Update


DEBUG = False
PROD = True
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

ITEM_SPAWN_TIME = 15 # in seconds
ITEM_SIZE = 15

OBJECT_IMAGE = None
PLAYER_IMAGE = None
BACKGROUND_IMAGE = None
EXPLOSION_IMAGE = None
#BACKGROUND_IMAGE = None
ITEM_IMAGE = None
BUBBLE_IMAGE = None
PAUSE_IMAGE = None
STARTBTN_IMAGE = None
RESTARTBTN_IMAGE = None
SETTINGBTN_IMAGE = None
GLOBEBTN_IMAGE = None
BACKBTN_IMAGE = None
LOADING_IMAGE = getImage("images/loading.png")
GAMEOVER_IMAGE = None

BACKGROUND_SOUND = None
EXPLOSION_SOUND = None
ITEMCOLLECT_SOUND = None

EXPLOSION_EFFECT = None
ITEMCOLLECT_EFFECT = None
ITEMUSED_SOUND = None

HUD_CLICK_TIMEOUT = 0.3 # in seconds

ITEM_INVINCIBLE_TIME = 2 # in seconds

gameObjectList = []
effectList = []
playerObject = False
playerAblilities = []

lastAddedObject = 0
lastAddedItem = 0

mousePos = Vector2(0,0)
mouseDown = False
activeInput = None

scoreboardData = None
userNameInput = None

userName = None
isInvincible = 0
inGame = False
isPaused = False
# 0 is main menu 1 is settings 2 is scoreboard
class Hud(Enum):
    main = 0
    settings = 1
    scoreboard = 2
    gameover = 3

class Key(Enum):
    Back = 27
    Del = 8
    Enter = 10
    Space = 32

KEYCODES = {
    65: 'a',
    66: 'b',
    67: 'c',
    68: 'd',
    69: 'e',
    70: 'f',
    71: 'g',
    72: 'h',
    73: 'i',
    74: 'j',
    75: 'k',
    76: 'l',
    77: 'm',
    78: 'n',
    79: 'o',
    80: 'p',
    81: 'q',
    82: 'r',
    83: 's',
    84: 't',
    85: 'u',
    86: 'v',
    87: 'w',
    88: 'x',
    89: 'y',
    90: 'z',
}

hudPage = 0
justClicked = time.clock()


def loadSound(fileName):
    url = io.File(fileName).toURL()
    #print("loading sound {0}, url: {1}".format(fileName,url))
    audio = newAudioClip(url)
    #print("loaded sound {}".format(fileName))
    return audio

def init():
    global OBJECT_IMAGE
    global PLAYER_IMAGE
    global BACKGROUND_IMAGE
    global EXPLOSION_IMAGE
    #global BACKGROUND_IMAGE
    global ITEM_IMAGE
    global BUBBLE_IMAGE
    global PAUSE_IMAGE
    global LOADING_IMAGE
    global STARTBTN_IMAGE
    global GLOBEBTN_IMAGE
    global SETTINGBTN_IMAGE
    global BACKBTN_IMAGE
    global RESTARTBTN_IMAGE
    global GAMEOVER_IMAGE

    global BACKGROUND_SOUND
    global EXPLOSION_SOUND
    global ITEMCOLLECT_SOUND
    global ITEMUSED_SOUND

    global EXPLOSION_EFFECT
    global ITEMCOLLECT_EFFECT

    addStatusBar(STATUS_H)
    setStatusText("Lade {}...".format(TITLE))

    move(50,50)
    text("Lade {}...".format(TITLE))

    image(LOADING_IMAGE, -200, 700)

    repaint()

    OBJECT_IMAGE = getImage("images/komet.png")
    PLAYER_IMAGE = getImage("images/player_40.png")
    BACKGROUND_IMAGE = getImage("images/anotherbg.jpg")
    EXPLOSION_IMAGE = getImage("images/explosion.png")
    #BACKGROUND_IMAGE = getImage("images/bg.gif")
    ITEM_IMAGE = getImage("images/item.png")
    BUBBLE_IMAGE = getImage("images/bubble_small.png")
    STARTBTN_IMAGE = getImage("images/start-btn-small.png")
    GLOBEBTN_IMAGE = getImage("images/btn-globe.png")
    SETTINGBTN_IMAGE = getImage("images/btn-settings.png")
    BACKBTN_IMAGE = getImage("images/btn-back.png")
    PAUSE_IMAGE = getImage("images/pause.png")
    GAMEOVER_IMAGE = getImage("images/game-over.png")
    RESTARTBTN_IMAGE = getImage("images/restart-btn.png")

    ScoreboardItem.defaultImg = getImage("images/scoreboard-item.png")
    TextInput.defaultImage = getImage("images/scoreboard-item.png")

    
    
    #BACKGROUND_SOUND = soundsystem.getWavStereo("sounds/sound.WAV")
    #EXPLOSION_SOUND = soundsystem.getWavStereo("sounds/explosion.wav")
    #ITEMCOLLECT_SOUND = soundsystem.getWavStereo("sounds/itemcollect.WAV")
    BACKGROUND_SOUND = loadSound("sounds/sound.WAV")
    EXPLOSION_SOUND = loadSound("sounds/explosion.wav")
    ITEMCOLLECT_SOUND = loadSound("sounds/itemcollect.WAV")
    ITEMUSED_SOUND = loadSound("sounds/gotshot.WAV")

    Button.HOVER_SOUND = loadSound("sounds/hud_hover.wav")

    EXPLOSION_EFFECT = Effect(None, EXPLOSION_IMAGE, EXPLOSION_SOUND)
    ITEMCOLLECT_EFFECT = Effect(None, None, ITEMCOLLECT_SOUND)

    loadAlphabet()

    return True

def openScoreboard():
    global hudPage
    #global scoreboardData

    print("open scoreboard")

    if scoreboardData is None:
        ScoreboardItem(1, "Nibba#")
        ScoreboardItem(2, "Kek")
        ScoreboardItem(3, "Hs")
    else:

        try:
            sortedScoreboard = list(sorted(scoreboardData, key=lambda a: a["time"], reverse=True))
        except e:
            print("could not load scoreboard {}".format(e))
            return

        for idx, user in enumerate(sortedScoreboard):
            if idx > 7:
                break
            ScoreboardItem(idx+1, user["username"], user["time"])


    hudPage = Hud.scoreboard

def openSettings():
    global hudPage
    print("open settings")
    hudPage = Hud.settings

def openMain():
    global hudPage
    global userName
    print("open main")

    ScoreboardItem.all = []
    userName = userNameInput.getInput()

    print("username: {}".format(userName))
    setStatusText("Willkommen in {0}, dein Benutzername: {1}".format(TITLE, userName.upper()))

    hudPage = Hud.main

def startGame():
    global inGame
    global playerObject
    global gameObjectList
    global userName
    
    gameObjectList = []
    playerObject.pos = Vector2(250, 250)
    playerObject.valid = True

    setStatusText("{} gestartet".format(TITLE))
    inGame = True
    beginTimer()
    print("started game")

def main():
    global userNameInput
    global userName
    global scoreboardData
    #global inGame

    # window setup
    if PROD or STANDALONE:
        makeGPanel(TITLE, MIN_X, MAX_X, MIN_Y, MAX_Y, mouseDragged = mouseDrag, mouseMoved = mouseDrag, mousePressed = mousePressed, mouseReleased = mouseReleased, closeClicked=onExit)
    else:
        makeGPanel(TITLE, MIN_X, MAX_X, MIN_Y, MAX_Y, mouseDragged = mouseDrag, mouseMoved = mouseDrag, mousePressed = mousePressed, mouseReleased = mouseReleased)
    enableRepaint(False)
    window(0, MAX_X, MAX_Y, 0)

    # initialize -> load images and sounds
    init()

    if Update.check():
        Update.update()

    version = readJson("version.json")

    version = version if not version is None else "dev"

    settings = readJson("settings.json")

    userName = settings["username"] if not settings is None else "none"

    print("Running {0} version {1} with python version {2}".format(TITLE, version, platform.python_version()))

    scoreboardData = readJson("scoreboard.json") or []

    BACKGROUND_SOUND.play()
        
    # start the game
    generatePlayer()
    
    # create play button

    Button(Hud.main, STARTBTN_IMAGE, None, None, Vector2(250 - 60, 250 + 100), startGame)
    Button(Hud.main, SETTINGBTN_IMAGE, None, None, Vector2(450, 50), openSettings)
    Button(Hud.main, GLOBEBTN_IMAGE, None, None, Vector2(450, 100), openScoreboard)

    userNameInput = TextInput(Hud.settings, Vector2(60, 350), userName)

    Button(Hud.settings, BACKBTN_IMAGE, None, None, Vector2(450, 50), openMain)
    Button(Hud.scoreboard, BACKBTN_IMAGE, None, None, Vector2(450, 50), openMain)

    Button(Hud.gameover, RESTARTBTN_IMAGE, None, None, Vector2(250 - 80, 250 + 130), startGame)

    openMain()

    #inGame = True
    
def onExit():
    print("exiting")
    writeJson("settings.json", {
        "username": userName
    })
    writeJson("scoreboard.json", scoreboardData)
    System.exit(0)
    
def generatePlayer():
    global playerObject
    start = Vector2(MAX_X/2,MAX_Y/2)
    end = Vector2(0, 0)
    playerObject = GameObject(0, start, end, PLAYER_SIZE, PLAYER_COLOR, PLAYER_IMAGE)

def drawScreenEffect(effect, drawTime):
    effectList.append([effect, drawTime + time.clock()])

def diePlayer(gameObject):
    global hudPage
    global inGame
    global scoreboardData

    collisionPos = getMidPos(playerObject.pos, gameObject.pos)

    EXPLOSION_EFFECT.setPos(Vector2(collisionPos.x - 10, collisionPos.y + 10))
    drawScreenEffect(EXPLOSION_EFFECT, 1)
    EXPLOSION_EFFECT.play()
    playerObject.destroy()

    survivedTime = endTimer()

    filteredScores = list(filter(lambda x: x["username"] == userName, scoreboardData))

    if len(filteredScores) > 0:
        filteredScores[0]["time"] = survivedTime
    else:
        scoreboardData.append({
            "username": userName,
            "time": survivedTime
        })

    print(scoreboardData)

    hudPage = Hud.gameover
    inGame = False

    setStatusText("Die Erde wurde zerstoert, du hast {} Sekunden ueberlebt".format(survivedTime/1000))

def setInvincible(invincible):
    global isInvincible

    if invincible:
        isInvincible = time.clock()
    else:
        isInvincible = 0

def clearItemAffect(item):
    ITEMUSED_SOUND.play()
    for i, o in enumerate(playerAblilities):
        if o[0] == item:
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
    
    startSide = randint(0, 3)
    
    startX = 0
    startY = 0
    endX = 0
    endY = 0
    
    print("object generated at side: {}".format(startSide))
    
    if startSide <= 1:
        startX = MIN_X if startSide < 1 else MAX_X
        endX = MAX_X if startSide < 1 else MIN_X
        startY = randint(MIN_Y, MAX_Y)
        endY = randint(MIN_Y, MAX_Y)
    else:
        startY = MIN_Y if startSide > 2 else MAX_Y
        endY = MAX_Y if startSide > 2 else MIN_Y
        startX = randint(MIN_X, MAX_X)
        endX = randint(MIN_X, MAX_X)
    
    # TODO: randomize size between MAX_OBJECT_SIZE and MIN_OBJECT_SIZE
    size = 20
    
    colorIdx = randint(0, len(OBJECT_COLORS)) - 1
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
    itemEffect = randint(0, 1)

    randPos = Vector2(randint(MIN_X, MAX_X), randint(MIN_Y, MAX_X))
    itemObject = GameObject(2, randPos, None, ITEM_SIZE, "yellow", ITEM_IMAGE, True, False, itemEffect)

    gameObjectList.append(itemObject)
    
def drawPlayer():
    if mouseDown and playerObject.valid and not isPaused:
        angle = getAngle(mousePos, playerObject.pos)    
        playerObject.pos = getPositionInFront(playerObject.pos, PLAYER_SPEED, angle)
        
    # move(playerObject.pos.x, playerObject.pos.y)
    # setColor(PLAYER_COLOR)
    # fillCircle(PLAYER_SIZE)
    # image(PLAYER_IMAGE, playerObject.pos.x - 15, playerObject.pos.y + 15)
    playerObject.draw()

    if hasItemEffect(1):
        image(BUBBLE_IMAGE, playerObject.pos.x - 17, playerObject.pos.y + 17)

    if isInvincible and not playerObject.flickering:
        playerObject.setFlickering(True)
    elif not isInvincible and playerObject.flickering:
        playerObject.setFlickering(False)


def drawGameObjects():
    for obj in gameObjectList:
        if not obj.static and playerObject.valid and not isPaused:
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

        if not playerObject.valid:
            continue
        
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

def drawEffects():
    for i, effect in enumerate(effectList):
        if effect[1] > time.clock():
            effect[0].draw()
        else:
            del effectList[i]

def drawHud():
    for button in Button.all:
        button.draw(hudPage, mousePos)
    for tinput in TextInput.all:
        tinput.draw(hudPage, mousePos)
    if hudPage == Hud.scoreboard:
        for sbItem in ScoreboardItem.all:
            sbItem.draw()
    elif hudPage == Hud.gameover:
        image(GAMEOVER_IMAGE, 250 - 150, 250 + 70)

def checkAbilities():
    if isInvincible > 0 and isInvincible + ITEM_INVINCIBLE_TIME < time.clock():
        setInvincible(False)

    for ability in playerAblilities:
        if ability[1] + ability[2] < time.clock():
            clearItemAffect(ability[0])

def processHudMouseClick():
    global justClicked
    global activeInput
    if not activeInput is None:
        activeInput.active = False
        activeInput = None
    for button in Button.all:
        if button.focused(hudPage, mousePos) and justClicked + HUD_CLICK_TIMEOUT < time.clock():
            justClicked = time.clock()
            button.onClick()
            return
    for tinput in TextInput.all:
        if tinput.focused(hudPage, mousePos) and justClicked + HUD_CLICK_TIMEOUT < time.clock():
            justClicked = time.clock()
            activeInput = tinput
            tinput.active = True
            return

def processKeyboardHit():
    global hudPage
    global isPaused
    global activeInput
    
    if kbhit():

        key = getKeyCode()

        if not activeInput is None:

            if key == Key.Back or key == Key.Enter:
                activeInput.active = False
                activeInput = None
                return
            elif key == Key.Del:
                activeInput.deleteLast()
                return

            if not key in KEYCODES:
                return

            letter = KEYCODES[key]

            print("keyboard hit {} in input box".format(letter))

            if hasLetter(letter, 50):
                activeInput.appendInput(letter or '#')
            else:
                Button.HOVER_SOUND.play()

            return
        
        print("keyboard hit {}".format(key))

        if (key == Key.Back or key == Key.Del) and not inGame:
            # hudPage = Hud.main
            openMain()
        elif key == Key.Enter and not inGame:
            if hudPage == Hud.main:
                startGame()
        elif key == Key.Space and inGame:
            isPaused = not isPaused
            if isPaused:
                pauseTimer()
            else:
                resumeTimer()
            print("paused game: {}".format(isPaused))
        
def tick():
    clear()

    if playerObject.valid and inGame and not isPaused:
        checkAbilities()
        addGameObject()
        addItem()

    image(BACKGROUND_IMAGE, MIN_X, MAX_Y)

    if inGame:
        drawPlayer()
        drawGameObjects()
        drawEffects()
        drawTimer()
    else:
        drawHud()

    if isPaused:
        image(PAUSE_IMAGE, 250-60, 250+60)
        
    processKeyboardHit()

    repaint()

def mousePressed(x,y):
    global mousePos
    global mouseDown 
    mousePos = Vector2(x, y)
    mouseDown = True
    if not inGame:
        processHudMouseClick()
    
def mouseReleased(x,y):
    global mouseDown 
    mouseDown = False
  
def mouseDrag(x, y):
    global mousePos
    mousePos = Vector2(x, y)

main()

while True:
    delay(20)
    if isinstance(playerObject, GameObject):
        tick()