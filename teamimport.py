#TODO: import team from text file into scene
import classes as c
import scenemanager as s

def importteam(file):
    """
    Imports team from .txt file
    Parameters:
    file: source text file

    Returns: 
    Team object
    """

    #errormessages:
    EX_MISSINGCOLON = "Line has no property or is missing a colon."
    EX_MISSINGSPECIES = "Beast has no species."
    EX_INVALID_PROPERTY = "Invalid property."
    EX_INVALID_EQUIPMENT = "Invalid equipment given."
    EX_INVALID_SPECIES = "Invalid species given."
    EX_MISSING_FORMAT = "No battle format given."
    EX_INVALID_FORMAT = "Invalid format given."

    teamreader = open( file , "rt" )

    team = c.Team()
    battleformat = ""
    beastnum = -1
    equipmentcntr = 0
    for linenum, line in enumerate(teamreader.readlines()):
        if (line[0] != '-'):
            if (len(line) > 1):
                colonpos = line.find(':')
                if colonpos < 0:
                    raise Exception("[Line " + str(linenum) + "] " + EX_MISSINGCOLON + " (" + line + ")")
                prop = line[0:colonpos]
                detail = line[colonpos+1:len(line)].replace('\n','').strip()
                
                if (prop == "Team name"):
                    team.name = detail
                elif (prop == "Format"):
                    if (detail in ["Doubles"]):
                        battleformat = detail
                    else:
                        raise Exception("[Line " + str(linenum) + "] " + EX_INVALID_FORMAT)
                elif (prop == "Species"):
                    try:
                        beastnum += 1
                        equipmentcntr = 0
                        newbeast = c.Beast(detail,None,[])
                        team.beasts.append(newbeast)
                    except Exception:
                        raise Exception("[Line " + str(linenum) + "] " + EX_INVALID_SPECIES)
                elif (prop == "Name"):
                    if (beastnum >= 0):
                        team.beasts[beastnum].nickname = detail
                    else:
                        raise Exception("[Line " + str(linenum) + "] " + EX_MISSINGSPECIES)
                elif (prop in ["@Head","@Chest","@Arm","@Legs","@Tail"]):
                    if (beastnum >= 0):
                        if ( detail != "" ):
                            try:
                                piece = c.getEquipment(detail)
                            except Exception:
                                raise Exception("[Line " + str(linenum) + "] " + EX_INVALID_EQUIPMENT + " (" + piece.name + ")")
                                
                            if (piece.part == team.beasts[beastnum].anatomy.parts[equipmentcntr]):
                                team.beasts[beastnum].equipItem(piece)
                            else:
                                raise Exception("[Line " + str(linenum) + "] Item '" + piece.name + "' does not match the limb '" +  team.beasts[beastnum].anatomy.parts[equipmentcntr] + "'")
                        equipmentcntr += 1
                    else:
                        raise Exception("[Line " + str(linenum) + "] " + EX_MISSINGSPECIES)
                else:
                        raise Exception("[Line " + str(linenum) + "] " + EX_INVALID_PROPERTY + " (" + line + ")")

    #Check validity and move beasts to subs where necessary based on format
    if (battleformat == ""):
        raise Exception(EX_MISSING_FORMAT)
    elif (battleformat == "Doubles"):
        teamlim = 2
        if (len(team.beasts) > teamlim):
            for beast in team.beasts[teamlim:]:
                team.subs.append(beast)
                team.beasts.pop()
        pass
    
    return team