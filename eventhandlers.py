import pygame
from globalconstants import *

def rounddmg(dmg:float) -> int:
    if (dmg > 0): #if any damage was dealt, min is 1
        dmg =  max(1,dmg)
    elif (dmg < 0): #if any health was healed, min is 1
        dmg =  min(-1,dmg)
    else:
        pass #don't do anything if total is exactly 0

    return int(dmg)

def continueaction():
    try:
        #this lterally does nothing why did I type this
        return True
    except Exception:
        return False
    