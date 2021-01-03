from math import floor

def printFullBeastStatus(beasts):
    for beast in beasts:
        print("---")
        healthpercentage = floor(beast.HP/beast.maxHP*100)
        print( str(beast.name) + ": \n" + str(beast.HP) + "/" + str(beast.maxHP) + " HP (" + str(healthpercentage) + "%)\n" )
        print( "ATK: " + str(beast.ATK))
        print( "DEF: " + str(beast.DEF))
        print( "heatRES: " + str(beast.heatRES*100) + "%")
        print( "coldRES: " + str(beast.coldRES*100) + "%")
        print( "shockRES: " + str(beast.shockRES*100) + "%")
        print( "SPE: " + str(beast.SPE))
        print("\nEquipment:")
        for equipment in beast.equipment:
            print(equipment.name)
            #printEquipment(equipment)
    print("---")
    return

def printEquipment(equipment):
    print(equipment.name)
    for bonus in equipment.statbonuses:
        print(str(bonus[0]) + ": " + str(bonus[1]))
    print("\nAttacks: ")
    for attack in equipment.attacks:
        print(attack.name)
        #printAttack(attack)
    return

def printAttack(attack):
    print(attack.name)
    print("Power: " + str(attack.power))
    print("Element: " + str(attack.element))
    print("Accuracy: " + str(attack.accuracy))
    return