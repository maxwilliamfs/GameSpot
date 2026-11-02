import requests
from app.core.conf import Settings

def get_developer(steamID):
    steam_api_url = "https://store.steampowered.com/api/appdetails"
    headers = {"User-Agent": f"GameSpotApp/1.0 {Settings.USER_EMAIL}"}

    response = requests.get(steam_api_url, params={"appids": steamID}, headers=headers)
    if response.status_code == 200:
        data = response.json()
        app_data = data.get(str(steamID), {})
        if app_data and app_data.get("success"):
            game_info = app_data.get("data", {})
            developers = game_info.get("developers", [])
            if developers:
                return developers[0]
    else:
        return "Missing"