import pygame
from pygame.locals import *
import scenemanager
import classes
from math import floor,ceil
from globalconstants import *
from uiElements import *

pygame.init()

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

def drawTargetSelect(surface,scene,beast):
    MAJORBOX.draw(surface)

    #create list of all buttons in the menu, divided into which column they belong to
    menuelements = [[],[]]

    #create button list for every column
    for slot,target in enumerate(scene.beasts[1:],start=1):
        col_num = 0
        if (slot > 2): #last two slots are other teams
            col_num = 1

        if (target.isalive):
            element = Button("beast",target.nickname,Box(Rect_f(0,0,0,0),None),font=buttonfont,textcolor=pygame.Color("black"),backgroundcolor=MOVESELECTFOREGROUNDCOLOR,hovercolor=BUTTONHOVERCOLOR,id=slot)
        else:
            element = TextBox(Box(Rect_f(0,0,0,0),None),lines = [str(target.nickname)],font=buttonfont,textcolor=pygame.Color("black"),backgroundcolor=MOVESELECTGREY,textalignment="centre")
        menuelements[col_num].append(element)
    
    #final column contains the status, and no buttons
    statustext = getStatusText(beast)
    statusbox = TextBox(Box(Rect_f(0,0,0,0),None),statustext,font=statusfont,textcolor=pygame.Color("black"),backgroundcolor=MOVESELECTFOREGROUNDCOLOR,margin=Margin(0.03,0.1,0.03,0.1))
    menuelements.append([statusbox])

    #create column boxes
    columns = []
    buttonwidth = (1-interbox_margin_x*(len(menuelements)-1))/len(menuelements)
    for column in range(len(menuelements)):
        columns.append(Box(Rect_f(column/len(menuelements),0,buttonwidth,1),parent=MINORBOX))
        for element in range(len(menuelements[column])):
            buttonrect = Rect_f( 0 , element*(buttonheight+interbox_margin_y) , 1 , buttonheight )
            menuelements[column][element].box.setrelrect(buttonrect)
            menuelements[column][element].box.setparent(columns[column])

    #last column
    for element_num,element in enumerate(menuelements[len(menuelements)-1]):
        if (element_num == 0):
            statusrect = Rect_f(0.05,0,0.9,0.5)
            element.box.setrelrect(statusrect)
            element.box.setparent(columns[len(menuelements)-1])

    for column in menuelements:
        for element in column:
            element.draw(surface)

    buttonlist = []
    for column in menuelements:
        for button in column:
            if isinstance(button,Button):
                buttonlist.append(button)
    return buttonlist

def drawMoveselect(surface,scene,beast):
    MAJORBOX.draw(surface)

    #create list of all buttons in the menu, divided into which column they belong to
    menuelements = [[]]
    col_num = 0

    #create button list for every column
    for atk_id, atk in enumerate(beast.attacks):
        if (len(menuelements[col_num]) >= column_buttonlimit):
            menuelements.append([])
            col_num = col_num + 1
        menuelements[col_num].append(Button("attack",atk.name,Box(Rect_f(0,0,0,0),None),font=buttonfont,textcolor=pygame.Color("black"),backgroundcolor=MOVESELECTFOREGROUNDCOLOR,hovercolor=BUTTONHOVERCOLOR,id=atk_id))
    
    #final column contains the status, and no buttons
    statustext = getStatusText(beast)
    statusbox = TextBox(Box(Rect_f(0,0,0,0),None),statustext,font=statusfont,textcolor=pygame.Color("black"),backgroundcolor=MOVESELECTFOREGROUNDCOLOR,margin=Margin(0.03,0.1,0.03,0.1))
    menuelements.append([statusbox])

    #set the positions and sizes for all buttons execpt last column
    columns = []
    buttonwidth = (1-interbox_margin_x*(len(menuelements)-1))/len(menuelements)
    for column in range(len(menuelements)):
        columns.append(Box(Rect_f(column/len(menuelements),0,buttonwidth,1),parent=MINORBOX))
        if (column < len(menuelements)):
            for element in range(len(menuelements[column])):
                buttonrect = Rect_f( 0 , element*(buttonheight+interbox_margin_y) , 1 , buttonheight )
                menuelements[column][element].box.setrelrect(buttonrect)
                menuelements[column][element].box.setparent(columns[column])
    
    #last column
    for element_num,element in enumerate(menuelements[len(menuelements)-1]):
        if (element_num == 0):
            statusrect = Rect_f(0.05,0,0.9,0.5)
            element.box.setrelrect(statusrect)
            element.box.setparent(columns[len(menuelements)-1])
    
    for column in menuelements:
        for element in column:
            element.draw(surface)

    buttonlist = []
    for column in menuelements:
        for button in column:
            if isinstance(button,Button):
                buttonlist.append(button)
    return buttonlist

def drawExecuteAttack(surface,scene,attacks):
    main_attack = attacks[0] #first attack is the name of the move that was used

    MAJORBOX.draw(surface)
    menuelements = [[]]
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
    menuelements[0].append(title)

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
    menuelements[0].append(details)

    continuebutton = Button(
        buttype="continue",
        text="continue",
        box=Box(Rect_f(0,0.8+boxoffset,1,0.15-boxoffset),parent=MAJORBOX),
        textcolor=pygame.Color("black"),
        backgroundcolor=pygame.Color("white"),
        border_radius=7,
        font=pygame.font.SysFont("None",30)
        )
    menuelements[0].append(continuebutton)

    for column in menuelements:
        for element in column:
            element.draw(surface)

    buttonlist = []
    for column in menuelements:
        for button in column:
            if isinstance(button,Button):
                buttonlist.append(button)
    return buttonlist

def drawScene(surface,scene):
    surface.fill(BACKGROUNDCOLOR)

    #turntracker
    turntrackerbox = Box(Rect_f(0.1,0.03,0.8,0.08),parent=BASEBOX)
    #turn tracker exists on 1 bar with 4 markers
    #print bar
    bar_x = 0.1
    bar_y = 0.325
    bar_w = 1-2*bar_x
    bar_h = 1-2*bar_y
    barbox = Box(Rect_f(bar_x,bar_y,bar_w,bar_h),parent = turntrackerbox,color=TRACKERBARCOLOR)
    barbox.draw(surface)    
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

            renderTextAtPos(surface,beast.nickname,namepos,alignment=namealignment,font = trackerFont,color = slotcolor)

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
            pygame.draw.rect(surface,slotcolor,(markerpos,markerdims))

    # Health/statusboxes
    slotreltextpos = [  
        (0,0),
        (0.6,0.42),
        (0.6,0.47),
        (0.05,0.17),
        (0.05,0.22)
    ]

    for slot, beast in enumerate(scene.beasts[1:],start=1):
        if beast.isalive:
            healthfrac = beast.HP/beast.maxHP
            slottext = beast.nickname + " " + str(beast.HP) + "/" + str(beast.maxHP) + " HP (" + str(max(round(healthfrac*100),1)) + "%)"
            textpos = multtuple(slotreltextpos[slot],screenDims)

            HPbaroffset = (0,int(NAMEFONTSIZE)/2)
            Hpbarwidth = int(surface.get_width()*(0.33))
            Hpbarheight = int(surface.get_height()*(0.01))
            HPbarposition = addtuple(textpos,HPbaroffset)

            pygame.draw.rect(surface,HPBACKGROUNDCOLOR,(HPbarposition,(Hpbarwidth,Hpbarheight)))
            pygame.draw.rect(surface,HPFOREGROUNDCOLOR,(HPbarposition,(Hpbarwidth*healthfrac,Hpbarheight)))
            if (slot == 1):
                textcolor = SLOT1COLOR
            elif (slot == 2):
                textcolor = SLOT2COLOR
            elif (slot == 3):
                textcolor = SLOT3COLOR
            elif (slot == 4):
                textcolor = SLOT4COLOR
            renderTextAtPos(surface,slottext,textpos,"centreLeft",font=NAMEFONT,color=textcolor)
    return

def addtuple(xs,ys):
     return tuple(x + y for x, y in zip(xs, ys))
    
def multtuple(xs,ys):
    return tuple(x * y for x, y in zip(xs, ys))