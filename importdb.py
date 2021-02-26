import csv
import classes

database_filepath = "database"
attacks_filename = "attacks.csv"

def importAttacks():
    f = open(str(database_filepath)+"/"+str(attacks_filename),"rt",encoding="utf-8")
    reader = csv.DictReader(f)

    Attacks = []
    for row in reader:
        #print(row["ID"],row["Name"])
        newattack = classes.Attack(
            atkid=row["ID"],
            name=row["Name"],
            physPower=row["Physical power"],
            heatPower=row["Heat power"],
            coldPower=row["Cold power"],
            shockPower=row["Shock power"],
            accuracy=["Accuracy"],
            critRate=row["Crit rate"],
            flags=row["Flags"],
            effects=row["Effects"])
        Attacks.append(newattack)

    return Attacks