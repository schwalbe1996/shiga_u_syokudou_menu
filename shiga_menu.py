from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from bs4 import BeautifulSoup
import pandas as pd
import requests
import time



# ==========================
# 子ページデータ取得関数
# ==========================
def scrape_child_page(datas):
    url =datas.get("url")
    response = requests.get(url)
    time.sleep(1)
    if response.status_code != 200:
        return None

    soup_sub = BeautifulSoup(response.content, "html.parser")

    # 栄養素データの取得（元のコードを使用）
    exclude_classes = {"allergy", "note"}
    li_tags = soup_sub.find("ul", class_="detail").find_all(
        "li", class_=lambda x: not (x and any(cls in exclude_classes for cls in x.split()))
    )

    # 商品名と価格の取得
    #product_name修正箇所：検索対象h3→h1,検索対象外：titleタグ。抽出範囲:タグ直下のテキストのみ抽出
    product_name = soup_sub.find("h1", id=lambda x: x is None or x != "title").contents[0].strip() if soup_sub.find("h1", id=lambda x: x is None or x != "title") else "不明"
    price = soup_sub.find("span", class_="price").text.strip() if soup_sub.find("span", class_="price") else "不明"

    # 栄養素データを保存
    details = {"カテゴリー":datas.get("cat_tag"),"商品名": product_name, "価格（税込）": price}
    for tags in li_tags:
        tag = tags.find("strong")
        val = tags.find("span", class_="price")
        if tag:
            tag = tag.text.strip()
        else:
            tag = ""  # データがない場合は空白
        if val:
            val = val.text.strip()
        else:
            val = ""  # データがない場合は空白
        if tag or val:
            details[tag] = val

    return details


# ==========================
# 親ページリンク取得関数
# ==========================
def get_menu_links():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(options=options)

    parent_url = "https://west2-univ.jp/sp/menu.php?t=657611"
    driver.get(parent_url)
    time.sleep(5)

    menu_links = []
    button_ids = ["on_b", "on_c", "on_d", "on_e", "on_f", "on_g"]

    try:
        for button_id in button_ids:
            button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.ID, button_id))
            )
            button.click()
            time.sleep(2)

        # ページ全体のHTMLからリンクを収集
        soup = BeautifulSoup(driver.page_source, "html.parser")
        target_class = "catMenu"
        toggle_elems = soup.find_all("p", class_="toggleTitle open")

        all_catmenus = []  # catMenuを保存するリスト

        for p_tag in toggle_elems:
            # <p> の直後の兄弟要素で class="catMenu" のものを取得

            cat_menu_div = p_tag.find_next_sibling("div", class_=target_class)
            if cat_menu_div:
                links = cat_menu_div.find_all("a")
                for link in links:
                    href = link.get("href")
                    if href:
                        menu_links.append({"url":"https://west2-univ.jp/sp/" + href,"cat_tag":p_tag.text.strip().split()[0]})

    finally:
        driver.quit()

    return menu_links


# ==========================
# メイン処理
# ==========================
def main():
    # 子ページのリンクを収集
    menu_links = get_menu_links()

    # 各子ページのデータを収集
    all_data = []
    for link in menu_links:
        details = scrape_child_page(link)
        if details:
            all_data.append(details)

    # DataFrameに変換し、CSV形式で保存
    columns = ["カテゴリー","商品名", "価格（税込）", "エネルギー", "タンパク質", "脂質", "炭水化物", "食塩相当量", "カルシウム", "野菜量", "鉄", "ビタミン A", "ビタミン B1", "ビタミン B2", "ビタミン C"]
    df = pd.DataFrame(all_data, columns=columns)
    df.to_csv("shiga_menu.csv", index=False, encoding="shift-jis")
    print("データを shiga_menu.csv に保存しました。")


if __name__ == "__main__":
    main()
