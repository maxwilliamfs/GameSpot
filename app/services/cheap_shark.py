import requests
from app.schemas.games import CreateGameSchema
cheap_shark_url = "https://www.cheapshark.com/api/1.0/games"
headers = {"User-Agent": "GameSpotApp/1.0 (williammaxbcc4794@gmail.com)"}

def cheap_shark_search(top_games):
    top_games_id = []

    for game in top_games:
        response = requests.get(cheap_shark_url,params={"title" : game},headers=headers)
        if response.status_code == 200:
            result = response.json()
            if isinstance(result, list) and len(result) > 0:
                first_game = result[0]
                top_games_id.append(first_game.get("gameID"))
            else:
                top_games_id.append(None)

    for game in top_games_id:
        new_game = CreateGameSchema(
            
        )


def steam_search(game_id):
    pass

def green_man_gaming_search(game_id):
    pass

def gog_search(game_id):
    pass

def epic_games_search(game_id):
    pass