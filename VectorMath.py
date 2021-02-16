from math import *
from Vector2 import *

def distance(pos1, pos2):
    return sqrt(pow(pos1.x-pos2.x, 2) + pow(pos1.y-pos2.y, 2))

def getAngle(pos1, pos2):
    x = pos1.x - pos2.x
    y = pos1.y - pos2.y
    
    angle = atan2(y, x) # angle in radians
    return angle;
    
def getPositionInFront(pos, dist, angle):
    xx = pos.x + (dist * cos(angle))
    yy = pos.y + (dist * sin(angle))    
    
    return Vector2(xx, yy)

def getMidPos(pos1, pos2):
    return Vector2((pos1.x + pos2.x) / 2, (pos1.y + pos2.y) / 2)