import pygame
from pygame.locals import *
import scenemanager
import classes
from math import floor,ceil
from globalconstants import *
from uiElements import *

pygame.init()

# ui constants, these can stay here
column_buttonlimit = 6
interbox_margin_y = 0.04
interbox_margin_x = 0.01
buttonheight = (1-interbox_margin_y*(column_buttonlimit-1))/column_buttonlimit
buttonfont = pygame.font.SysFont(None,int(200*buttonheight))
statusfont = pygame.font.SysFont(None,int(250*buttonheight))

def getStatusText(beast):
    statustext = [beast.nickname,"","Status:"]
    #print HP total
    hptext = str(beast.HP) + "/" + str(beast.maxHP) + " HP (" + str(max(round(beast.HP/beast.maxHP*100),1)) + "%)"
    statustext.append(hptext)
    if (len(beast.statuseffects)):
        for status in beast.statuseffects:
            #different statuses need other things printed
            if (status["name"] == BURNNAME):
                statustext.append(BURNNAME)
            elif (status["name"] == SLOWNAME):
                statustext.append(SLOWNAME + " (" + str(ceil(status["trackleft"]/TURNTRACKER_LENGTH)) + ")")
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

    boxoffset = 0.01
    detailstext = []
    for n,attack in enumerate(attacks):
        if (attack["success"]):
            if (attack["hit"]):
                if (attack["crit"]):
                    detailstext.append("Critical hit!")
                detailstext.append(attack["defender"].nickname + " took " + str(attack["damage total"]) + " (" + str(round(attack["damage total"]/attack["defender"].maxHP*100)) + "%) dmg!")
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
    turntrackerbox = Box(Rect_f(0.1,0.03,0.8,0.07),parent=BASEBOX)
    for slot,beast in enumerate(scene.beasts[1:],start=1):
        if beast.isalive:
            #set current bar position
            bar_w = 0.4
            bar_h = 0.18
            lcol_x = 0
            rcol_x = 1-bar_w
            trow_y = 0
            brow_y = 1-bar_h
            if ( slot == 1 ): #topright
                barrect = Rect_f(rcol_x,trow_y,bar_w,bar_h)
            elif ( slot == 2 ): #bottomright
                barrect = Rect_f(rcol_x,brow_y,bar_w,bar_h)
            elif ( slot == 3 ): #topleft
                barrect = Rect_f(lcol_x,trow_y,bar_w,bar_h)
            elif ( slot == 4 ): #bottomleft
                barrect = Rect_f(lcol_x,brow_y,bar_w,bar_h)
            
            #print bar
            barbox = Box(barrect,parent = turntrackerbox,color=TRACKERBARCOLOR)
            barbox.draw(surface)
            
            #print name
            nameoffset = 0.005
            trackerFont = pygame.font.SysFont(None,barbox.absrect.height*3)
            if slot == 1 or slot == 2: #right column has name to the left
                namepos = (barbox.absrect.left-nameoffset*barbox.parent.absrect.width,barbox.absrect.top+barbox.absrect.height/2)
                namealignment = "centreRight"
            else: #left column has name to the right
                namepos = (barbox.absrect.right+nameoffset*barbox.parent.absrect.width,barbox.absrect.top+barbox.absrect.height/2)
                namealignment = "centreLeft"
            renderTextAtPos(surface,beast.nickname,namepos,alignment=namealignment,font = trackerFont)
                

            #print marker
            if (scene.turnTracker[slot] < scene.turnTrackerLength/2):
                markerposx = barbox.absrect.left + barbox.absrect.width*min(scene.turnTracker[slot]/scene.turnTrackerLength*2,1)
                markerradius = barbox.absrect.height*1.5/2
            else:
                markerposx = barbox.absrect.right - barbox.absrect.width*min((scene.turnTracker[slot]-scene.turnTrackerLength/2)/scene.turnTrackerLength*2,1)
                markerradius = barbox.absrect.height*1/2
            markerpos = ( markerposx , barbox.absrect.centery )
            pygame.draw.circle(surface,TRACKERMARKERCOLOR,markerpos,markerradius)

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
            renderTextAtPos(surface,slottext,textpos,"centreLeft",font=NAMEFONT)
    return

def addtuple(xs,ys):
     return tuple(x + y for x, y in zip(xs, ys))
    
def multtuple(xs,ys):
    return tuple(x * y for x, y in zip(xs, ys))