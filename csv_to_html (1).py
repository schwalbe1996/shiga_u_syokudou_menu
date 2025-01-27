import pandas as pd

# CSVファイルを読み込む
df = pd.read_csv('shiga_menu.csv')

# HTMLテーブルに変換し、index.htmlとして保存
df.to_html('index.html', index=False, justify='center', border=0, classes='table table-striped')
