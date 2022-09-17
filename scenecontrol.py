from __future__ import annotations
from globalconstants import *
import scenemanager as sm

class SceneController:
    "High level controller that can create, destroy and run scenes"
    scenes:list[sm.Scene]
    def __init__(self):
        self.scenes = []
        self.activescene = None
    
    def addscene(self,teams:list[sm.c.Team],format:str,setactive:bool = True):
        """ Creates a new Scene object and adds it to the scene list \n
            teams:list[Team]        : a list of teams that are initiated in the scene. Number of teams, and which team slot they get depends on "format" \n
            format:str              : battle format \n
            setactive:bool = True   : Immediately set the created scene as the active scene \n"""
        newscene = sm.Scene(format,teams)
        newscene.setupBattle()
        self.scenes.append(newscene)
        if setactive:
            self.setactivescene(self.scenes[-1])

    def endactivescene(self):
        self.endscene(self.activescene)

    def endscene(self,scene:sm.Scene):
        """ Removes the scene from the list. If selected scene is the active scene, active scene will be cleared\n
            scene:sm.Scene  : Scene to be removed
        """
        if scene == self.activescene:
            self.setactivescene(None)
        self.scenes.remove(scene)


    def runscenes(self,scenes:list[sm.Scene]=None):
        """ Runs all scenes in the list one cycle. If None, all scenes will run\n
            scenes:list[sm.Scene]=None  : Scenes to be run
        """
        if scenes == None:
            scenes = self.scenes

        for scene in scenes:
            scene.run()

    def setactivescene(self,scene:sm.Scene):
        self.activescene = scene

    def getactivescene(self):
        return self.activescene

    def runactivescene(self):
        self.runscenes([self.activescene])