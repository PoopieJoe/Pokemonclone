import sys
import pygame
import thorpy
import core
from globalconstants import *
#from pygame.locals import *

DEBUG = False

def main():
    pygame.init()
    game = core.CoreGame()
    application = thorpy.Application(**game.applicationargs)

    game.launch()

    application.quit()
    pygame.quit()


if __name__ == "__main__":
    if DEBUG:
        import cProfile
        cProfile.run('main()','profilestats.prof')
    else:
        main()
