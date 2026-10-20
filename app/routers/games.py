from fastapi import APIRouter, Depends, status
from app.schemas.games import CreateGameSchema,UpdateGameSchema,GameResponseSchema
from app.core.secure import verify_admin
from app.services.steam_scrapper import refresh_games
from app.services.game import create, update, search, delete
from app.services.cheap_shark import cheap_shark_search

jogos_teste = [
    "Call of Duty®: Modern Warfare® 4",
    "AION 2",
    "Dota 2",
    "Counter-Strike 2",
    "EA SPORTS FC™ 27",
    "Dead by Daylight",
    "Cyberpunk 2077",
    "Battlefield™ 6",
    "Red Dead Redemption 2",
    "Enshrouded",
    "WARDOGS",
    "Aniimo",
    "PUBG: BATTLEGROUNDS",
    "HELLDIVERS™ 2",
    "Grand Theft Auto V Enhanced",
    "RuneScape: Dragonwilds",
    "eFootball™",
    "Torchlight: Infinite",
    "Hogwarts Legacy",
    "We Were Here Tomorrow",
    "Cyberpunk 2077: Phantom Liberty",
    "Dressmaker",
    "Warframe",
    "Phantom Blade Zero",
    "Street Fighter™ 6",
    "DayZ",
    "FINAL FANTASY RESONANCE",
    "DayZ Badlands",
    "Marvel Rivals",
    "Castlevania: Belmont's Curse",
    "THE FINALS",
    "Warhammer 40,000: Space Marine 2",
    "007 First Light",
    "Batman™: Arkham Knight",
    "Risk of Rain 2",
    "SnowRunner",
    "Fallout 4",
    "Mortal Kombat 1",
    "ARC Raiders",
    "ELDEN RING",
    "Microsoft Flight Simulator 2024",
    "Overwatch®",
    "iRacing",
    "REMATCH",
    "over the hill",
    "NBA 2K27",
    "Wuthering Waves",
    "Palworld",
    "GrandChase",
    "LEGO® Batman™: O Legado do Cavaleiro das Trevas",
    "Mortal Kombat 11",
    "Planet Zoo 2",
    "Project Zomboid",
    "FINAL FANTASY XIV Online",
    "BOMBANANA!",
    "Arena Breakout: Infinite",
    "Dragon's Dogma 2",
    "No Rest for the Wicked",
    "Battlefield™ REDSEC",
    "EA SPORTS FC™ 26",
    "Silver Pines",
    "Wallpaper Engine",
    "Stardew Valley",
    "Forza Horizon 6",
    "Empires of the Undergrowth",
    "Diablo® IV",
    "Fallout 76",
    "Middle-earth™: Shadow of War™",
    "Fallout: New Vegas",
    "EA Play",
    "The Elder Scrolls® Online",
    "ARC Raiders - Frozen Trail Collector Set",
    "Euro Truck Simulator 2",
    "Tom Clancy's Rainbow Six Siege",
    "Stranded Deep",
    "The Sims™ 4",
    "ARK: Survival Evolved",
    "Once Human",
    "Delta Force",
    "STAR WARS: Galactic Racer™",
    "F1® 25",
    "ARK: Survival Ascended",
    "Crimson Desert Enhanced",
    "Baldur's Gate 3",
    "American Truck Simulator",
    "Black Desert",
    "How to Fish",
    "Core Keeper",
    "Call of Duty®: Warzone™",
    "Everything is Crab: The Animal Evolution Roguelite",
    "Path of Exile 2",
    "Ravenswatch",
    "Brawlhalla",
    "Risk of Rain 2: Hallowed Concepts",
    "Outward Definitive Edition",
    "War Thunder",
    "Street Fighter 30th Anniversary Collection",
    "Rust",
    "Magic: The Gathering Arena",
    "Atomic Heart"
]

games_router = APIRouter(prefix="/games",tags=["Jogos"])

@games_router.get("/{name}", status_code=status.HTTP_200_OK)
async def search_game(name : str):
    return await search(name)

@games_router.post("", status_code=status.HTTP_201_CREATED, response_model=GameResponseSchema)
async def create_game(game : CreateGameSchema, admin_user = Depends(verify_admin)):
    return await create(game)

@games_router.patch("/{game_id}", status_code=status.HTTP_200_OK, response_model=GameResponseSchema)
async def update_game(game_id : str, update_data : UpdateGameSchema, admin_user = Depends(verify_admin)):
    return await update(game_id,update_data)

@games_router.delete("/{game_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_game(game_id : str, admin_user = Depends(verify_admin)):
    return await delete(game_id)

@games_router.get("", status_code=status.HTTP_200_OK)
async def refresh_games_database():
    return cheap_shark_search(jogos_teste)
