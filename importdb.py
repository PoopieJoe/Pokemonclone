import csv
import classes

def importAttacks(filepath):
    attacks = []
    with open(filepath,"rt",encoding="utf-8") as f:
        reader = csv.DictReader(f)

        for row in reader:
            newattack = classes.Attack(
                atkid=int(row["ID"]),
                name=row["Name"],
                physPower=float(row["Physical power"]),
                heatPower=float(row["Heat power"]),
                coldPower=float(row["Cold power"]),
                shockPower=float(row["Shock power"]),
                accuracy=float(row["Accuracy"]),
                critRate=float(row["Crit rate"]),
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
            newequipment = classes.Equipment(
                equipmentid=int(row["ID"]),
                name=row["Name"], 
                part=row["Part"],
                attacks=[int(attack) for attack in row["Attacks"].split(",") if attack != ""], 
                addmaxHP=int(row["added maxHP"]),
                maxHPmult=float(row["maxHP multiplier"]),
                addphysATK=int(row["added ATK"]),
                physATKmult=float(row["ATK multiplier"]),
                addphysDEF=int(row["added DEF"]),
                physDEFmult=float(row["DEF multiplier"]),
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
            newanatomy = classes.Anatomy(
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
            newspecies = classes.Species(
                monid=int(row["ID"]), 
                name=row["Name"], 
                anatomy=int(row["Anatomy"]),
                maxHP=int(row["maxHP"]),
                physATK=int(row["physATK"]), 
                physDEF=int(row["physDEF"]), 
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