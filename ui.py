from __future__ import annotations
import pygame
import thorpy
from pygame.locals import *
from math import floor,ceil
from globalconstants import *
from uiElements import *
import classes as c
import scenemanager as sm
import gamecontrol as gc
import misc

pygame.init()

# Thorpy styling
class UICONSTANTS(CONSTOBJ):
    def __init__(self) -> None:
        super().__init__()
        self.BOTTOMPANELW = SCREENW*0.8
        self.BOTTOMPANELH = SCREENH*0.33
        self.STATUSPANELW = self.BOTTOMPANELW*0.4
        self.STATUSPANELH = self.BOTTOMPANELH
        self.CHOICEBUTTONBOXW = self.BOTTOMPANELW-self.STATUSPANELW
        self.CHOICEBUTTONBOXH = self.BOTTOMPANELH
        self.CHOICEBUTTONW = 200
        self.CHOICEBUTTONH = 40
        self.CHOICEBUTTONSPERCOL = int(self.CHOICEBUTTONBOXH/self.CHOICEBUTTONH)
        self.CHOICEBUTTONSPERROW = int(self.CHOICEBUTTONBOXW/self.CHOICEBUTTONW)
        self.STATUSPANELFONTSIZE = 12
        self.TURNTRACKERW = SCREENW*0.6
        self.TURNTRACKERH = SCREENH*0.02
        self.HEALTHBARW = SCREENW*0.02
        self.HEALTHBARH = SCREENH*0.4
        self.HEALTHBARGROUPPOS = (SCREENW*0.5,SCREENH*0.4)

UICONST = UICONSTANTS()

class MenuButtonPainter(thorpy.painters.painter.Painter):
    def __init__(self,rectcolor=(100,100,100),presscolor=(0,0,0),size=None,clip=None,pressed=False,hovered=False):
        super(MenuButtonPainter, self).__init__(size,clip,pressed,hovered)
        self.rectcolor = rectcolor
        self.presscolor = presscolor

    def get_surface(self):
        surface = pygame.Surface(self.size, flags=pygame.SRCALPHA).convert_alpha()
        rect_body = surface.get_rect()
        # Parallelogram at 60 degrees, 50px wide if unhovered
        sqrt3 = 1.732 # good enough approximation of sqrt(3)
        if self.hovered:
            shapewidth = rect_body.width- rect_body.height/sqrt3
        else: 
            shapewidth = 50
        
        if self.pressed:
            fillcolor = self.presscolor
        else:
            fillcolor = self.rectcolor
            
        topleft = rect_body.topleft
        topright = (topleft[0]+shapewidth,topleft[1])
        bottomleft = (rect_body.bottomleft[0]+rect_body.height/sqrt3,rect_body.bottomleft[1])
        bottomright = (bottomleft[0]+shapewidth,bottomleft[1])

        shapepoints = [topleft,topright,bottomright,bottomleft] #in drawing order
        pygame.draw.polygon(surface,fillcolor,shapepoints)
        surface.set_clip(self.clip) #don't forget to set clip
        return surface

class TextBoxPainter(thorpy.painters.painter.Painter):
    def __init__(self,rectcolor=(100,100,100),bordercolor=(0,0,0),borderwidth=3,size=None,clip=None,pressed=False,hovered=False):
        super(TextBoxPainter, self).__init__(size,clip,pressed,hovered)
        self.rectcolor = rectcolor
        self.bordercolor = bordercolor
        self.borderwidth = borderwidth

    def get_surface(self):
        surface = pygame.Surface(self.size, flags=pygame.SRCALPHA).convert_alpha()
        rect_body = surface.get_rect()
        borderrect = rect_body.inflate(-self.borderwidth,-self.borderwidth)
        borderrect.move(-self.borderwidth,-self.borderwidth)
        pygame.draw.rect(surface,self.rectcolor,borderrect)

        pygame.draw.line(surface,self.bordercolor,borderrect.topleft,borderrect.topright,self.borderwidth)
        pygame.draw.line(surface,self.bordercolor,borderrect.topright,borderrect.bottomright,self.borderwidth)
        pygame.draw.line(surface,self.bordercolor,borderrect.bottomright,borderrect.bottomleft,self.borderwidth)
        pygame.draw.line(surface,self.bordercolor,borderrect.bottomleft,borderrect.topleft,self.borderwidth)
        return surface

class CustomPainters:
    def __init__(self) -> None:
        self.menubutton = MenuButtonPainter(    size=(400,80),
                                                rectcolor=(55,255,55),
                                                presscolor=(20,180,20))
        self.choicebutton = MenuButtonPainter(  size=(UICONST.CHOICEBUTTONW,UICONST.CHOICEBUTTONH),
                                                rectcolor=(230,200,100),
                                                presscolor=(180,160,100))
        self.big_textbox = TextBoxPainter(  rectcolor=(200,200,200),
                                            bordercolor=(50,50,50))

CUSTOMPAINTERS = CustomPainters()

class MenuContainer:
    def __init__(self,elements:dict={},reactions:dict={},build=False,**kwargs):
        self.elements = elements
        self.reactions = reactions
        self.background = None
        if build:
            self.build(**kwargs)
        return

    def addelements(self,elements:dict):
        self.elements.update(elements)

    def delelements(self,keys:list[str]):
        for key in keys:
            self.elements.pop(key)

    def addreactions(self,reactions:dict):
        self.reactions.update(reactions)

    def delreactions(self,keys:list[str]):
        for key in keys:
            self.reactions.pop(key)

    def build(self,**kwargs):
        if self.elements:
            elementlist = [self.elements[key] for key in self.elements]
        else:
            elementlist = None
        self.background = thorpy.Background(elements=elementlist,**kwargs)
        if self.reactions:
            for key in self.reactions:
                self.background.add_reaction(self.reactions[key])

    def updateelements(self,elements:dict={}):
        for key in elements:
            if key in self.elements:
                self.background.remove_elements([self.elements[key]])
            self.elements.update(elements)
            self.background.add_element(elements[key])
        thorpy.functions.refresh_current_menu()

    def reblit(self):
        self.background.unblit_and_reblit()

class GameGui:
    def __init__(self,gcontrol:gc.GameController):
        self.evthandler = UIHandler(self,gcontrol)
        ## Main menu
        self.genmainmenu()

    def launchmenu(self,menucontainer:MenuContainer):
        if thorpy.functions.get_current_menu():
            thorpy.functions.quit_menu_func()
        menu = thorpy.Menu(menucontainer.background,fps=FPS)
        menu.play()

    def genmainmenu(self):
        thorpy.style.FONT_SIZE = 48

        startbutton = thorpy.make_button("Battle",func=self.evthandler.startbuttonfunc)
        startbutton.set_painter(CUSTOMPAINTERS.menubutton)
        startbutton.finish()

        teamsbutton = thorpy.make_button("Teams")
        teamsbutton.set_painter(CUSTOMPAINTERS.menubutton)
        teamsbutton.set_pressed_state()
        teamsbutton.finish()

        quitbutton = thorpy.make_button("Quit",func=thorpy.functions.quit_func)
        quitbutton.set_painter(CUSTOMPAINTERS.menubutton)
        quitbutton.finish()

        mainmenubar = thorpy.Ghost([startbutton,teamsbutton,quitbutton])
        thorpy.store(mainmenubar,mode="v")
        mainmenubar.set_center((SCREENW/6,SCREENH*8/16))

        # Other buttons
        thorpy.style.FONT_SIZE = 18
        self.mainmenu = MenuContainer({"bar":mainmenubar},build=True,image=pygame.image.load(SCENEBG))

    def gensceneview(self,scene:sm.Scene):
        reac_time = thorpy.ConstantReaction(thorpy.constants.THORPY_EVENT, self.evthandler.updatescene,
                                            {"id":thorpy.constants.EVENT_TIME})

        turntracker = getturntrackers(scene)
        turntracker.set_center((SCREENW*0.5,SCREENH*0.1))
        healthbars = gethealthbars(scene)
        healthbars.set_center(UICONST.HEALTHBARGROUPPOS)

        self.sceneview = MenuContainer(elements={"turntracker":turntracker,"healthbars":healthbars},reactions={"reac_time":reac_time})

        self.sceneview.build(image=pygame.image.load(SCENEBG))
        return

    def updatesceneview(self,scene:sm.Scene):
        turntracker = getturntrackers(scene)
        turntracker.set_center((SCREENW*0.5,SCREENH*0.1))
        self.sceneview.updateelements({"turntracker":turntracker})
        healthbars = gethealthbars(scene)
        healthbars.set_center(UICONST.HEALTHBARGROUPPOS)
        self.sceneview.updateelements({"healthbars":healthbars})

        if scene.getstate() == SCENESTATES.DONE:
            # delete time reaction
            self.sceneview.delreactions(["reac_time"]) 

            winners = scene.rankings["winners"]
            losers = scene.rankings["losers"]
            victorytext = ' and '.join(beast.nickname for beast in winners) + " win(s)!\n" + ' and '.join(beast.nickname for beast in losers) + " lose(s)!"
            bottomtext = thorpy.make_text(text=victorytext,font_size=UICONST.STATUSPANELFONTSIZE,font_color=(0,0,0))
            returnbutton = thorpy.make_button("Return to menu",self.evthandler.endactivebattleandreturn)
            returnbutton.set_painter(CUSTOMPAINTERS.choicebutton)
            returnbutton.finish()
            boxgroup = thorpy.make_group([bottomtext,returnbutton],mode="v")
            bottombox = thorpy.Box([boxgroup],size=(UICONST.CHOICEBUTTONBOXW,UICONST.CHOICEBUTTONBOXH))
            bottombox.set_painter(CUSTOMPAINTERS.big_textbox)
            bottombox.finish()
            self.sceneview.updateelements({"buttonbox":bottombox})
        
        elif scene.active_beast:
            activebeast = scene.active_beast

            # statuspanel
            statuspanel = getstatuspanel(activebeast)
            statuspanel.finish()
            self.sceneview.updateelements({"statuspanel":statuspanel})

            if scene.getstate() == SCENESTATES.CHOOSEATTACK:
                # generate movebuttons
                movebuttons = [thorpy.make_button(atk.name,self.evthandler.movebuttonfunc,params={"scene":scene,"atk":atk}) for atk in activebeast.attacks]
                [but.set_painter(CUSTOMPAINTERS.choicebutton) for but in movebuttons]
                [but.finish() for but in movebuttons]
                movebutcols = [thorpy.make_group(movebuttons[col*UICONST.CHOICEBUTTONSPERCOL:(col+1)*UICONST.CHOICEBUTTONSPERCOL-1],mode="v") for col in range(ceil(len(movebuttons)/UICONST.CHOICEBUTTONSPERCOL))]
                movebutsgroup = thorpy.make_group(movebutcols,mode="h")
                movebuttonbox = thorpy.Box([movebutsgroup],size=(UICONST.CHOICEBUTTONBOXW,UICONST.CHOICEBUTTONBOXH))
                movebuttonbox.set_painter(CUSTOMPAINTERS.big_textbox)
                movebuttonbox.finish()
                self.sceneview.updateelements({"buttonbox":movebuttonbox})

            elif scene.getstate() == SCENESTATES.CHOOSETARGET:

                validtargets = scene.beasts.copy()
                for flagname in [flag["name"] for flag in activebeast.getselectedattack().flags]:
                    if flagname == TARGETOTHER: #effect on 1 other (friendly or enemy)
                        validtargets.remove(activebeast)
                    elif flagname == TARGETTEAM: #effect on team (friendly or enemy)
                        pass
                    elif flagname == TARGETALLOTHER: #effect on all others
                        raise Exception("Not implemented: " + TARGETALLOTHER)
                    elif flagname == TARGETSELF: #effect on self
                        raise Exception("Not implemented: " + TARGETSELF)
                    elif flagname == TARGETANY: #effect on any one character (including self)
                        pass
                    elif flagname == TARGETNONE: #no target (e.g. only set field conditions such as weather or terrain)
                        raise Exception("Not implemented: " + TARGETNONE)
                
                for beast in scene.beasts:
                    if (not beast.isalive):
                        validtargets.remove(beast) #remove dead things

                targetbuttons = [thorpy.make_button(target.nickname,self.evthandler.targetbuttonfunc,params={"scene":scene,"beasts":[target]}) for target in validtargets]
                [but.set_painter(CUSTOMPAINTERS.choicebutton) for but in targetbuttons]
                [but.finish() for but in targetbuttons]
                targetbutcols = [thorpy.make_group(targetbuttons[col*UICONST.CHOICEBUTTONSPERCOL:(col+1)*UICONST.CHOICEBUTTONSPERCOL-1],mode="v") for col in range(ceil(len(targetbuttons)/UICONST.CHOICEBUTTONSPERCOL))]
                targetbutsgroup = thorpy.make_group(targetbutcols,mode="h")
                targetbuttonbox = thorpy.Box([targetbutsgroup],size=(UICONST.CHOICEBUTTONBOXW,UICONST.CHOICEBUTTONBOXH))
                targetbuttonbox.set_painter(CUSTOMPAINTERS.big_textbox)
                targetbuttonbox.finish()
                self.sceneview.updateelements({"buttonbox":targetbuttonbox})

            elif scene.getstate() == SCENESTATES.EXECUTEATTACK:
                attacks = scene.attackresult
                boxtitle = thorpy.make_text(getattackresulttext(attacks),font_size=UICONST.STATUSPANELFONTSIZE,font_color=(0,0,0))
                continuebutton = thorpy.make_button("Continue",self.evthandler.executeattackcontinue,params={"scene":scene})
                continuebutton.set_painter(CUSTOMPAINTERS.choicebutton)
                continuebutton.finish()
                boxgroup = thorpy.make_group([boxtitle,continuebutton],mode="v")
                bottombox = thorpy.Box([boxgroup],size=(UICONST.CHOICEBUTTONBOXW,UICONST.CHOICEBUTTONBOXH))
                bottombox.set_painter(CUSTOMPAINTERS.big_textbox)
                bottombox.finish()
                self.sceneview.updateelements({"buttonbox":bottombox})
                
            elif scene.getstate() == SCENESTATES.IDLE:
                idletext = thorpy.make_text(text="Playing...",font_size=UICONST.STATUSPANELFONTSIZE,font_color=(0,0,0))
                idlebuttonbox = thorpy.Box([idletext],size=(UICONST.CHOICEBUTTONBOXW,UICONST.CHOICEBUTTONBOXH))
                idlebuttonbox.set_painter(CUSTOMPAINTERS.big_textbox)
                idlebuttonbox.finish()
                self.sceneview.updateelements({"buttonbox":idlebuttonbox})

            else:
                pass

        # bottompanel
        bottompanel = thorpy.Ghost(elements=[self.sceneview.elements["buttonbox"],self.sceneview.elements["statuspanel"]])
        thorpy.store(bottompanel,mode="h",margin=0)
        bottompanel.fit_children()
        
        bottompanel.set_center((SCREENW*0.5,SCREENH-UICONST.CHOICEBUTTONBOXH/2))

        self.sceneview.updateelements({"bottompanel":bottompanel})
        self.sceneview.reblit()
        return

class UIHandler:
    def __init__(self,gui:GameGui,gcontrol:gc.GameController) -> None:
        self.gui = gui
        self.gcontrol = gcontrol

    def startbuttonfunc(self):
        # normally swap to scene selection, but now we just skip to the scene view
        self.gcontrol.makeScene()
        self.gcontrol.setstate(GAMESTATES.SCENE)
        self.gui.gensceneview(self.gcontrol.scontrol.activescene)
        self.gui.launchmenu(self.gui.sceneview)
        return

    def movebuttonfunc(self,scene:sm.Scene,atk:c.Attack):
        activebeast = scene.active_beast
        activebeast.selectattack(atk)
        scene.setstate(SCENESTATES.CHOOSETARGET)
        return

    def targetbuttonfunc(self,scene:sm.Scene,beasts:list[sm.c.Beast]):
        activebeast = scene.active_beast
        activebeast.selecttargets(targets=beasts)
        scene.clearactiveflag()
        scene.setstate(SCENESTATES.IDLE)
        return

    def executeattackcontinue(self,scene:sm.Scene):
        scene.clearactiveflag()
        scene.setstate(SCENESTATES.IDLE)
        return

    def endactivebattleandreturn(self):
        self.gcontrol.scontrol.endactivescene()
        self.returntomainmenu()

    def returntomainmenu(self):
        self.gui.launchmenu(self.gui.mainmenu)

    def updatescene(self):
        activescene = self.gcontrol.getactivescene()
        activescene.run()
        if activescene.statechanged() or activescene.getstate() == SCENESTATES.IDLE:
            self.gui.updatesceneview(activescene)
            thorpy.functions.refresh_current_menu()
        

def getstatuspanel(beast:c.Beast,painter=CUSTOMPAINTERS.big_textbox) -> thorpy.Box:
    statustext = thorpy.make_text(text=getStatusText(beast),font_size=UICONST.STATUSPANELFONTSIZE,font_color=(0,0,0))
    statuspanel = thorpy.Box(elements=[statustext],size=(UICONST.STATUSPANELW,UICONST.STATUSPANELH))
    statuspanel.set_painter(painter)
    return statuspanel

def getturntrackers(scene:sm.Scene)->thorpy.Ghost:
    bars = []
    for beast in scene.beasts:
        bar = thorpy.LifeBar(   text=beast.nickname,
                                size=(UICONST.TURNTRACKERW,UICONST.TURNTRACKERH),
                                font_size=10) 

        spefrac = 1-abs(1-2*beast.turntracker/TURNTRACKER_LENGTH)
        if beast.turntracker < TURNTRACKER_LENGTH/2:
            bar.life_color = (0,255,0)
        else:
            bar.life_color = (0,100,0)
        bar.set_life(spefrac)
        bars.append(bar)
    bargroup = thorpy.make_group(bars,mode="v")
    return bargroup

def gethealthbars(scene:sm.Scene)->thorpy.Ghost:
    bars = []
    for beast in scene.beasts:
        bar = thorpy.LifeBar(   text=beast.nickname,
                                size=(UICONST.HEALTHBARW,UICONST.HEALTHBARH),
                                font_size=10,
                                type_="v") 

        hpfrac = beast.gethealthfrac()
        if hpfrac < 0.25:
            bar.life_color = (210,100,100)
        elif hpfrac < 0.5:
            bar.life_color = (190,190,80)
        else:
            bar.life_color = (100,230,50)
        bar.set_life(hpfrac)
        bars.append(bar)
    bargroup = thorpy.make_group(bars,mode="h")
    return bargroup

def getStatusText(beast:c.Beast) -> str:
    statustext = [beast.nickname,""]
    #print HP total
    hptext = str(beast.HP) + "/" + str(beast.maxHP) + " HP (" + str(max(round(beast.HP/beast.maxHP*100),1)) + "%)"
    statustext.append(hptext)
    if (beast.statuseffects):
        for status in beast.statuseffects:
            #different statuses need other things printed
            if (status["name"] == BURNNAME):
                statustext.append(BURNNAME)
            elif (status["name"] == SLOWNAME):
                statustext.append(SLOWNAME + " (" + str(ceil(status["trackleft"]/TURNTRACKER_LENGTH)) + " turns left)")
    else:
        statustext.append("Healthy")
    statustext.append("")
    statustext.append("physATK: " + str(int(beast.physATK)))
    statustext.append("magATK: " + str(int(beast.magATK)))
    statustext.append("physRES: " + str(int(beast.RES[0]*100)) + "%")
    statustext.append("heatRES: " + str(int(beast.RES[1]*100)) + "%")
    statustext.append("coldRES: " + str(int(beast.RES[2]*100)) + "%")
    statustext.append("shockRES: " + str(int(beast.RES[3]*100)) + "%")
    return '\n'.join(statustext)

def getattackresulttext(result:list[dict]) -> str:
    main_attack = result[0]

    targets = [target["defender"] for target in result]
    targets = list(dict.fromkeys(targets)) #remove duplicates by converting to dict and back
    text = [main_attack["attacker"].nickname + " used " + main_attack["attack"].name + " on " + " and ".join([x.nickname for x in targets]) + "!"]
    return '\n'.join(text)

#########################################################
# DECPRECATED CODE THAT MIGHT STILL BE USEFUL
#########################################################

def getShortStatusText(beast: c.Beast) -> str:
    statustext = [beast.nickname]
    #print HP total
    hptext = str(beast.HP) + "/" + str(beast.maxHP) + " HP (" + str(max(round(beast.HP/beast.maxHP*100),1)) + "%)"
    statustext.append(hptext)
    if (beast.statuseffects):
        for status in beast.statuseffects:
            #different statuses need other things printed
            if (status["name"] == BURNNAME):
                statustext.append(BURNNAME)
            elif (status["name"] == SLOWNAME):
                statustext.append(SLOWNAME + " (" + str(ceil(status["trackleft"]/TURNTRACKER_LENGTH)) + " turns left)")
    return statustext

def getAttackTooltipText(attack: c.Attack) -> str:
    statustext = attack.tooltip.copy()

    #Flags
    for flag in attack.flags:
        if flag["name"] == CONTACTFLAG:
            statustext.append("Contact")
        elif flag["name"] == MULTIHITNAME:
            statustext.append("Hits " + str(flag["value"]) + " times")
        elif flag["name"] == TARGETOTHER:
            statustext.append("Target: Any Other")
        elif flag["name"] == TARGETTEAM:
            statustext.append("Target: Team")
        elif flag["name"] == TARGETALLOTHER:
            statustext.append("Target: All Others")
        elif flag["name"] == TARGETSELF:
            statustext.append("Target: Self")
        elif flag["name"] == TARGETANY:
            statustext.append("Target: Any")
        elif flag["name"] == TARGETNONE:
            statustext.append("Target: None")
        else:
            statustext.append("UNHANDLED FLAG tooltip: " + flag["name"])

    #Chains
    if attack.chainID != NOCHAINID:
        nextatk = c.getAttack(attack.chainID)
        chainatks = [nextatk]
        while nextatk.chainID != NOCHAINID:
            nextatk = c.getAttack(nextatk.chainID)
            chainatks.append(nextatk)
            
        statustext.append("Chains into:")
        for atk in chainatks:
            statustext.append(atk.name)
        

    #Damage
    for n,power in enumerate(attack.power):
        if power>0:
            statustext.append(ELEMENTS[n] + " power: " + str(int(power*100)) + "%")
    #Secondary effects
    for effect in attack.effects:
        if effect["value"]==VALUENONE:
            #effects with no value
            statustext.append(str(int(effect["chance"]*100)) + "% Chance to apply " + effect["name"])
        elif effect["chance"]==CHANCENONE:
            #effect which always applies
            statustext.append("Applies " + effect["name"] + " " + str(effect["value"]))
        else:
            #generic status
            statustext.append(str(int(effect["chance"]*100)) + "% Chance to apply " + effect["name"] + " " + str(effect["value"]))
    return statustext

def getTargetTooltipText(target: c.Beast) -> str:
    return getShortStatusText(target)

def getTurntrackerTooltipText(scene: sm.Scene) -> str:
    text = []
    for beast in scene.beasts:
        trackerpercentage = (beast.turntracker % (scene.turnTrackerLength/2))/(scene.turnTrackerLength/2)*100 #0-100 going one way, 0-100 going back
        text.append(beast.nickname + ": " + str(round(trackerpercentage,1)) + "% (" + str(beast.SPE) + " SPE)")
    return text

#########################################################
# ELDERLY CODE (DEPRECATED)
#########################################################

# def drawExecuteAttack(screen,scene,attacks):
#     drawScene(screen,scene)
#     overlay = screen.getLayer("overlay")

#     MAJORBOX.draw(overlay)

#     buttons = []

#     targets = []
#     for target in attacks:
#         targets.append(target["defender"])
#     targets = list(dict.fromkeys(targets)) #remove duplicates

#     main_attack = attacks[0] #first attack is the name of the move that was used
#     titletext = [main_attack["attacker"].nickname + " used " + main_attack["attack"].name + " on " + " and ".join([x.nickname for x in targets]) + "!"]
#     title = TextBox(
#         box=Box(Rect_f(0,0,1,0.2),parent=MAJORBOX),
#         lines=titletext,
#         textcolor=pygame.Color("black"),
#         backgroundcolor=pygame.Color("white"),
#         border_radius=14,
#         textalignment="centre",
#         font=pygame.font.SysFont("None",30)
#         )
#     title.draw(overlay)

#     # main body text
#     boxoffset = 0.01
#     detailstext = []
#     for n,attack in enumerate(attacks):
#         if (attack["success"]):
#             if (attack["hit"]):
#                 if (attack["crit"]):
#                     detailstext.append("Critical hit!")
#                 dmgperc = attack["damage total"]/attack["defender"].maxHP*100
#                 if (dmgperc >= 1):
#                     detailstext.append(attack["defender"].nickname + " took " + str(attack["damage total"]) + " (" + str(round(dmgperc)) + "%) dmg!")
#                 else:
#                     detailstext.append(attack["defender"].nickname + " took " + str(attack["damage total"]) + " (<1%) dmg!")
                
#                 if attack["secondary effects"]:
#                     for status in attack["secondary effects"]:
#                         if status["name"] in [BURNNAME,SLOWNAME]:
#                             detailstext.append("    Status applied: " + status["name"] + "!") #TODO include severity (if applicable)
#                         elif status["name"] == REFLECTNAME:
#                             refldmgperc = status["damage total"]/attack["attacker"].maxHP*100
#                             if (dmgperc >= 1):
#                                 detailstext.append("    " + attack["defender"].nickname + " reflected " + str(status["damage total"])  + " (" + str(round(refldmgperc)) + "%) dmg back to " + attack["attacker"].nickname)
#                             else:
#                                 detailstext.append("    " + attack["defender"].nickname + " reflected " + str(status["damage total"])  + " (<1%) dmg back to " + attack["attacker"].nickname)
#             else:
#                 detailstext.append("The attack missed!")
#         else:
#             if n == 0: #chain attacks dont need this spam
#                 detailstext.append("The attack failed!")

#     details = TextBox(
#         box=Box(Rect_f(0,0.2+boxoffset,1,0.6-boxoffset),parent=MAJORBOX),
#         lines = detailstext,
#         margin=Margin(0.05,0.1,0.05,0.05),
#         textcolor=pygame.Color("black"),
#         backgroundcolor=pygame.Color("white"),
#         border_radius=14,
#         font=pygame.font.SysFont("None",30),
#         textalignment="topLeft"
#         )
#     details.draw(overlay)

#     continuebutton_x = 0*(buttonwidth + interbox_margin_x)
#     continuebutton_y = 5*(buttonheight + interbox_margin_y)
#     continuebutton = Button(    buttype="continue",
#                                 text="continue",
#                                 box=Box(Rect_f(0,0.8+boxoffset,1,0.15-boxoffset),parent=MAJORBOX),
#                                 textcolor=pygame.Color("black"),
#                                 backgroundcolor=pygame.Color("white"),
#                                 border_radius=7,
#                                 font=pygame.font.SysFont("None",30))
#     continuebutton.draw(overlay)
#     buttons.append(continuebutton)

#     return buttons

