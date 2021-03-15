# Below are examples for how web scraping works using Python.
# If you want to learn how to web scrape with Python watch this video:
# https://youtu.be/dBs_RGOCqSc

# ---------------- requests + beautiful soup ----------------
import requests
from bs4 import BeautifulSoup

page_html = requests.get("https://alfredo.lol/karen").text
soup = BeautifulSoup(page_html, features="lxml")

# get the name of all the add-ons on the page
for addon in soup.find_all("div", class_="addon-container"):
    print(addon.a.h3.text)

# ---------------- selenium ----------------
from selenium import webdriver

driver = webdriver.Firefox()
driver.get("https://alfredo.lol/karen")

# ---------------- requests + sleep ----------------
import requests
from time import sleep
from random import randint

while True:
        r = requests.get("https://google.com")
        print(r.text)
        sleep(randint(1,5))
