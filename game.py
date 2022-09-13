import sys
import pygame
import thorpy
import core
from globalconstants import *

#from pygame.locals import *

pygame.init()

# SETUP

game = core.CoreGame()

application = thorpy.Application(**game.applicationargs)

game.launch()

application.quit()
pygame.quit()
