import csv
from globalconstants import *
import classes as c

def getAttack(dbfilepath,id):
    with open(dbfilepath,"rt",encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row["ID"] == id or row["Name"] == id:
                return {
                    "atkid":int(row["ID"]),
                    "name":row["Name"],
                    "physPower":float(row["Physical power"]),
                    "heatPower":float(row["Heat power"]),
                    "coldPower":float(row["Cold power"]),
                    "shockPower":float(row["Shock power"]),
                    "accuracy":float(row["Accuracy"]),
                    "critRate":float(row["Crit rate mod"]),
                    "flags":[flag for flag in row["Flags"].split(",") if flag != ""],
                    "effects":[effect for effect in row["Effects"].split(",") if effect != ""],
                    "chainID": -1 if row["ChainID"]=="" else int(row["ChainID"]),
                    "tooltip":[str(text) for text in row["Tooltip"].split("\\n") ]
                    }

    raise Exception("Invalid Attackid given: " + id)
