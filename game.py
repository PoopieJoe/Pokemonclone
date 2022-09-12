import sys
import pygame
import thorpy
import core
from globalconstants import *

#from pygame.locals import *

pygame.init()

# SETUP

application = thorpy.Application((SCREENW,SCREENH), "Pokemonclone")

game = core.CoreGame()

game.launch()

application.quit()
pygame.quit()
