import pygame
import thorpy
from pygame.locals import *
from math import floor,ceil
from fnmatch import fnmatch
from eventhandlers import continueaction
from globalconstants import *
from uiElements import *
from tuplemath import addtuple, multtuple
from classes import Beast, Attack, getAttack, getStaticText
from scenemanager import Scene, Slot
import teamimport as timport

pygame.init()

# Thorpy styling

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

# generic button
generic_menubutton_painter = MenuButtonPainter( size=(400,80),
                                                rectcolor=(55,255,55),
                                                presscolor=(20,180,20))
movebutton_painter = MenuButtonPainter( size=(200,40),
                                        rectcolor=(200,200,200),
                                        presscolor=(100,100,100))


# UI constants
interbox_margin_y = 0.04
interbox_margin_x = 0.01
numcolumns = 4
numbutspercol = 6
buttonwidth = 1/numcolumns-interbox_margin_x
buttonheight = 1/numbutspercol-interbox_margin_y
buttonfont = pygame.font.SysFont(None,int(200*buttonheight))
statusfont = pygame.font.SysFont(None,int(250*buttonheight))

def getStatusText(beast:Beast):
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
    
    return statustext

def getShortStatusText(beast: Beast) -> str:
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

def getAttackTooltipText(attack: Attack) -> str:
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
        nextatk = getAttack(attack.chainID)
        chainatks = [nextatk]
        while nextatk.chainID != NOCHAINID:
            nextatk = getAttack(nextatk.chainID)
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

def getTargetTooltipText(target: Beast) -> str:
    return getShortStatusText(target)

def getStatusInfo(status: Beast) -> str:
    if ( fnmatch(status["name"], BURNNAME) ):
        return getStaticText("Burntooltip")
    elif ( fnmatch(status["name"], SLOWNAME) ):
        return getStaticText("Slowtooltip")
    
    return ["Tooltip not implemented"]

def getTurntrackerTooltipText(scene: Scene) -> str:
    text = []
    for slot in scene.slots:
        beast = slot.beast
        trackerpercentage = (slot.turntracker % (scene.turnTrackerLength/2))/(scene.turnTrackerLength/2)*100 #0-100 going one way, 0-100 going back
        text.append(beast.nickname + ": " + str(round(trackerpercentage,1)) + "% (" + str(beast.SPE) + " SPE)")
    return text

def drawTargetSelect(screen: Screen, scene: Scene, slot: Slot):
    overlay = screen.getLayer("overlay")
    tooltips = screen.getLayer("tooltips")

    MAJORBOX.draw(overlay)

    beast = slot.beast
    attackflags = beast.selected_attack.atk.flags
    beastslot = slot.num

    valid_targets = [0,1,2,3]
    for flagname in [flag["name"] for flag in attackflags]:
        if flagname == TARGETOTHER: #effect on 1 other (friendly or enemy)
            valid_targets.remove(beastslot)
        elif flagname == TARGETTEAM: #effect on team (friendly or enemy)
            #valid_targets.remove(beastslot)
            # if beastslot == 0 or beastslot == 2:
            #     valid_targets.remove(beastslot + 1)
            # else:
            #     valid_targets.remove(beastslot - 1)
            pass
        elif flagname == TARGETALLOTHER: #effect on all others
            raise Exception("Not implemented: " + TARGETALLOTHER)
        elif flagname == TARGETSELF: #effect on self
            raise Exception("Not implemented: " + TARGETSELF)
        elif flagname == TARGETANY: #effect on any one character (including self)
            pass
        elif flagname == TARGETNONE: #no target (e.g. only set field conditions such as weather or terrain)
            raise Exception("Not implemented: " + TARGETNONE)
    
    for x in scene.slots:
        if (not x.beast.isalive):
            valid_targets.remove(x.num) #remove dead things

    buttons = []

    for slot in scene.slots:

        row_num = slot.num % BEASTSPERTEAM
        col_num = floor( slot.num / BEASTSPERTEAM )

        targetbutton_x = col_num * (buttonwidth + interbox_margin_x)
        targetbutton_y = row_num * (buttonheight + interbox_margin_y)

        if slot.num in valid_targets:
            targetbutton = Button(  "target",
                                    slot.beast.nickname,
                                    Box(Rect_f(targetbutton_x,targetbutton_y,buttonwidth,buttonheight),MINORBOX),
                                    font=buttonfont,
                                    textcolor=pygame.Color("black"),
                                    backgroundcolor=MOVESELECTFOREGROUNDCOLOR,
                                    hovercolor=BUTTONHOVERCOLOR,
                                    action=beast.selecttarget,
                                    actionargs=[scene,slot.num]
                                    )
            buttons.append(targetbutton)
        else:
            targetbutton = Button(  "target",
                                    slot.beast.nickname,
                                    Box(Rect_f(targetbutton_x,targetbutton_y,buttonwidth,buttonheight),MINORBOX),
                                    font=buttonfont,
                                    textcolor=pygame.Color("black"),
                                    backgroundcolor=MOVESELECTGREY,
                                    hovercolor=MOVESELECTGREY,
                                    actionargs=[scene,slot]
                                    )
        targetbutton.draw(overlay)

        targettooltip = Tooltip(getTargetTooltipText,[slot.beast],targetbutton.box)
        targettooltip.draw(tooltips)
    
    backbutton_x = 2 * (buttonwidth + interbox_margin_x)
    backbutton_y = 0 * (buttonheight + interbox_margin_y)
    backbutton = Button(    "back",
                            "Back",
                            Box(Rect_f(backbutton_x,backbutton_y,buttonwidth,buttonheight),MINORBOX),
                            font=buttonfont,
                            textcolor=pygame.Color("black"),
                            backgroundcolor=MOVESELECTFOREGROUNDCOLOR,
                            hovercolor=BUTTONHOVERCOLOR,
                            action=scene.setstate,
                            actionargs=["Choose attack"]
                            )
    backbutton.draw(overlay)
    buttons.append(backbutton)

    statusbox_rectf = Rect_f(3*(buttonwidth + interbox_margin_x),0,buttonwidth,1)
    statustext = getStatusText(beast)
    statusbox = TextBox(    Box(statusbox_rectf,MINORBOX),
                            statustext,
                            font=statusfont,
                            textcolor=pygame.Color("black"),
                            backgroundcolor=MOVESELECTFOREGROUNDCOLOR,
                            margin=Margin(0.03,0.1,0.03,0.1))
    statusbox.draw(overlay)

    return buttons

def drawMoveselect(screen,scene,slot):
    drawScene(screen,scene)

    beast = slot.beast
    overlay = screen.getLayer("overlay")
    tooltips = screen.getLayer("tooltips")
    MAJORBOX.draw(overlay)
    buttons = []

    for atk_id,atk in enumerate(beast.attacks):
        row_num = atk_id % numbutspercol
        col_num = floor(atk_id / numbutspercol)

        atkbutton_x = col_num * (buttonwidth + interbox_margin_x)
        atkbutton_y = row_num * (buttonheight + interbox_margin_y)
        attackbutton = Button(  "attack",
                                atk.name,
                                Box(Rect_f(atkbutton_x,atkbutton_y,buttonwidth,buttonheight),MINORBOX),
                                font=buttonfont,
                                textcolor=pygame.Color("black"),
                                backgroundcolor=MOVESELECTFOREGROUNDCOLOR,
                                hovercolor=BUTTONHOVERCOLOR,
                                action=beast.selectattack,
                                actionargs=[atk]
                                )
        attackbutton.draw(overlay)
        buttons.append(attackbutton)

        attacktooltip = Tooltip(getAttackTooltipText,[atk],attackbutton.box)
        attacktooltip.draw(tooltips)

    statusbox_rectf = Rect_f(3*(buttonwidth + interbox_margin_x),0,buttonwidth,1)
    statustext = getStatusText(beast)
    statusbox = TextBox(    Box(statusbox_rectf,MINORBOX),
                            statustext,
                            font=statusfont,
                            textcolor=pygame.Color("black"),
                            backgroundcolor=MOVESELECTFOREGROUNDCOLOR,
                            margin=Margin(0.03,0.1,0.03,0.1))
    statusbox.draw(overlay)

    return buttons

def drawExecuteAttack(screen,scene,attacks):
    drawScene(screen,scene)
    overlay = screen.getLayer("overlay")

    MAJORBOX.draw(overlay)

    buttons = []

    targets = []
    for target in attacks:
        targets.append(target["defender"])
    targets = list(dict.fromkeys(targets)) #remove duplicates

    main_attack = attacks[0] #first attack is the name of the move that was used
    titletext = [main_attack["attacker"].nickname + " used " + main_attack["attack"].name + " on " + " and ".join([x.nickname for x in targets]) + "!"]
    title = TextBox(
        box=Box(Rect_f(0,0,1,0.2),parent=MAJORBOX),
        lines=titletext,
        textcolor=pygame.Color("black"),
        backgroundcolor=pygame.Color("white"),
        border_radius=14,
        textalignment="centre",
        font=pygame.font.SysFont("None",30)
        )
    title.draw(overlay)

    # main body text
    boxoffset = 0.01
    detailstext = []
    for n,attack in enumerate(attacks):
        if (attack["success"]):
            if (attack["hit"]):
                if (attack["crit"]):
                    detailstext.append("Critical hit!")
                dmgperc = attack["damage total"]/attack["defender"].maxHP*100
                if (dmgperc >= 1):
                    detailstext.append(attack["defender"].nickname + " took " + str(attack["damage total"]) + " (" + str(round(dmgperc)) + "%) dmg!")
                else:
                    detailstext.append(attack["defender"].nickname + " took " + str(attack["damage total"]) + " (<1%) dmg!")
                
                if attack["secondary effects"]:
                    for status in attack["secondary effects"]:
                        if status["name"] in [BURNNAME,SLOWNAME]:
                            detailstext.append("    Status applied: " + status["name"] + "!") #TODO include severity (if applicable)
                        elif status["name"] == REFLECTNAME:
                            refldmgperc = status["damage total"]/attack["attacker"].maxHP*100
                            if (dmgperc >= 1):
                                detailstext.append("    " + attack["defender"].nickname + " reflected " + str(status["damage total"])  + " (" + str(round(refldmgperc)) + "%) dmg back to " + attack["attacker"].nickname)
                            else:
                                detailstext.append("    " + attack["defender"].nickname + " reflected " + str(status["damage total"])  + " (<1%) dmg back to " + attack["attacker"].nickname)
            else:
                detailstext.append("The attack missed!")
        else:
            if n == 0: #chain attacks dont need this spam
                detailstext.append("The attack failed!")

    details = TextBox(
        box=Box(Rect_f(0,0.2+boxoffset,1,0.6-boxoffset),parent=MAJORBOX),
        lines = detailstext,
        margin=Margin(0.05,0.1,0.05,0.05),
        textcolor=pygame.Color("black"),
        backgroundcolor=pygame.Color("white"),
        border_radius=14,
        font=pygame.font.SysFont("None",30),
        textalignment="topLeft"
        )
    details.draw(overlay)

    continuebutton_x = 0*(buttonwidth + interbox_margin_x)
    continuebutton_y = 5*(buttonheight + interbox_margin_y)
    continuebutton = Button(    buttype="continue",
                                text="continue",
                                box=Box(Rect_f(0,0.8+boxoffset,1,0.15-boxoffset),parent=MAJORBOX),
                                textcolor=pygame.Color("black"),
                                backgroundcolor=pygame.Color("white"),
                                border_radius=7,
                                font=pygame.font.SysFont("None",30),
                                action=continueaction)
    continuebutton.draw(overlay)
    buttons.append(continuebutton)

    return buttons

def drawTurnTracker(screen,scene):
    overlay = screen.getLayer("overlay")
    tooltips = screen.getLayer("tooltips")
    
    #turntracker
    turntrackerbox = Box(Rect_f(0.1,0.03,0.8,0.08),parent=BASEBOX)
    #turn tracker exists on 1 bar with 4 markers
    #print bar
    bar_x = 0.1
    bar_y = 0.325
    bar_w = 1-2*bar_x
    bar_h = 1-2*bar_y
    barbox = Box(Rect_f(bar_x,bar_y,bar_w,bar_h),parent = turntrackerbox,color=TRACKERBARCOLOR)
    barbox.draw(overlay)    
    for slot in scene.slots:
        beast = slot.beast
        if beast.isalive:
            #print name
            nameoffset = 0.005
            trackerFont = pygame.font.SysFont(None,int(turntrackerbox.absrect.height*0.5))
            if (slot.num == 0):
                namepos = (barbox.absrect.left-nameoffset*barbox.parent.absrect.width,barbox.absrect.top+barbox.absrect.height*0)
                namealignment = "centreRight"
                slotcolor = SLOT1COLOR
            elif (slot.num == 1):
                namepos = (barbox.absrect.left-nameoffset*barbox.parent.absrect.width,barbox.absrect.top+barbox.absrect.height*1)
                namealignment = "centreRight"
                slotcolor = SLOT2COLOR
            elif (slot.num == 2):
                namepos = (barbox.absrect.right+nameoffset*barbox.parent.absrect.width,barbox.absrect.top+barbox.absrect.height*0)
                namealignment = "centreLeft"
                slotcolor = SLOT3COLOR
            elif (slot.num == 3):
                namepos = (barbox.absrect.right+nameoffset*barbox.parent.absrect.width,barbox.absrect.top+barbox.absrect.height*1)
                namealignment = "centreLeft"
                slotcolor = SLOT4COLOR

            renderTextAtPos(overlay,beast.nickname,namepos,alignment=namealignment,font = trackerFont,color = slotcolor)

            #print marker
            markerwidth = barbox.absrect.height*1/2
            if (slot.turntracker < scene.turnTrackerLength/2): #moving forward to attack
                progresstoattack = slot.turntracker/TURNTRACKER_LENGTH*2
                markerposx = barbox.absrect.left + barbox.absrect.width*min(progresstoattack,1)
                markerheight = barbox.absrect.height*2
                markerposy = barbox.absrect.centery-markerheight/2 + 1 #idk why but its off by 1 pixel and its infuriating
        
            else: #moving back to move select
                progresstomovesel = (slot.turntracker-scene.turnTrackerLength/2)/scene.turnTrackerLength*2
                markerposx = barbox.absrect.right - barbox.absrect.width*min(progresstomovesel,1) - markerwidth
                markerheight = barbox.absrect.height
                markerposy = barbox.absrect.centery-markerheight/2 + 1 #idk why but its off by 1 pixel and its infuriating
            markerpos = ( markerposx , markerposy )
            markerdims = ( markerwidth , markerheight )
            pygame.draw.rect(overlay,slotcolor,(markerpos,markerdims))
    
    for slot in scene.slots:
        beast = slot.beast
        if beast.isalive:
            region = turntrackerbox
            turntrackertooltip = Tooltip(   getTurntrackerTooltipText,
                                            [scene],
                                            region=region)
            turntrackertooltip.draw(tooltips)
    return

def drawHealthbars(screen,scene):
    overlay = screen.getLayer("overlay")
    tooltips = screen.getLayer("tooltips")

    slotreltextpos = [  
        (0.6,0.42),
        (0.6,0.47),
        (0.05,0.17),
        (0.05,0.22)
    ]

    Hpbarwidth = int((SCREENW,SCREENH)[0]*(0.33))
    Hpbarheight = int((SCREENW,SCREENH)[1]*(0.01))

    for slot in scene.slots:
        beast = slot.beast
        if beast.isalive:
            #HP bar
            healthfrac = beast.HP/beast.maxHP
            slottext = beast.nickname + " " + str(beast.HP) + "/" + str(beast.maxHP) + " HP (" + str(max(round(healthfrac*100),1)) + "%)"
            textpos = multtuple(slotreltextpos[slot.num],(SCREENW,SCREENH))
            HPbaroffset = (0,int(NAMEFONTSIZE)/2)
            HPbarposition = addtuple(textpos,HPbaroffset)

            if (slot.num == 0):
                textcolor = SLOT1COLOR
                region=Box(Rect_f(0.6,0.40,0.33,0.05),BASEBOX)
            elif (slot.num == 1):
                textcolor = SLOT2COLOR
                region=Box(Rect_f(0.6,0.45,0.33,0.05),BASEBOX)
            elif (slot.num == 2):
                textcolor = SLOT3COLOR
                region=Box(Rect_f(0.05,0.15,0.33,0.05),BASEBOX)
            elif (slot.num == 3):
                textcolor = SLOT4COLOR
                region=Box(Rect_f(0.05,0.20,0.33,0.05),BASEBOX)

            #bars
            pygame.draw.rect(overlay,HPBACKGROUNDCOLOR,(HPbarposition,(Hpbarwidth,Hpbarheight)))
            pygame.draw.rect(overlay,HPFOREGROUNDCOLOR,(HPbarposition,(Hpbarwidth*healthfrac,Hpbarheight)))

            #name text
            renderTextAtPos(overlay,slottext,textpos,"centreLeft",font=NAMEFONT,color=textcolor)

            #statustooltip
            textsize = NAMEFONT.size(slottext)
            healthbartooltip = Tooltip( getShortStatusText,
                                        [slot.beast],
                                        region=Box(Rect_f(slotreltextpos[slot.num][0],slotreltextpos[slot.num][1]-textsize[1]/(2*SCREENH),textsize[0]/SCREENW,textsize[1]/SCREENH),BASEBOX))
            healthbartooltip.draw(tooltips)

            #(De-)Buff icons
            iconx = textpos[0] + NAMEFONT.size(slottext)[0]
            icony = textpos[1]- NAMEFONT.size(slottext)[1]/2
            radius = int(NAMEFONT.get_height()/2)
            for effect in beast.statuseffects:
                #icon
                if ( effect["name"] == BURNNAME ):
                    pygame.draw.circle(overlay,pygame.Color("red"),(iconx+radius,icony+radius),radius)
                elif ( effect["name"] == SLOWNAME ):
                    pygame.draw.circle(overlay,pygame.Color("lightblue"),(iconx+radius,icony+radius),radius)
                else:
                    iconx -= 2*radius
                iconx += 2*radius

                #tooltip
                bufftooltip = Tooltip(  getStatusInfo,
                                        [effect],
                                        region = Box(   Rect_f( (iconx-2*radius)/SCREENW,
                                                                (icony)/SCREENH,
                                                                (2*radius)/SCREENW,
                                                                (2*radius)/SCREENH),
                                                        BASEBOX))
                bufftooltip.draw(tooltips)

    return

def drawBackground(screen,scene):
    background = screen.getLayer("background")
    bgimg = pygame.image.load("./images/scene.png")
    
    background.fill(BACKGROUNDCOLOR)
    bgimg = pygame.transform.scale(bgimg,(background.get_width(),int(background.get_height()*0.525)))
    background.blit(bgimg,(0,0))
    return

def drawScene(screen,scene):
    drawBackground(screen,scene)
    drawTurnTracker(screen,scene)
    drawHealthbars(screen,scene)
    return

def drawIdle(screen,scene):
    drawScene(screen,scene)
    return