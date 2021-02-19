import pygame
from pygame.locals import *
import scenemanager
import classes
from math import floor

pygame.init()

screenDims = (1280,720)

DEFAULTFONTSIZE = int(screenDims[1]/(360/50))
DEFAULTFONT = pygame.font.SysFont(None,DEFAULTFONTSIZE)
NAMEFONTSIZE = int(screenDims[1]/(360/20))
NAMEFONT = pygame.font.SysFont(None,NAMEFONTSIZE)

BACKGROUNDCOLOR = pygame.Color(80,158,40)
BACKGROUND = pygame.surface.Surface(screenDims).fill(BACKGROUNDCOLOR)
HPBACKGROUNDCOLOR = pygame.Color(180,180,180)
HPFOREGROUNDCOLOR = pygame.Color(180,0,0)
MOVESELECTBACKGROUNDCOLOR = pygame.Color(200,200,200)
MOVESELECTFOREGROUNDCOLOR = pygame.Color(240,240,240)
TESTCOLOR = pygame.Color(255,0,255)

def renderTextAtPos(surface,text,pos,alignment="topLeft",font=None,color=pygame.Color(255,255,255),backgroundcolor=BACKGROUNDCOLOR):
    if (font==None):
        font = DEFAULTFONT

    textSurface = font.render(text,1,color)
    if (alignment == "topLeft"):
        textpos=pos
    if (alignment == "topCentre"):
        textpos = (pos[0] - textSurface.get_width()/2, pos[1])
    if (alignment == "centreLeft"):
        textpos = (pos[0], pos[1] - textSurface.get_height()/2)
    if (alignment == "centreRight"):
        textpos = (pos[0] - textSurface.get_width(),pos[1] - textSurface.get_height()/2)

    backFill = pygame.surface.Surface((textSurface.get_width(),textSurface.get_height()))
    backFill.fill(backgroundcolor)
    surface.blit(backFill,textpos)
    surface.blit(textSurface,textpos)
    return Rect(textpos,(textSurface.get_width(),textSurface.get_height()))

def drawScene(surface,scene):
    surface.fill(BACKGROUNDCOLOR)
    renderTextAtPos(surface,"Battle title",(surface.get_width()/2,0),"topCentre")

    slotreltextpos = [  
        (0,0),
        (0.6,0.45),
        (0.6,0.55),
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

def drawMoveselect(surface,beast):
    majorBox = Rect(screenDims[0]*(0.02),screenDims[1]*(0.65),screenDims[0]*(0.96),screenDims[1]*(0.33))
    pygame.draw.rect(surface,MOVESELECTBACKGROUNDCOLOR,majorBox,border_radius = 14)

    #anything drawn inside the major box should at least be separated by a number of pixels equal to the margin
    majorBoxmargin_x = majorBox.width*(0.005)
    majorBoxmargin_y = majorBox.height*(0.03)

    minorBox = Rect(majorBox.left+majorBoxmargin_x,majorBox.top+majorBoxmargin_y,majorBox.width-2*majorBoxmargin_x,majorBox.height-2*majorBoxmargin_y)
    columns = []
    numcolumns = 4
    for col in range(numcolumns):
        newcol = Rect(minorBox.left+col*minorBox.width/numcolumns,minorBox.top,minorBox.width/numcolumns,minorBox.height)
        columns.append(newcol)

    numatks = len(beast.attacks)
    column_atklimit = 6
    #column1 - contains up to 6 attacks
    col1_boxes = []
    interbox_margin = minorBox.height*(0.04)
    if (numatks < column_atklimit):
        boxheight = (columns[0].height-interbox_margin*(numatks-1))/numatks
        for box in range(numatks):
            newbox = Rect( columns[0].left , columns[0].top+box*(boxheight+interbox_margin) , columns[0].width , boxheight )
            col1_boxes.append(newbox)
    else:
        boxheight = (columns[0].height-interbox_margin*(column_atklimit-1))/column_atklimit
        for box in range(column_atklimit):
            newbox = Rect( columns[0].left , columns[0].top+box*(boxheight+interbox_margin) , columns[0].width , boxheight )
            col1_boxes.append(newbox)
    
    for box_id, atk in enumerate(beast.attacks):
        #draws attack background
        pygame.draw.rect(surface, MOVESELECTFOREGROUNDCOLOR, col1_boxes[box_id],border_radius=7)
        attackfont = pygame.font.SysFont(None,int(boxheight/3))
        textoffset = (col1_boxes[box_id].w*(0.05),col1_boxes[box_id].h*(0.1))
        renderTextAtPos(surface,atk.name,addtuple(col1_boxes[box_id].topleft,textoffset),color = pygame.Color(0,0,0),font = attackfont,backgroundcolor=MOVESELECTFOREGROUNDCOLOR)



    #column2
    #column3
    #column4
    #pygame.draw.rect(surface,TESTCOLOR,minorBox)

    

    return

def addtuple(xs,ys):
     return tuple(x + y for x, y in zip(xs, ys))
    
def multtuple(xs,ys):
    return tuple(x * y for x, y in zip(xs, ys))