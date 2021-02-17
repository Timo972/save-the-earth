from Letters import getNumImg
from gpanel import *
import time
import math

TOP_OFFSET = 50
LEFT_OFFSET = 40

timerPausedAt = 0
timerStartedAt = 0
timerEnabled = False
#survivedTime = 0

"""Sets the start point for endTimer()"""
def beginTimer():
    global timerStartedAt
    global timerEnabled
    timerStartedAt = time.clock() * 1000
    timerEnabled = True

"""Draws the time diff between beginTimer() and now in human readable format"""
def drawTimer():
    #global survivedTime
    if not timerEnabled:
        return

    survivedTime = endTimer(False)

    # print(survivedTime)

    days = math.floor(survivedTime / (1000 * 60 * 60 * 24))
    hours = math.floor((survivedTime % (1000 * 60 * 24)) / (1000 * 60 * 60))
    minutes = math.floor((survivedTime % (1000 * 60 * 60)) / (1000 * 60))
    seconds = math.floor((survivedTime % (1000 * 60)) / 1000)
    #miliseconds = math.floor((survivedTime % 1000) / 1000)

    #data = [days, hours, minutes, seconds, miliseconds]
    data = [days, hours, minutes, seconds]

    data = list(filter(lambda item: item > 0, data))

    amountToDraw = (len(data) * 3)  - 1

    leftOffset = 500 - LEFT_OFFSET * amountToDraw

    for idx, num in enumerate(data):
        if num == 0 and idx > 0:
            continue

        if idx > 0:
            image(getNumImg(10), leftOffset, TOP_OFFSET)
            leftOffset += LEFT_OFFSET

        if num > 9:
            for num_mem in str(num):
                if num_mem == '.':
                    return
                image(getNumImg(int(num_mem)), leftOffset, TOP_OFFSET)
                leftOffset += LEFT_OFFSET
        else:
            image(getNumImg(0), leftOffset, TOP_OFFSET)
            leftOffset += LEFT_OFFSET
            image(getNumImg(int(num)), leftOffset, TOP_OFFSET)
            leftOffset += LEFT_OFFSET

        

    #print(survivedTime)

"""Pauses the timer"""
def pauseTimer():
    global timerPausedAt
    if not timerEnabled:
        return
    timerPausedAt = time.clock() * 1000

"""Resumes the timer"""
def resumeTimer():
    global timerStartedAt
    global timerPausedAt 
    if not timerEnabled:
        return
    timerStartedAt = time.clock() * 1000 - (timerPausedAt - timerStartedAt)
    timerPausedAt = 0

"""Returns time differenz between beginTimer() and now in milliseconds"""
def endTimer(end = True):
    global timerEnabled

    if not timerEnabled:
        return 0

    now = time.clock() * 1000
    #print("timer running: {0} {1}".format(timerPausedAt == 0, timerPausedAt))

    timerDiff = 0

    if timerPausedAt > 0:
        timerDiff = timerPausedAt - timerStartedAt
    else:
        timerDiff = now - timerStartedAt

    if end:
        timerEnabled = True

    return timerDiff