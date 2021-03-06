import csv
from pathlib import Path
from math import floor
from globalconstants import *

class Beast:
    "Describes an ingame beast, complete with stats and equipment"
    def __init__(self, species, nickname = None, loadout = []):
        #details
        self.species = getSpecies(species)
        if (nickname == None):
            self.nickname = species.name
        else:
            self.nickname = nickname

        #stats
        self.maxHP = self.species.maxHP
        self.HP = self.species.maxHP
        self.physATK = self.species.physATK
        self.armor = self.species.armor
        self.magATK = self.species.magATK
        self.RES = [1-(100/self.armor),self.species.heatRES,self.species.coldRES,self.species.shockRES]
        self.SPE = self.species.SPE

        #status
        self.isalive = False
        self.statuseffects = []

        self.attacks = []
        self.selected_attack = [None,0]

        #Equipment
        if (loadout == []): #an empty loadout
            for limb in getAnatomy(self.species.anatomy).parts:
                loadout.append(None)

        if (len(loadout) != len(getAnatomy(self.species.anatomy).parts)):
            raise Exception("number of loadout items does not match the number of limbs")
            
        self.equipment = []
        for n,piece in enumerate(loadout):
            if (piece != None):
                piece = getEquipment(piece)
                if (piece.part == getAnatomy(self.species.anatomy).parts[n]):
                    self.equipItem(piece)
                else:
                    raise Exception("Item " + piece.part + " does not match the limb part " + getAnatomy(self.species.anatomy).parts[n])

        #Flags
        self.flags = [["execute_attack",False],["choose_attack",False]]

    def calcBurnDMG(self):
        dmgpertick = BURNDMG*self.maxHP*100/TURNTRACKER_LENGTH
        return (max(1,floor(dmgpertick)), max(1,floor(1/dmgpertick)))

    def selectattack(self,atk_id):
        print(str(self.nickname) + " selected " + self.attacks[atk_id].name + " as their attack!")
        try:
            self.selected_attack[0] = self.attacks[atk_id]
            return True
        except Exception:
            return False
        
    
    def selecttarget(self,scene,slot):
        print(str(self.nickname) + " selected " + str(scene.beasts[slot].nickname) + " as the target!")
        try:
            self.selected_attack[1] = slot
            return True
        except Exception:
            return False
    
    def setchainattack(self,atk_id):
        self.selected_attack[0] = ATTACKS[atk_id]

    def addstatuseffect(self,effect):
        self.statuseffects.append(effect)

    def death(self):
        self.HP = 0
        self.SPE = 0
        self.isalive = False

    def getflag(self,flag):
        return self.flags[flag][1]

    def setflag(self,flag):
        self.flags[flag][1] = True

    def clearflag(self,flag):
        self.flags[flag][1] = False

    def clearALLflags(self):
        for flag in self.flags:
            flag[1] = False

    def equipItem(self,equipment):
        self.equipment.append(equipment)
        #TODO remake this
        #for bonus in equipment.statbonuses:
        #    if (bonus[0] == "maxHP"):
        #        self.maxHP += bonus[1]
        #    elif (bonus[0] == "ATK"):
        #        self.ATK += bonus[1]
        #    elif (bonus[0] == "SPE"):
        #        self.SPE += bonus[1]
        #    elif (bonus[0] == "DEF"):
        #        self.DEF += bonus[1]
        #    elif (bonus[0] == "heatRES"):
        #        self.heatRES += bonus[1]
        #    elif (bonus[0] == "coldRES"):
        #        self.coldRES += bonus[1]
        #    elif (bonus[0] == "shockRES"):
        #        self.shockRES += bonus[1]
        
        for attack in equipment.attacks:
            if (attack not in self.attacks):
                self.attacks.append(getAttack(attack))

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
        effects
    ):
        self.id = atkid
        self.name = name
        self.power = [physPower,heatPower,coldPower,shockPower]
        self.accuracy = accuracy
        self.critRate = critRate
        self.flags = flags
        self.effects = effects

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
                effects=[effect for effect in row["Effects"].split(",") if effect != ""]
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

dbpath = "./database/"
ATTACKS = importAttacks(Path(dbpath+"attacks.csv"))
EQUIPMENT = importEquipment(Path(dbpath+"equipment.csv"))
ANATOMIES = importAnatomies(Path(dbpath+"anatomies.csv"))
SPECIES = importSpecies(Path(dbpath+"species.csv"))