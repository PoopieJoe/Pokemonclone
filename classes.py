class Beast:
    "Describes an ingame beast, complete with stats and equipment"
    def __init__(self, name = "none", species = "none", maxHP = 1, ATK = 0, DEF = 1, heatRES = 0, coldRES = 0, shockRES = 0, SPE = 0):
        #details
        self.species = species
        self.name = name

        #basestats --> move these to a species list
        self.baseMaxHP = maxHP
        self.baseATK = ATK
        self.baseDEF = DEF
        self.baseHeatRES = heatRES
        self.baseColdRES = coldRES
        self.baseShockRES  = shockRES
        self.baseSPE = SPE

        #stats
        self.maxHP = self.baseMaxHP
        self.HP = self.maxHP
        self.ATK = self.baseATK
        self.DEF = self.baseDEF
        self.heatRES = self.baseHeatRES
        self.coldRES = self.baseColdRES
        self.shockRES = self.baseShockRES
        self.SPE = self.baseSPE

        #status
        self.isalive = False
        self.statuseffects = []

        self.attacks = []
        self.selected_attack = [None,0]

        #Equipment
        self.equipmentslots = []
        self.equipment = []

        #Flags
        self.flags = [["execute_attack",False],["choose_attack",False]]

    def selectattack(self,atk_id):
        self.selected_attack[0] = self.attacks[atk_id]
        print(str(self.name) + " selected " + self.selected_attack[0].name)
    
    def selecttarget(self,scene,slot):
        self.selected_attack[1] = slot
        print(str(self.name) + " selected " + str(scene.beasts[slot].name))

    def addstatuseffect(self,name):
        self.statuseffects.append(name)

    def death(self):
        self.HP = 0
        self.SPE = 0
        self.isalive = False

    def setflag(self,flag):
        self.flags[flag][1] = True

    def clearflag(self,flag):
        self.flags[flag][1] = False

    def clearALLflags(self):
        for flag in self.flags:
            flag[1] = False

    def equipItem(self,equipment):
        self.equipment.append(equipment)
        for bonus in equipment.statbonuses:
            if (bonus[0] == "maxHP"):
                self.maxHP += bonus[1]
            elif (bonus[0] == "ATK"):
                self.ATK += bonus[1]
            elif (bonus[0] == "SPE"):
                self.SPE += bonus[1]
            elif (bonus[0] == "DEF"):
                self.DEF += bonus[1]
            elif (bonus[0] == "heatRES"):
                self.heatRES += bonus[1]
            elif (bonus[0] == "coldRES"):
                self.coldRES += bonus[1]
            elif (bonus[0] == "shockRES"):
                self.shockRES += bonus[1]
        
        for attack in equipment.attacks:
            if (attack not in self.attacks):
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
        addphysDEF,
        physDEFmult,
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
        self.addphysDEF = addphysDEF
        self.physDEFmult = physDEFmult
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
        self.physPower = physPower
        self.heatPower = heatPower
        self.coldPower = coldPower
        self.shockPower = shockPower
        self.accuracy = accuracy
        self.critRate = critRate
        self.flags = flags
        self.effects = effects