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
    ex_missingcolon = "Line has no property or is missing a colon."
    ex_missingspecies = "Beast has no species."
    ex_invalid_property = "Invalid property."
    ex_invalid_equipment = "Invalid equipment given."
    ex_invalid_species = "Invalid species given."
    ex_missing_format = "No battle format given."
    ex_invalid_format = "Invalid format given."

    teamreader = open( file , "rt" )

    team = s.Team()
    battleformat = ""
    beastnum = -1
    equipmentcntr = 0
    for linenum, line in enumerate(teamreader.readlines()):
        if (line[0] != '-'):
            if (len(line) > 1):
                colonpos = line.find(':')
                if colonpos < 0:
                    raise Exception("[Line " + str(linenum) + "] " + ex_missingcolon + " (" + line + ")")
                prop = line[0:colonpos]
                detail = line[colonpos+1:len(line)].replace('\n','').strip()
                
                if (prop == "Team name"):
                    team.name = detail
                elif (prop == "Format"):
                    if (detail in ["Doubles"]):
                        battleformat = detail
                    else:
                        raise Exception("[Line " + str(linenum) + "] " + ex_invalid_format)
                elif (prop == "Species"):
                    try:
                        beastnum += 1
                        equipmentcntr = 0
                        newbeast = c.Beast(detail,None,[])
                        team.beasts.append(newbeast)
                    except Exception:
                        raise Exception("[Line " + str(linenum) + "] " + ex_invalid_species)
                elif (prop == "Name"):
                    if (beastnum >= 0):
                        team.beasts[beastnum].nickname = detail
                    else:
                        raise Exception("[Line " + str(linenum) + "] " + ex_missingspecies)
                elif (prop in ["@Head","@Chest","@Arm","@Legs","@Tail"]):
                    if (beastnum >= 0):
                        try:
                            if ( detail != "" ):
                                piece = c.getEquipment(detail)
                                if (piece.part == team.beasts[beastnum].anatomy.parts[equipmentcntr]):
                                    team.beasts[beastnum].equipItem(piece)
                                else:
                                    raise Exception("[Line " + str(linenum) + "] Item '" + piece.name + "' does not match the limb '" +  team.beasts[beastnum].anatomy.parts[equipmentcntr] + "'")
                            equipmentcntr += 1
                        except Exception:
                            raise Exception("[Line " + str(linenum) + "] " + ex_invalid_equipment + " (" + piece.name + ")")
                    else:
                        raise Exception("[Line " + str(linenum) + "] " + ex_missingspecies)
                else:
                        raise Exception("[Line " + str(linenum) + "] " + ex_invalid_property + " (" + line + ")")

    #Check validity and move beasts to subs where necessary based on format
    if (battleformat == ""):
        raise Exception(ex_missing_format)
    elif (battleformat == "Doubles"):
        teamlim = 2
        if (len(team.beasts) > teamlim):
            for beast in team.beasts[teamlim:]:
                team.subs.append(beast)
                team.beasts.pop()
        pass
    
    return team