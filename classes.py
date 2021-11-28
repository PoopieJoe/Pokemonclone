import csv
from pathlib import Path
from math import floor
from fnmatch import fnmatch
from globalconstants import *

class Flag:
    def __init__(self, type, raised):
        self.slot = -1
        self.type = type
        self.raised = raised

    def raisee(self):
        self.raised = True

    def clear(self):
        self.raised = False

    def israised(self):
        return self.raised

class SelectedAtk:
    def __init__(self, attack, slot):
        self.atk = attack
        self.slot = slot

class Beast:
    "Describes an ingame beast, complete with stats and equipment"
    def __init__(self, species, nickname = None, loadout = []):
        #details
        self.species = getSpecies(species)
        if (nickname == None):
            self.nickname = self.species.name
        else:
            self.nickname = nickname
        self.anatomy = getAnatomy(self.species.anatomy)

        #stats
        self.maxHP = self.species.maxHP
        self.HP = self.species.maxHP
        self.physATK = self.species.physATK
        self.armor = self.species.armor
        self.magATK = self.species.magATK
        self.SPE = self.species.SPE
        self.heatRES = self.species.heatRES
        self.coldRES = self.species.coldRES
        self.shockRES = self.species.shockRES
        self.calcRES()

        #status
        self.isalive = False
        self.statuseffects = []
        self.equipmentflags = []

        self.attacks = []
        self.selected_attack = SelectedAtk(None,-1)

        #Equipment
        if (loadout == []): #an empty loadout
            for _ in self.anatomy.parts:
                loadout.append(None)
        else:
            if (len(loadout) != len(self.anatomy.parts)):
                raise Exception("number of loadout items does not match the number of limbs")
            
        self.equipment = []
        for n,piece in enumerate(loadout):
            if (piece != None):
                piece = getEquipment(piece)
                if (piece.part == self.anatomy.parts[n]):
                    self.equipItem(piece)
                else:
                    raise Exception("Item " + piece.part + " does not match the limb part " + self.anatomy.parts[n])

        #Flags
        self.flags = [Flag("execute_attack",False),Flag("choose_attack",False)]
    
    def validityCheck(self):
        #TODO: check if build is legal
        return True

    def calcRES(self):
        self.RES = [1-(100/self.armor),self.heatRES,self.coldRES,self.shockRES]
        return

    def calcBurnDMG(self):
        dmgpertick = BURNDMG*self.maxHP*100/TURNTRACKER_LENGTH*(1-self.RES[1])

        if (abs(dmgpertick) < 1): 
            outdmgpertick = floor(dmgpertick/abs(dmgpertick)) #preserve sign and set to 1
        else:
            outdmgpertick = floor(dmgpertick)

        if (self.RES[1] == 1): #immunity to fire
            outticksperdmg = 1
        else:
            outticksperdmg = max(1,floor(1/dmgpertick))
        return (outdmgpertick, outticksperdmg)

    def selectattack(self,atk_id):
        print(str(self.nickname) + " selected " + str(self.attacks[atk_id].name) + " as their attack!")
        try:
            self.selected_attack.atk = self.attacks[atk_id]
            return True
        except Exception:
            return False
    
    def selecttarget(self,scene,slot):
        #check current attack
        attack = self.selected_attack.atk
        for flag in attack.flags:
            if (flag == TARGETOTHER):
                targetslots = [scene.slots[slot]]
            elif (flag == TARGETTEAM):
                if (slot == 0 or slot == 2):
                    otherslot = slot + 1
                else:
                    otherslot = slot - 1
                targetslots = [scene.slots[slot],scene.slots[otherslot]]
            elif (flag == TARGETALLOTHER):
                targetslots = scene.slots
                targetslots.pop(self) 
            else:
                pass

        
        print(str(self.nickname) + " selected " + " and ".join([slot.beast.nickname for slot in targetslots]) + " as the target(s)!")
        try:
            self.selected_attack.slots = targetslots
            return True
        except Exception:
            return False
    
    def setchainattack(self,atk_id):
        self.selected_attack.atk = ATTACKS[atk_id]

    def addstatuseffect(self,effect):
        self.statuseffects.append(effect)

    def death(self):
        self.HP = 0
        self.SPE = 0
        self.isalive = False

    def getflag(self,flagtype):
        for flag in self.flags:
            if flag.type == flagtype:
                return flag.israised()

    def setflag(self,flagtype):
        for flag in self.flags:
            if flag.type == flagtype:
                flag.raisee()

    def clearflag(self,flagtype):
        for flag in self.flags:
            if flag.type == flagtype:
                flag.clear()

    def clearALLflags(self):
        for flag in self.flags:
            flag.clear()

    def equipItem(self,equipment):
        self.equipment.append(equipment)

        self.maxHP = round(self.maxHP*equipment.maxHPmult)
        self.physATK *= equipment.physATKmult
        self.armor *= equipment.armormult
        self.magATK *= equipment.magATKmult
        self.heatRES *= equipment.heatRESmult
        self.coldRES *= equipment.coldRESmult
        self.shockRES *= equipment.shockRESmult
        self.SPE *= equipment.SPEmult

        self.maxHP += equipment.addmaxHP
        self.physATK += equipment.addphysATK
        self.armor += equipment.addarmor
        self.magATK += equipment.addmagATK
        self.heatRES += equipment.addheatRES
        self.coldRES += equipment.addcoldRES
        self.shockRES += equipment.addshockRES
        self.SPE += equipment.addSPE
        
        self.calcRES()

        #TODO set flags and effects

        for attackid in equipment.attacks:
            attack = getAttack(attackid)
            if (attack.name not in [x.name for x in self.attacks]):
                self.attacks.append(attack)

class Anatomy:
    def __init__(
        self,
        anatomyid,
        name,
        parts,
    ):
        self.id = anatomyid
        self.name = name
        self.parts = parts

class Equipment:
    def __init__(
        self, 
        equipmentid,
        name, 
        part,
        attacks, 
        addmaxHP,
        maxHPmult,
        addphysATK,
        physATKmult,
        addarmor,
        armormult,
        addmagATK,
        magATKmult,
        addheatRES,
        heatRESmult,
        addcoldRES,
        coldRESmult,
        addshockRES,
        shockRESmult,
        addSPE,
        SPEmult,
        flags,
        effects
    ):
        #ID,Name,Part,Attacks,max HP,ATK add,ATK mult,DEF add,Def mult,heatRES add,heatRES mult,coldRES add,coldRES mult,shockRES add,shockRES mult,SPE add,SPE mult,Flags,Effects
        self.id = equipmentid
        self.name = name
        self.part = part
        self.attacks = attacks
        self.addmaxHP = addmaxHP
        self.maxHPmult = maxHPmult
        self.addphysATK = addphysATK
        self.physATKmult = physATKmult
        self.addarmor = addarmor
        self.armormult = armormult
        self.addmagATK = addmagATK
        self.magATKmult = magATKmult
        self.addheatRES = addheatRES
        self.heatRESmult = heatRESmult
        self.addcoldRES = addcoldRES
        self.coldRESmult = coldRESmult
        self.addshockRES = addshockRES
        self.shockRESmult = shockRESmult
        self.addSPE = addSPE
        self.SPEmult = SPEmult
        self.flags = flags
        self.effects = effects

class Attack:
    def __init__(
        self, 
        atkid, 
        name, 
        physPower, 
        heatPower, 
        coldPower, 
        shockPower, 
        accuracy, 
        critRate, 
        flags, 
        effects,
        chainid,
        tooltip
    ):
        self.id = atkid
        self.name = name
        self.power = [physPower,heatPower,coldPower,shockPower]
        self.accuracy = accuracy
        self.critRate = critRate
        self.flags = flags
        self.effects = []
        self.chainid = chainid
        for effect in effects:
            neweffect = {
                "name": "",
                "value": 0,
                "chance": 1
            }
            if fnmatch(effect, "*_*(*)"):   #format: NAME_VALUE(CHANCE)
                underscorepos = effect.index('_')
                openparenpos = effect.index('(')
                closeparenpos = effect.index(')')
                neweffect["name"] = effect[:underscorepos]
                neweffect["value"] = int(effect[underscorepos+1:openparenpos])
                neweffect["chance"] = float(effect[openparenpos+1:closeparenpos])
            elif fnmatch(effect, "*_*"):    #format: NAME_VALUE
                underscorepos = effect.index('_')
                neweffect["name"] = effect[:underscorepos]
                neweffect["value"] = int(effect[underscorepos+1:])
            elif fnmatch(effect, "*(*)"):   #format: NAME(CHANCE)
                openparenpos = effect.index('(')
                closeparenpos = effect.index(')')
                neweffect["name"] = effect[:openparenpos]
                neweffect["chance"] = float(effect[openparenpos+1:closeparenpos])
            else:
                raise Exception("Effect '" + effect + "' follows invalid format")
            self.effects.append(neweffect)
            
        self.tooltip = tooltip

class Species:
    def __init__(
        self, 
        monid, 
        name, 
        anatomy,
        maxHP,
        physATK, 
        armor, 
        magATK,
        heatRES, 
        coldRES, 
        shockRES, 
        SPE, 
        ability, 
        flags
    ):
        self.id = monid
        self.name = name
        self.anatomy = anatomy
        self.maxHP = maxHP
        self.physATK = physATK
        self.armor = armor
        self.magATK = magATK
        self.heatRES = heatRES
        self.coldRES = coldRES
        self.shockRES = shockRES
        self.SPE = SPE
        self.ability = ability
        self.flags = flags

class StaticText:
    def __init__(
        self,
        tag,
        text
    ):
        self.tag = tag
        self.text = text

def getAttack(ID):
    """Returns the attack object by ID or by full name string"""
    if (isinstance(ID,int)):
        return ATTACKS[ID]
    elif (isinstance(ID,str)):
        for attack in ATTACKS:
            if (attack.name == ID):
                return attack
    else:
        raise Exception("Attack " + ID + " does not exist")

def getEquipment(ID):
    """Returns the equipment object by ID or by full name string"""
    if (isinstance(ID,int)):
        return EQUIPMENT[ID]
    elif (isinstance(ID,str)):
        for equipment in EQUIPMENT:
            if (equipment.name == ID):
                return equipment
    else:
        raise Exception("Equipment " + ID + " does not exist")

def getAnatomy(ID):
    """Returns the anatomy object by ID or by full name string"""
    if (isinstance(ID,int)):
        return ANATOMIES[ID]
    elif (isinstance(ID,str)):
        for anatomy in ANATOMIES:
            if (anatomy.name == ID):
                return anatomy
    else:
        raise Exception("Anatomy " + ID + " does not exist")

def getSpecies(ID):
    """Returns the species object by ID or by full name string"""
    if (isinstance(ID,int)):
        return SPECIES[ID]
    elif (isinstance(ID,str)):
        for species in SPECIES:
            if (species.name == ID):
                return species
    else:
        raise Exception("Species " + ID + " does not exist")

def getStaticText(tag):
    for entry in STATICTEXT:
        if (entry.tag == tag):
            return entry.text
    else:
        raise Exception("Statictext entry" + tag + " does not exist")

def importAttacks(filepath):
    attacks = []
    with open(filepath,"rt",encoding="utf-8") as f:
        reader = csv.DictReader(f)

        for row in reader:
            newattack = Attack(
                atkid=int(row["ID"]),
                name=row["Name"],
                physPower=float(row["Physical power"]),
                heatPower=float(row["Heat power"]),
                coldPower=float(row["Cold power"]),
                shockPower=float(row["Shock power"]),
                accuracy=float(row["Accuracy"]),
                critRate=float(row["Crit rate mod"]),
                flags=[flag for flag in row["Flags"].split(",") if flag != ""],
                effects=[effect for effect in row["Effects"].split(",") if effect != ""],
                chainid= None if row["ChainID"]=="" else int(row["ChainID"]),
                tooltip=[text for text in row["Tooltip"].split("\\") ]
                )
            attacks.append(newattack)
    return attacks

def importEquipment(filepath):
    equipment = []
    with open(filepath,"rt",encoding="utf-8") as f:
        reader = csv.DictReader(f)
        
        for row in reader:
            newequipment = Equipment(
                equipmentid=int(row["ID"]),
                name=row["Name"], 
                part=row["Part"],
                attacks=[int(attack) for attack in row["Attacks"].split(",") if attack != ""], 
                addmaxHP=int(row["added maxHP"]),
                maxHPmult=float(row["maxHP multiplier"]),
                addphysATK=int(row["added ATK"]),
                physATKmult=float(row["ATK multiplier"]),
                addarmor=int(row["added armor"]),
                armormult=float(row["armor multiplier"]),
                addmagATK=int(row["added magATK"]),
                magATKmult=float(row["magATK multiplier"]),
                addheatRES=float(row["added heatRES"]),
                heatRESmult=float(row["heatRES multiplier"]),
                addcoldRES=float(row["added coldRES"]),
                coldRESmult=float(row["coldRES multiplier"]),
                addshockRES=float(row["added shockRES"]),
                shockRESmult=float(row["shockRES multiplier"]),
                addSPE=int(row["added SPE"]),
                SPEmult=float(row["SPE multiplier"]),
                flags=[flag for flag in row["Flags"].split(",") if flag != ""],
                effects=[effect for effect in row["Effects"].split(",") if effect != ""]
                )
            equipment.append(newequipment)
    return equipment

def importAnatomies(filepath):
    anatomies = []
    with open(filepath,"rt",encoding="utf-8") as f:
        reader = csv.DictReader(f)

        for row in reader:
            newanatomy = Anatomy(
                anatomyid=int(row["ID"]),
                name=row["Name"],
                parts=[part for part in row["Parts"].split(",") if part != ""]
                )
            anatomies.append(newanatomy)

    return anatomies

def importSpecies(filepath):
    species = []
    with open(filepath,"rt",encoding="utf-8") as f:
        reader = csv.DictReader(f)

        for row in reader:
            newspecies = Species(
                monid=int(row["ID"]), 
                name=row["Name"], 
                anatomy=int(row["Anatomy"]),
                maxHP=int(row["maxHP"]),
                physATK=int(row["physATK"]), 
                armor=int(row["armor"]), 
                magATK=int(row["magATK"]),
                heatRES=float(row["heatRES"]), 
                coldRES=float(row["coldRES"]), 
                shockRES=float(row["shockRES"]), 
                SPE=int(row["SPE"]), 
                ability=row["Ability"], 
                flags=[flag for flag in row["Flags"].split(",") if flag != ""],
                )
            species.append(newspecies)

    return species

def importStatictext(filepath):
    statictext = []
    with open(filepath,"rt",encoding="utf-8") as f:
        reader = csv.DictReader(f)

        for row in reader:
            newstatictext = StaticText(
                tag = row["Tag"],
                text = [text for text in row["Text"].split("\\") ]
                )
            statictext.append(newstatictext)

    return statictext

dbpath = "./database/"
ATTACKS = importAttacks(Path(dbpath+"attacks.csv"))
EQUIPMENT = importEquipment(Path(dbpath+"equipment.csv"))
ANATOMIES = importAnatomies(Path(dbpath+"anatomies.csv"))
SPECIES = importSpecies(Path(dbpath+"species.csv"))
STATICTEXT = importStatictext(Path(dbpath+"statictext.csv"))