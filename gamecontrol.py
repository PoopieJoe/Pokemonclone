from __future__ import annotations
from pathlib import Path
from globalconstants import *
import scenecontrol as sc
import teamcontrol as tc

class GameController:
    "Object that manages the game state"
    def __init__(self) -> None:
        #create scenecontroller
        self.scontrol = sc.SceneController()

        #create teamcontroller
        self.tcontrol = tc.TeamController()

        self.setstate(GAMESTATES.START)
        return

    def setstate(self,state:str):
        if GAMESTATES.contains(state):
            self.state = state
            return True
        else:
            return False

    def makeScene(self,teams:list[sc.sm.c.Team],format:str,setactive:bool = True):
        self.scontrol.addscene(teams,format,setactive)

    def getactivescene(self) -> sc.sm.Scene:
        return self.scontrol.activescene