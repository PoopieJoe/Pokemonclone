import pygame
from pygame.locals import *
import scenemanager
import classes
from math import floor,ceil
from eventhandlers import continueaction
from globalconstants import *
from uiElements import *
from tuplemath import addtuple,multtuple

pygame.init()

interbox_margin_y = 0.04
interbox_margin_x = 0.01
numcolumns = 4
numbutspercol = 6
buttonwidth = 1/numcolumns-interbox_margin_x
buttonheight = 1/numbutspercol-interbox_margin_y
buttonfont = pygame.font.SysFont(None,int(200*buttonheight))
statusfont = pygame.font.SysFont(None,int(250*buttonheight))

def getStatusText(beast):
    statustext = [beast.nickname,"","Status:"]
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
    return statustext

def getShortStatusText(beast):
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

def getStatusInfo(status):
    #TODO: make this
    return ["idk","make this"]


def getTurntrackerTooltipText(scene):
    text = []
    for slot,beast in enumerate(scene.beasts[1:],start=1):
        trackerpercentage = (scene.turnTracker[slot] % (scene.turnTrackerLength/2))/(scene.turnTrackerLength/2)*100 #0-100 going one way, 0-100 going back
        text.append(beast.nickname + ": " + str(round(trackerpercentage,1)) + "% (" + str(beast.SPE) + " SPE)")
    return text

def drawTargetSelect(screen,scene,beast):
    overlay = screen.getLayer("overlay")
    MAJORBOX.draw(overlay)

    buttons = []

    for slot,target in enumerate(scene.beasts[1:],start=1):
        row_num = (slot - 1) % BEASTSPERTEAM
        col_num = floor( (slot - 1) / BEASTSPERTEAM )

        targetbutton_x = col_num * (buttonwidth + interbox_margin_x)
        targetbutton_y = row_num * (buttonheight + interbox_margin_y)
        targetbutton = Button(  "target",
                                target.nickname,
                                Box(Rect_f(targetbutton_x,targetbutton_y,buttonwidth,buttonheight),MINORBOX),
                                font=buttonfont,
                                textcolor=pygame.Color("black"),
                                backgroundcolor=MOVESELECTFOREGROUNDCOLOR,
                                hovercolor=BUTTONHOVERCOLOR,
                                action=beast.selecttarget,
                                actionargs=[scene,slot]
                                )
        targetbutton.draw(overlay)
        buttons.append(targetbutton)
    
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

def drawMoveselect(screen,scene,beast):
    drawScene(screen,scene)

    overlay = screen.getLayer("overlay")
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
                                actionargs=[atk_id]
                                )
        attackbutton.draw(overlay)
        buttons.append(attackbutton)

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

    main_attack = attacks[0] #first attack is the name of the move that was used
    titletext = [main_attack["attacker"].nickname + " used " + main_attack["attack"].name + " on " + main_attack["defender"].nickname + "!"]
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
                
                
                if attack["secondary effects applied"]:
                    for status in attack["secondary effects applied"]:
                        detailstext.append("Status applied: " + status + "!")
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
    for slot,beast in enumerate(scene.beasts[1:],start=1):
        if beast.isalive:
            #print name
            nameoffset = 0.005
            trackerFont = pygame.font.SysFont(None,int(turntrackerbox.absrect.height*0.5))
            if (slot == 1):
                namepos = (barbox.absrect.left-nameoffset*barbox.parent.absrect.width,barbox.absrect.top+barbox.absrect.height*0)
                namealignment = "centreRight"
                slotcolor = SLOT1COLOR
            elif (slot == 2):
                namepos = (barbox.absrect.left-nameoffset*barbox.parent.absrect.width,barbox.absrect.top+barbox.absrect.height*1)
                namealignment = "centreRight"
                slotcolor = SLOT2COLOR
            elif (slot == 3):
                namepos = (barbox.absrect.right+nameoffset*barbox.parent.absrect.width,barbox.absrect.top+barbox.absrect.height*0)
                namealignment = "centreLeft"
                slotcolor = SLOT3COLOR
            elif (slot == 4):
                namepos = (barbox.absrect.right+nameoffset*barbox.parent.absrect.width,barbox.absrect.top+barbox.absrect.height*1)
                namealignment = "centreLeft"
                slotcolor = SLOT4COLOR

            renderTextAtPos(overlay,beast.nickname,namepos,alignment=namealignment,font = trackerFont,color = slotcolor)

            #print marker
            markerwidth = barbox.absrect.height*1/2
            if (scene.turnTracker[slot] < scene.turnTrackerLength/2): #moving forward to attack
                progresstoattack = scene.turnTracker[slot]/TURNTRACKER_LENGTH*2
                markerposx = barbox.absrect.left + barbox.absrect.width*min(progresstoattack,1)
                markerheight = barbox.absrect.height*2
                markerposy = barbox.absrect.centery-markerheight/2 + 1 #idk why but its off by 1 pixel and its infuriating
        
            else: #moving back to move select
                progresstomovesel = (scene.turnTracker[slot]-scene.turnTrackerLength/2)/scene.turnTrackerLength*2
                markerposx = barbox.absrect.right - barbox.absrect.width*min(progresstomovesel,1) - markerwidth
                markerheight = barbox.absrect.height
                markerposy = barbox.absrect.centery-markerheight/2 + 1 #idk why but its off by 1 pixel and its infuriating
            markerpos = ( markerposx , markerposy )
            markerdims = ( markerwidth , markerheight )
            pygame.draw.rect(overlay,slotcolor,(markerpos,markerdims))
    
    for slot,target in enumerate(scene.beasts[1:],start=1):
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
        (0,0),
        (0.6,0.42),
        (0.6,0.47),
        (0.05,0.17),
        (0.05,0.22)
    ]

    Hpbarwidth = int(screenDims[0]*(0.33))
    Hpbarheight = int(screenDims[1]*(0.01))

    for slot, beast in enumerate(scene.beasts[1:],start=1):
        if beast.isalive:
            #HP bar
            healthfrac = beast.HP/beast.maxHP
            slottext = beast.nickname + " " + str(beast.HP) + "/" + str(beast.maxHP) + " HP (" + str(max(round(healthfrac*100),1)) + "%)"
            textpos = multtuple(slotreltextpos[slot],screenDims)
            HPbaroffset = (0,int(NAMEFONTSIZE)/2)
            HPbarposition = addtuple(textpos,HPbaroffset)

            if (slot == 1):
                textcolor = SLOT1COLOR
                region=Box(Rect_f(0.6,0.40,0.33,0.05),BASEBOX)
            elif (slot == 2):
                textcolor = SLOT2COLOR
                region=Box(Rect_f(0.6,0.45,0.33,0.05),BASEBOX)
            elif (slot == 3):
                textcolor = SLOT3COLOR
                region=Box(Rect_f(0.05,0.15,0.33,0.05),BASEBOX)
            elif (slot == 4):
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
                                        [scene.beasts[slot]],
                                        region=Box(Rect_f(slotreltextpos[slot][0],slotreltextpos[slot][1]-textsize[1]/(2*screenDims[1]),textsize[0]/screenDims[0],textsize[1]/screenDims[1]),BASEBOX))
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
                                        region = Box(   Rect_f( (iconx-2*radius)/screenDims[0],
                                                                (icony)/screenDims[1],
                                                                (2*radius)/screenDims[0],
                                                                (2*radius)/screenDims[1]),
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