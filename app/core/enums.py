from enum import Enum, auto

class StoresEnum(Enum):
    GOG = "GOG"
    GreenManGaming = "GreenManGaming"
    Steam = "Steam"
    EpicGames = "EpicGames"

class StoreIDEnum(Enum):
    GOG = 7
    GreenManGaming = 3
    Steam = 1
    EpicGames = 25

class TokenTypesEnum(Enum):
    Access_Token = "Access_Token"
    Refresh_Token = "Refresh_Token"