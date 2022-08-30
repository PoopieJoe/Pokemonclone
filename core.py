
from time import sleep
from pathlib import Path
import math
import pygame
import thorpy
import classes as c
import scenemanager as smanage
import ui
from globalconstants import *
import teamimport as timport
thorpy.VarSet
class CoreGame:
    def __init__(
        self
    ):
        self.clock = pygame.time.Clock()
        self.ms = pygame.time.get_ticks()
        self.state = GAME_START
        self.scenes = []
        self.activescene = None
        self.startMenu()


    def startMenu(self):
        # Start menu
        thorpy.style.FONT_SIZE = 48

        Team1 = timport.importteam(Path("./teams/Test_3.txt"))
        Team2 = timport.importteam(Path("./teams/Test_1.txt"))
        tmpbeasts = Team1.beasts + Team2.beasts
        self.startbutton = thorpy.make_button("Battle",func=self.startScene,params={"beasts":tmpbeasts})
        self.startbutton.set_painter(ui.menubutton_painter)
        self.startbutton.finish()

        self.teamsbutton = thorpy.make_button("Teams")
        self.teamsbutton.set_painter(ui.menubutton_painter)
        self.teamsbutton.set_pressed_state()
        self.teamsbutton.finish()

        self.quitbutton = thorpy.make_button("Quit",func=thorpy.functions.quit_func)
        self.quitbutton.set_painter(ui.menubutton_painter)
        self.quitbutton.finish()

        self.mainmenubar = thorpy.Ghost([self.startbutton,self.teamsbutton,self.quitbutton])
        thorpy.store(self.mainmenubar,mode="v")
        self.mainmenubar.set_center((SCREENW/6,SCREENH*8/16))

        # Other buttons
        thorpy.style.FONT_SIZE = 18

        self.gui = thorpy.Background(elements=[self.mainmenubar],
                                            image=pygame.image.load(SCENEBG))



        # self.reac_time = thorpy.ConstantReaction(thorpy.constants.THORPY_EVENT, self.tick_game,
        #                     {"id":thorpy.constants.EVENT_TIME})
        # self.gui.add_reaction(self.reac_time)


    def startScene(self,beasts,setactive = True):
        newscene = smanage.Scene()
        for n,beast in enumerate(beasts):
            if n >= len(beasts): team = 1
            else: team = 0
            newscene.addBeast(beast,team)
        newscene.setupBattle()
        self.scenes.append(newscene)
        if setactive:
            self.activescene = self.scenes[-1]
            self.state = GAME_SCENE
        self.tick_scenes([self.activescene]) #tick scene to proc ui
        return

    def tick_game(self):
        self.ms = pygame.time.get_ticks()
        dt = self.clock.tick()

        self.tick_scenes()
        print("time: " + str(self.ms))

    def tick_scenes(self,scenes=None):
        #tick scenes
        if scenes == None:
            scenes = self.scenes

        for scene in scenes:
            #check for raised event flags and sort flags
            if (scene.noflags()):
                scene.fetchFlags()
            scene.popflag()

            #change gamestate according to state
            if (scene.state == SCENE_EXECUTEATTACK):
                if (scene.active_slot.beast.selected_attack.atk != None):
                    scene.processattack()
                else:
                    scene.attackDone()
            elif (len(scene.raisedFlags) == 0 and scene.state == SCENE_IDLE):
                scene.tick()

        # build active scene ui depending on state
        if self.activescene:
            if (self.activescene.state == SCENE_IDLE):
                pass
            elif (self.activescene.state == SCENE_CHOOSEATTACK):
                # fetch active beast from the active scene
                activebeast = self.activescene.active_slot.beast

                # Textbox with beast stats/state
                self.beasttitle = thorpy.make_text(activebeast.nickname)
                self.beasttitle.set_center((SCREENW*0.5,SCREENH-ui.CHOICEBUTTONBOXH-self.beasttitle.get_rect().h/2))

                # generate movebuttons
                self.movebuttons = [thorpy.make_button(atk.name,activebeast.selectattack,params={"atk":atk}) for atk in activebeast.attacks]
                [but.set_painter(ui.choicebutton_painter) for but in self.movebuttons]
                [but.finish() for but in self.movebuttons]
                self.movebutcols = [thorpy.make_group(self.movebuttons[col*ui.CHOICEBUTTONSPERCOL:(col+1)*ui.CHOICEBUTTONSPERCOL-1],mode="v") for col in range(math.ceil(len(self.movebuttons)/ui.CHOICEBUTTONSPERCOL))]
                self.movebutsgroup = thorpy.make_group(self.movebutcols,mode="h")
                self.movebuttonbox = thorpy.Box([self.movebutsgroup],size=(ui.CHOICEBUTTONBOXW,ui.CHOICEBUTTONBOXH))
                self.movebuttonbox.set_painter(ui.big_textbox_painter)
                self.movebuttonbox.finish()
                # thorpy.store(self.movebuttonbox,mode="v",margin=0,align="right")

                # statuspanel
                self.statustext = thorpy.make_text(text=ui.getStatusText(activebeast),font_size=40,font_color=(0,0,0))
                self.statuspanel = thorpy.Box(elements=[self.statustext],size=(ui.STATUSPANELW,ui.STATUSPANELH))
                self.statuspanel.set_painter(ui.big_textbox_painter)
                self.statuspanel.finish()

                # complete bottompanel
                self.bottompanel = thorpy.Box(elements=[self.movebuttonbox,self.statuspanel],size=(ui.BOTTOMPANELW,ui.BOTTOMPANELH))
                self.bottompanel.set_painter(ui.big_textbox_painter)
                self.bottompanel.finish()

                thorpy.store(self.bottompanel,mode="h")
                
                self.bottompanel.set_center((SCREENW*0.5,SCREENH-ui.CHOICEBUTTONBOXH/2))
                self.statuspanel.set_topleft((0,0))

                self.gui = thorpy.Background(   elements=[self.beasttitle,self.bottompanel],
                                                image=pygame.image.load(SCENEBG))

                menu = thorpy.Menu(self.gui,fps=FPS)
                menu.play()
            elif (self.activescene.state == SCENE_CHOOSETARGET):
                pass
            elif (self.activescene.state == SCENE_EXECUTEATTACK):
                pass
                if (self.activescene.attackresult):
                    pass
            else:
                pass #just black screen?
