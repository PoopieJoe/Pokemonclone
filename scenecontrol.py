from globalconstants import *
import scenemanager as sm

class SceneController:
    def __init__(self):
        self.scenes = []
        self.activescene = None
    
    def addscene(self,teams,setactive = True):
        newscene = sm.Scene()
        tmpbeasts = []
        for team in teams:
            for beast in team.beasts:
                tmpbeasts.append(beast)

        for n,beast in enumerate(tmpbeasts):
            newscene.addBeast(beast=beast,team=n)
        newscene.setupBattle()
        self.scenes.append(newscene)
        if setactive:
            self.activescene = self.scenes[-1]

    def removescene(self,scene):
        if type(scene) is sm.Scene:
            self.scenes.remove(scene)
        elif type(scene) is int:
            self.scenes.pop(scene)
        else:
            raise TypeError(type(scene) + " is not a valid type")

    def runscenes(self,scenes=None):
        if scenes == None:
            scenes = self.scenes

        for scene in scenes:
            scene.run()

    def runactivescene(self):
        self.runscenes([self.activescene])