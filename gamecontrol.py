from pathlib import Path
from globalconstants import *
import scenecontrol as sc
import teamcontrol as tc

class GameController:
    def __init__(self) -> None:
        #create scenecontroller
        self.scontrol = sc.SceneController()

        #create teamcontroller
        self.tcontrol = tc.TeamController()

        self.state = GAME_MAINMENU
        return

    def setstate(self,state:str):
        if state in GAME_STATES:
            self.state = state
        else:
            raise Exception("Invalid game state")

    def makeScene(self,setactive:bool=True):
        Team1 = self.tcontrol.fetchteam(Path("./teams/Test_3.txt"))
        Team2 = self.tcontrol.fetchteam(Path("./teams/Test_1.txt"))
        self.scontrol.addscene([Team1,Team2],setactive=setactive)

    def getactivescene(self) -> sc.sm.Scene:
        return self.scontrol.activescene