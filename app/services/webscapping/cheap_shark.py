from fastapi import HTTPException
from steam_scrapper import get_developer
from app.schemas.games import CreateGameSchema
import requests
import time

cheap_shark_url = "https://www.cheapshark.com/api/1.0/games"
headers = {"User-Agent": "GameSpotApp/1.0 (williammaxbcc4794@gmail.com)"}

def cheap_shark_search(top_games):
    top_games_info = []

    for game in top_games:
        max_tries = 3
        tries = 0
        time_stamp = 1
        for tries in range(max_tries):
            time.sleep(time_stamp)
            response = requests.get(cheap_shark_url, params={"title": game}, headers=headers)
            print(response.status_code)
            if response.status_code == 200:
                data = response.json()
                game_cheap_id = ""
                if len(data) == 1:
                    game_cheap_id = data.get("gameID")
                elif len(data) > 1:
                    game_cheap_id = data[0].get("gameID")
                else:
                    game_cheap_id = "None"
                    top_games_info.append("None")
                    break
                top_games_info.append(game_cheap_id)
                break
            elif response.status_code == 429:
                time_stamp *= 2
            else:
                raise HTTPException(status_code=response.status_code,detail="ERROR: Erro in games search")

def id_search(game_id):
    response = requests.get(cheap_shark_url, params={"id": game_id}, headers=headers)
    data = response.json()

    prices = []

    game = CreateGameSchema(
        title=data["info"]["title"],
        all_time_cheapest_price=data["cheapestPriceEver"]["price"],
        developer=get_developer(data["steamAppID"])

    )

