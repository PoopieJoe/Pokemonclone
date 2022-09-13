from pathlib import Path
import pygame
import gamecontrol as gc
import ui
from globalconstants import *

class CoreGame:
    def __init__(
        self
    ):
        self.clock = pygame.time.Clock()
        self.ms = pygame.time.get_ticks()
        self.scenes = []
        self.activescene = None
        self.applicationargs = {"size":(SCREENW,SCREENH), "caption":WINDOWNAME}

    def launch(self):
        self.gamecontrol = gc.GameController()
        self.gui = ui.GameGui(self.gamecontrol)
        self.gui.launchmenu(self.gui.mainmenu)