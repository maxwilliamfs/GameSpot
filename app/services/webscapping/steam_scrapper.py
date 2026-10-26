from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from app.services.webscapping import cheap_shark
import time
import requests


def refresh_games():
    options = Options()
    options._binary_location = "/usr/bin/brave"
    navigator = webdriver.Chrome(options=options)
    navigator.maximize_window()
    title_name_address = "//a[contains(@href, '/app/') and normalize-space(.) != '']"
    steam_url = "https://store.steampowered.com/"

    navigator.get(steam_url)
    time.sleep(2)
    first_btn = navigator.find_element(By.XPATH,"//div[text()='Explorar']")
    first_btn.click()

    time.sleep(2)
    first_btn = navigator.find_element(By.XPATH,"//span[text()='Mais vendidos']")
    first_btn.click()
    time.sleep(2)

    top_games_preview = navigator.find_elements(By.XPATH,title_name_address)[:100]
    navigator.execute_script("arguments[0].scrollIntoView({block: 'center'})",top_games_preview[-1])
    time.sleep(1)

    top_games = navigator.find_elements(By.XPATH,title_name_address)[:100]

    top_games_titles = []
    for game in top_games:
        top_games_titles.append(game.text)

    time.sleep(1)
    cheap_shark.cheap_shark_search(top_games_titles)

def get_developer(steamID):
    steam_api_url = "https://store.steampowered.com/api/appdetails"
    headers = {"User-Agent": "GameSpotApp/1.0 (williammaxbcc4794@gmail.com)"}

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
