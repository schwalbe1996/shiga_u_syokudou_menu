from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import chromedriver_binary

options = Options()
# ヘッドレスモード（Linux上で動かすとき必ずこのモードにしておく）
options.add_argument('--headless')
driver = webdriver.Chrome(options=options)
driver.get('https://example.com')
print(driver.current_url)
