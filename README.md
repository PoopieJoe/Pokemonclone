# Pokemonclone (initial draft)
 
Beasts:

Description:
Wicked monsters with wide-ranging animalistic body types (think hydra, chimera, centipede, humanoid, snakelike, fishlike, etc.)  

Equipment:  
Each beast has body parts unique to its type.  
e.g. humanoids have a headpiece, two armpieces, a chestpiece and a legpiece  
hydras have multiple headpieces, a chestpiece and a tailpiece  
etc...  

(Almost) every body part can equip a piece of equipment.  
Each beast also has a unique set of stats  

Stats:  

	Health Points (positive integer)  
		fragile: 1-200
		midrange: 200-400
		healthy: 400-600
		fat: 600+

	ATtacK (positive integer)
		weak: 50
		average: 100
		strong: 150

	RESistance (positive/negative percentage)
		One for each element [Physical,Heat,Cold,Shock]
		vulnerable: -100% (take 200% dmg)
		average: 0% (take normal dmg)
		resistant: +50% (take 50% dmg)
		immune: +100% (take 0% dmg)
		absorbant: +150% (heal for 50% dmg)

	SPEed (positive integer)
		dead slow: 50 (half as many turns as average)
		slow: 80 (20% less turns as average)
		average: 100
		fast: 120% (20% more turns as average)
		lightning fast: 200 (twice as many turns as average)

################################################################  
Equipment  
Equipment provides bonuses to stats, attacks for the beast to use, or additional effects.  

e.g. a headpiece can provide extra Heat resistance, as well a a fiery breath attack  
a chestpiece can provide extra HP and physical resistance.  
an armpiece that empowers attacks, but inflicts physical self damage when an attack is used.  
a legpiece that gives a healing attack, but reduces Cold resistance.  
a wingpiece that gives Shock immunity, but reduces the SPE stat by half.  
etc...  

################################################################  
Basic attack structure  

	Power (positive percentage):  
		weak: 50%  
		average: 100%  
		strong: 150%  

	Element:
		One of Physical,Heat,Cold,Shock

	Accuracy(?)
		inaccurate: 80%
		base: 100%
		accurate: 120%


################################################################
Damage calc

	Hit if ( random(0,99.9%) < (Accuracy * modifier) )
	DMG = [ATacK]*[Power]*(1-[elemental RESistance]) * [modifier 1] * [modifier 2] * ...
	True damage? (unresisted dmg)