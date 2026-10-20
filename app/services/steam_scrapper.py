from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time

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

time.sleep(5)
