from fastapi import HTTPException
from app.services.webscapping.steam_scrapper import get_developer
from app.schemas.games import CreateGameSchema
import requests
import time

ids = [
  "324340","None","None","None","327581","152058","202350","306473","206516","281587","328808","None","None","268290","298615","300920","228547","None",
  "249998","334401","264414","331996","332174","328839","251191","104077","324322","None","None","324169","157695","286574","307902","107598","199815",
  "211060","144222","260921","308654","236717","291866","None","141021","300679","329912","327456","None","281411","None","None","196050","323482",
  "102722","239901","330373","None","271592","284226","312443","305806","332769","210978","150036","315191","175863","323772","187747","166717","80",
  "332210","186966","333483","93389","269728","141220","144894","144209","None","1295","321328","299534","276883","329877","202278","149344","231604",
  "329516","241552","None","321803","295364","258398","279442","333522","246641","220342","182370","104006","None","252876"
]

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
                if len(data) >= 1:
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
    return top_games_info

def id_search(game_id):
    response = requests.get(cheap_shark_url, params={"id": game_id}, headers=headers)
    data = response.json()

    prices = []


    game = CreateGameSchema(
        title=data["info"]["title"],
        all_time_cheapest_price=data["cheapestPriceEver"]["price"],
        developer=get_developer(data["steamAppID"])

    )

