from globalconstants import *
import teamimport as timport
import classes as c

class TeamController:
    def __init__(self) -> None:
        pass    
        
    def fetchteam(self,path) -> c.Team:
        return timport.importteam(path)