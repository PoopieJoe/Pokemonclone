#### Gameplay-related constants

# Elements
ELEMENTS = ["physical","heat","cold","shock"]

# Under the hood constants
TURNTRACKER_LENGTH = 20000 #time unit for 1 full turn (between move selections). Since monsters move their speed every tick, at average speed of 100, it takes 100 ticks from move selection to attack, and 100 ticks from attack back to move selection

# Randomness
attackroll_randmod = 0.1 #attacks deal randomly between 90% and 110% dmg
critchance = 0.05 #5% critchance
critmulti = 1.5 #critical hit dmg multiplier

# Status effects
BURNNAME = "Burn"
BURNDMG = 1/8 #dmg per turn

SLOWNAME = "Slow"
SLOWMOD = 0.8 #speed multiplier during slow