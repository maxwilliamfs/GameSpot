from app.core.conf import Settings

from fastapi import HTTPException
from app.schemas.games import CreateGameSchema,StorePriceDetails
from app.core.enums import StoresEnum,StoreIDEnum
from app.services.webscapping.steam_api import get_developer
import requests
import time
from app.services.game import create
import asyncio
cheap_shark_url = "https://www.cheapshark.com/api/1.0/games"
headers = {"User-Agent": f"GameSpotApp/1.0 {Settings.USER_EMAIL}"}

async def cheap_shark_search(top_games):
    top_games_ids = []
    for game in top_games:
        max_tries = 3
        tries = 0
        time_stamp = 1
        for tries in range(max_tries):
            await asyncio.sleep(time_stamp)
            response = requests.get(cheap_shark_url, params={"title": game}, headers=headers)
            print(response.status_code)
            if response.status_code == 200:
                data = response.json()
                game_cheap_id = ""
                if len(data) >= 1:
                    game_cheap_id = data[0].get("gameID")
                    top_games_ids.append(game_cheap_id)
                else:
                    top_games_ids.append("None")
                break
            elif response.status_code == 429:
                retry_after = response.headers.get("Retry-After")
                if retry_after:
                    time_stamp = int(retry_after)
                    print(f"ERROR: Rate Limit. Wait {time_stamp} seconds.")
                else:
                    time_stamp *= 2
                    print(f"ERROR: Rate Limit. Wait {time_stamp} seconds.")
            else:
                print(f"Error {response.status_code}")
    for game in top_games_ids:
        if game != "None":
            create_game_schema = await id_search(game)
            if create_game_schema != "None":
                await create(create_game_schema)
async def id_search(game_id):
    max_tries = 3
    tries = 0
    time_stamp = 1
    for tries in range(max_tries):
        await asyncio.sleep(time_stamp)
        response = requests.get(cheap_shark_url, params={"id": game_id}, headers=headers)
        if response.status_code == 200:
            data = response.json()
            if len(data) == 0:
                return "None"
            game_prices = data["deals"]
            prices_ = {}
            for store in StoresEnum:
                store_number = StoreIDEnum[store.name].value
                store_price_details = StorePriceDetails(
                    price=get_store_price(game_prices, store_number)
                )
                prices_[store.value] = store_price_details

            game = CreateGameSchema(
                title=data["info"]["title"],
                all_time_cheapest_price=data["cheapestPriceEver"]["price"],
                developer=get_developer(data["info"]["steamAppID"]),
                prices=prices_
            )
            return game
        elif response.status_code == 429:
            retry_after = response.headers.get("Retry-After")
            if retry_after:
                time_stamp = int(retry_after)
                print(f"ERROR: Rate Limit. Wait {time_stamp} seconds.")
            else:
                time_stamp *= 2
                print(f"ERROR: Rate Limit. Wait {time_stamp} seconds.")
        else:
            print(f"Error {response.status_code}, ID: {game_id}")
    return "None"


def get_store_price(deals,store_number):
    for deal in deals:
        if str(deal["storeID"]) == str(store_number):
            return deal["price"]
    return "-1"



