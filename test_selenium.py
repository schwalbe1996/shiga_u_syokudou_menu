import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

options = Options()
options.add_argument("--headless")
options.add_argument("--no-sandbox")

# ポイント: 以下のように「executable_path」は不要
driver = webdriver.Chrome(options=options)

driver.get("https://www.python.org/")
time.sleep(3)

print("Page title is:", driver.title)
driver.quit()
