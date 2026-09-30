from enum import Enum, auto

class StoresEnum(Enum):
    Xbox = "Xbox"
    Playstation = "Playstation"
    Steam = "Steam"
    Nintendo = "Nintendo"
    EpicGames = "EpicGames"

class TokenTypesEnum(Enum):
    Access_Token = "Access_Token"
    Refresh_Token = "Refresh_Token"