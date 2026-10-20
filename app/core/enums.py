from enum import Enum, auto

class StoresEnum(Enum):
    GOG = "GOG"
    GreenManGaming = "GreenManGaming"
    Steam = "Steam"
    EpicGames = "EpicGames"

class TokenTypesEnum(Enum):
    Access_Token = "Access_Token"
    Refresh_Token = "Refresh_Token"