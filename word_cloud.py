#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from janome.tokenizer import Tokenizer
import pandas as pd
import collections
from wordcloud import WordCloud

# csvファイルを読み込み
df_file = pd.read_csv('./merged_file/normalized.txt', encoding='utf-8')

# 歌詞をデータフレームからリストに変換
song_lyrics = df_file['歌詞'].tolist()

t = Tokenizer()

results = []

for s in song_lyrics:
    tokens = list(t.tokenize(s, wakati=True))
    result = [i.replace('\u3000','') for i in tokens]   # 全角スペースを削除

    # リストに追加
    results.extend(result)

# wordcloud 
#日本語のフォントパス
fpath = '/home/tonoyama/.fonts/SourceHanCodeJP-Normal.otf'

text = ' '.join(results)  # 区切り文字を「・」にして文字列に変換

# 単語の最大表示数は500に設定
wordcloud = WordCloud(background_color='white',
    font_path=fpath, width=800, height=600, max_words=500).generate(text)

#画像はwordcloud.pyファイルと同じディレクトリにpng保存
wordcloud.to_file('./wordcloud-mrchildren.png')