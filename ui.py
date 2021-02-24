import pygame
from pygame.locals import *
import scenemanager
import classes
from math import floor
from uiElements import *

pygame.init()

column_buttonlimit = 6
interbox_margin_y = 0.04
interbox_margin_x = 0.01
buttonheight = (1-interbox_margin_y*(column_buttonlimit-1))/column_buttonlimit
buttonfont = pygame.font.SysFont(None,int(200*buttonheight))
statusfont = pygame.font.SysFont(None,int(250*buttonheight))

def drawTargetSelect(surface,scene,beast):
    MAJORBOX.draw(surface)

    #create list of all buttons in the menu, divided into which column they belong to
    elements = [[],[]]

    #create button list for every column
    for slot,target in enumerate(scene.beasts[1:],start=1):
        col_num = 0
        if (slot > 2): #last two slots are other teams
            col_num = 1

        if (target.isalive):
            element = Button("beast",target.name,Box(Rect_f(0,0,0,0),None),font=buttonfont,textcolor=pygame.Color("black"),backgroundcolor=MOVESELECTFOREGROUNDCOLOR,hovercolor=BUTTONHOVERCOLOR)
        else:
            element = TextBox(Box(Rect_f(0,0,0,0),None),lines = [str(target.name)],font=buttonfont,textcolor=pygame.Color("black"),backgroundcolor=MOVESELECTGREY,textalignment="centre")
        elements[col_num].append(element)
    
    #final column contains the status, and no buttons
    statustext = [beast.name,"","Status:"]
    if (len(beast.statuseffects)):
        for status in beast.statuseffects:
            statustext.append(str(status))
    else:
        statustext.append("Healthy")
    statusbox = TextBox(Box(Rect_f(0,0,0,0),None),statustext,font=statusfont,textcolor=pygame.Color("black"),backgroundcolor=MOVESELECTFOREGROUNDCOLOR,margin=Margin(0.03,0.1,0.03,0.1))
    elements.append([statusbox])

    #create column boxes
    columns = []
    buttonwidth = (1-interbox_margin_x*(len(elements)-1))/len(elements)
    for column in range(len(elements)):
        columns.append(Box(Rect_f(column/len(elements),0,buttonwidth,1),parent=MINORBOX))
        for element in range(len(elements[column])):
            buttonrect = Rect_f( 0 , element*(buttonheight+interbox_margin_y) , 1 , buttonheight )
            elements[column][element].box.setrelrect(buttonrect)
            elements[column][element].box.setparent(columns[column])

    #last column
    for element_num,element in enumerate(elements[len(elements)-1]):
        if (element_num == 0):
            statusrect = Rect_f(0.05,0,0.9,0.5)
            element.box.setrelrect(statusrect)
            element.box.setparent(columns[len(elements)-1])

    for column in elements:
        for element in column:
            element.draw(surface)

    buttonlist = []
    for column in elements:
        for button in column:
            if isinstance(button,Button):
                buttonlist.append(button)
    return buttonlist

    return

def drawMoveselect(surface,beast):
    MAJORBOX.draw(surface)

    #create list of all buttons in the menu, divided into which column they belong to
    elements = [[]]
    col_num = 0

    #create button list for every column
    for button_id, atk in enumerate(beast.attacks):
        if (len(elements[col_num]) >= column_buttonlimit):
            elements.append([])
            col_num = col_num + 1
        elements[col_num].append(Button("atk",atk.name,Box(Rect_f(0,0,0,0),None),font=buttonfont,textcolor=pygame.Color("black"),backgroundcolor=MOVESELECTFOREGROUNDCOLOR,hovercolor=BUTTONHOVERCOLOR))
    #final column contains the status, and no buttons
    statustext = [beast.name,"","Status:"]
    if (len(beast.statuseffects)):
        for status in beast.statuseffects:
            statustext.append(str(status))
    else:
        statustext.append("Healthy")
    statusbox = TextBox(Box(Rect_f(0,0,0,0),None),statustext,font=statusfont,textcolor=pygame.Color("black"),backgroundcolor=MOVESELECTFOREGROUNDCOLOR,margin=Margin(0.03,0.1,0.03,0.1))
    elements.append([statusbox])

    #set the positions and sizes for all buttons execpt last column
    columns = []
    buttonwidth = (1-interbox_margin_x*(len(elements)-1))/len(elements)
    for column in range(len(elements)):
        columns.append(Box(Rect_f(column/len(elements),0,buttonwidth,1),parent=MINORBOX))
        if (column < len(elements)):
            for element in range(len(elements[column])):
                buttonrect = Rect_f( 0 , element*(buttonheight+interbox_margin_y) , 1 , buttonheight )
                elements[column][element].box.setrelrect(buttonrect)
                elements[column][element].box.setparent(columns[column])
    
    #last column
    for element_num,element in enumerate(elements[len(elements)-1]):
        if (element_num == 0):
            statusrect = Rect_f(0.05,0,0.9,0.5)
            element.box.setrelrect(statusrect)
            element.box.setparent(columns[len(elements)-1])
    
    for column in elements:
        for element in column:
            element.draw(surface)

    buttonlist = []
    for column in elements:
        for button in column:
            if isinstance(button,Button):
                buttonlist.append(button)
    return buttonlist

def drawScene(surface,scene):
    surface.fill(BACKGROUNDCOLOR)
    renderTextAtPos(surface,"Battle title",(surface.get_width()/2,0),"topCentre")

    slotreltextpos = [  
        (0,0),
        (0.6,0.35),
        (0.6,0.45),
        (0.05,0.2),
        (0.05,0.3)
    ]

    for slot, beast in enumerate(scene.beasts[1:],start=1):
        if beast.isalive:
            healthfrac = beast.HP/beast.maxHP
            slottext = beast.name + " " + str(beast.HP) + "/" + str(beast.maxHP) + " HP (" + str(max(round(healthfrac*100),1)) + "%)"
            textpos = multtuple(slotreltextpos[slot],screenDims)

            HPbaroffset = (0,int(NAMEFONTSIZE)/2)
            Hpbarwidth = int(screenDims[0]*(0.33))
            Hpbarheight = int(screenDims[1]*(0.02))
            HPbarposition = addtuple(textpos,HPbaroffset)

            pygame.draw.rect(surface,HPBACKGROUNDCOLOR,(HPbarposition,(Hpbarwidth,Hpbarheight)))
            pygame.draw.rect(surface,HPFOREGROUNDCOLOR,(HPbarposition,(Hpbarwidth*healthfrac,Hpbarheight)))
            renderTextAtPos(surface,slottext,textpos,"centreLeft",font=NAMEFONT)
    return

def addtuple(xs,ys):
     return tuple(x + y for x, y in zip(xs, ys))
    
def multtuple(xs,ys):
    return tuple(x * y for x, y in zip(xs, ys))