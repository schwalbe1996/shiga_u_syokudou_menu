import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from bs4 import BeautifulSoup
import requests
import time

options = Options()
options.add_argument("--headless")
options.add_argument("--no-sandbox")

# ポイント: 以下のように「executable_path」は不要
driver = webdriver.Chrome(options=options)

driver.get("https://west2-univ.jp/sp/menu.php?t=657611")
time.sleep(3)

print("Page title is:", driver.title)
driver.quit()
