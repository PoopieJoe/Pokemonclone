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

    def launch(self):
        self.gamecontrol = gc.GameController()
        self.gui = ui.GameGui(self.gamecontrol)
        self.gui.launchmenu(self.gui.mainmenu)

    # def startMenu(self):
    #     # Start menu
    #     thorpy.style.FONT_SIZE = 48

    #     Team1 = timport.importteam(Path("./teams/Test_3.txt"))
    #     Team2 = timport.importteam(Path("./teams/Test_1.txt"))
    #     tmpbeasts = Team1.beasts + Team2.beasts
    #     self.startbutton = thorpy.make_button("Battle",func=self.startScene,params={"beasts":tmpbeasts})
    #     self.startbutton.set_painter(ui.menubutton_painter)
    #     self.startbutton.finish()

    #     self.teamsbutton = thorpy.make_button("Teams")
    #     self.teamsbutton.set_painter(ui.menubutton_painter)
    #     self.teamsbutton.set_pressed_state()
    #     self.teamsbutton.finish()

    #     self.quitbutton = thorpy.make_button("Quit",func=thorpy.functions.quit_func)
    #     self.quitbutton.set_painter(ui.menubutton_painter)
    #     self.quitbutton.finish()

    #     self.mainmenubar = thorpy.Ghost([self.startbutton,self.teamsbutton,self.quitbutton])
    #     thorpy.store(self.mainmenubar,mode="v")
    #     self.mainmenubar.set_center((SCREENW/6,SCREENH*8/16))

    #     # Other buttons
    #     thorpy.style.FONT_SIZE = 18

    #     self.mainmenu = thorpy.Background(elements=[self.mainmenubar],
    #                                         image=pygame.image.load(SCENEBG))



        # self.reac_time = thorpy.ConstantReaction(thorpy.constants.THORPY_EVENT, self.tick_game,
        #                     {"id":thorpy.constants.EVENT_TIME})
        # self.gui.add_reaction(self.reac_time)


    # def startScene(self,beasts,setactive = True):
    #     newscene = smanage.Scene()
    #     for n,beast in enumerate(beasts):
    #         if n >= len(beasts): team = 1
    #         else: team = 0
    #         newscene.addBeast(beast,team)
    #     newscene.setupBattle()
    #     self.scenes.append(newscene)
    #     if setactive:
    #         self.activescene = self.scenes[-1]
    #         self.state = GAME_SCENE
    #     self.tick_scenes([self.activescene]) #tick scene to proc ui
    #     return

    # def tick_game(self):
    #     self.ms = pygame.time.get_ticks()
    #     dt = self.clock.tick()

    #     self.tick_scenes()
    #     print("time: " + str(self.ms))

    # def tick_scenes(self,scenes=None):
    #     #tick scenes
    #     if scenes == None:
    #         scenes = self.scenes

    #     for scene in scenes:
    #         #check for raised event flags and sort flags
    #         if (scene.noflags()):
    #             scene.fetchFlags()
    #         scene.popflag()

    #         #change gamestate according to state
    #         if (scene.state == SCENE_EXECUTEATTACK):
    #             if (scene.active_slot.beast.selected_attack.atk != None):
    #                 scene.processattack()
    #             else:
    #                 scene.attackDone()
    #         elif (len(scene.raisedFlags) == 0 and scene.state == SCENE_IDLE):
    #             scene.tick()

    #     # build active scene ui depending on state
    #     if self.activescene:
    #         if (self.activescene.state == SCENE_IDLE):
    #             pass
    #         elif (self.activescene.state == SCENE_CHOOSEATTACK):
    #             # fetch active beast from the active scene
    #             activebeast = self.activescene.active_slot.beast

    #             # generate movebuttons
    #             self.movebuttons = [thorpy.make_button(atk.name,activebeast.selectattack,params={"atk":atk}) for atk in activebeast.attacks]
    #             [but.set_painter(ui.choicebutton_painter) for but in self.movebuttons]
    #             [but.finish() for but in self.movebuttons]
    #             self.movebutcols = [thorpy.make_group(self.movebuttons[col*ui.CHOICEBUTTONSPERCOL:(col+1)*ui.CHOICEBUTTONSPERCOL-1],mode="v") for col in range(math.ceil(len(self.movebuttons)/ui.CHOICEBUTTONSPERCOL))]
    #             self.movebutsgroup = thorpy.make_group(self.movebutcols,mode="h")
    #             self.movebuttonbox = thorpy.Box([self.movebutsgroup],size=(ui.CHOICEBUTTONBOXW,ui.CHOICEBUTTONBOXH))
    #             self.movebuttonbox.set_painter(ui.big_textbox_painter)
    #             self.movebuttonbox.finish()


    #         elif (self.activescene.state == SCENE_CHOOSETARGET):
    #             # fetch active beast from the active scene
    #             activeslot = self.activescene.active_slot
    #             activebeast = activeslot.beast

    #             # Textbox with beast stats/state
    #             self.beasttitle = thorpy.make_text(activebeast.nickname)
    #             self.beasttitle.set_center((SCREENW*0.5,SCREENH-ui.CHOICEBUTTONBOXH-self.beasttitle.get_rect().h/2))

    #             # generate targetbuttons
    #             validtargets = self.activescene.slots.copy()
    #             for flagname in [flag["name"] for flag in activebeast.getselectedattack().flags]:
    #                 if flagname == TARGETOTHER: #effect on 1 other (friendly or enemy)
    #                     validtargets.remove(activeslot)
    #                 elif flagname == TARGETTEAM: #effect on team (friendly or enemy)
    #                     #valid_targets.remove(beastslot)
    #                     # if beastslot == 0 or beastslot == 2:
    #                     #     valid_targets.remove(beastslot + 1)
    #                     # else:
    #                     #     valid_targets.remove(beastslot - 1)
    #                     pass
    #                 elif flagname == TARGETALLOTHER: #effect on all others
    #                     raise Exception("Not implemented: " + TARGETALLOTHER)
    #                 elif flagname == TARGETSELF: #effect on self
    #                     raise Exception("Not implemented: " + TARGETSELF)
    #                 elif flagname == TARGETANY: #effect on any one character (including self)
    #                     pass
    #                 elif flagname == TARGETNONE: #no target (e.g. only set field conditions such as weather or terrain)
    #                     raise Exception("Not implemented: " + TARGETNONE)
                
    #             for slot in self.activescene.slots:
    #                 if (not slot.beast.isalive):
    #                     validtargets.remove(slot) #remove dead things

    #             self.targetbuttons = [thorpy.make_button(target.name,activebeast.selecttarget,params={"scene":self.activescene,"slot":target}) for target in validtargets]
    #             [but.set_painter(ui.choicebutton_painter) for but in self.targetbuttons]
    #             [but.finish() for but in self.targetbuttons]
    #             self.targetbutcols = [thorpy.make_group(self.targetbuttons[col*ui.CHOICEBUTTONSPERCOL:(col+1)*ui.CHOICEBUTTONSPERCOL-1],mode="v") for col in range(math.ceil(len(self.targetbuttons)/ui.CHOICEBUTTONSPERCOL))]
    #             self.targetbutsgroup = thorpy.make_group(self.targetbutcols,mode="h")
    #             self.targetbuttonbox = thorpy.Box([self.targetbutsgroup],size=(ui.CHOICEBUTTONBOXW,ui.CHOICEBUTTONBOXH))
    #             self.targetbuttonbox.set_painter(ui.big_textbox_painter)
    #             self.targetbuttonbox.finish()

    #         elif (self.activescene.state == SCENE_EXECUTEATTACK):
    #             pass
    #             if (self.activescene.attackresult):
    #                 pass
    #         else:
    #             pass #just black screen?
            
    #         # statuspanel
    #         self.statuspanel = ui.getstatuspanel(activebeast)
    #         self.statuspanel.finish()

    #         # complete bottompanel
    #         self.bottompanel = thorpy.Ghost(elements=[self.movebuttonbox,self.statuspanel])
    #         thorpy.store(self.bottompanel,mode="h",margin=0)
    #         self.bottompanel.fit_children()
            
    #         self.bottompanel.set_center((SCREENW*0.5,SCREENH-ui.CHOICEBUTTONBOXH/2))

    #         self.gui = thorpy.Background(   elements=[self.bottompanel],
    #                                         image=pygame.image.load(SCENEBG))

    #         menu = thorpy.Menu(self.gui,fps=FPS)
    #         menu.play()
