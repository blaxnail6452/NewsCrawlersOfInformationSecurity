#步驟1 import所有需要的library
import pandas as pd
import numpy as np

#步驟2 將儲存全部新聞的結果的csv讀入
df_news = pd.read_csv("News_crawlers.csv")

#步驟3 設立我們要的key_word，也就是與遠端上課、居家辦公相關的結果
key_word = ["Zoom", "Google meet", "Teams", "遠距", "居家", "居家上班", "居家上課", "辦公", "工作", "上班", "上課", "防駭", "會議"]

#步驟4 開始利用我們的key word來搜尋有哪些新聞的內文是具有這些關鍵字的
count = 0
time = []
author = []
title = []
content = []
href = []
content_is_nan = 0
for i in df_news["content"]:
	if i is np.nan: #避免內文的爬取是NaN，造成程式錯誤
		content_is_nan = 1 #若內文為空，即不採用
		continue
	for j in key_word: #利用key_word的方式搜尋內文，剛好可以去掉有問題的新聞(填詞為pass的部分)
		if j in i:
			#print("編號" + str(count) + "新聞，關鍵字為 : " + j)
			time.append(df_news.iloc[count][1])
			author.append(df_news.iloc[count][2])
			title.append(df_news.iloc[count][3])
			content.append(df_news.iloc[count][4])
			href.append(df_news.iloc[count][5])
			break
	count += 1
	content_is_nan = 0

#步驟5 將我們篩選出有符合條件的新聞寫入News_crawlers_filter.csv中
df = pd.DataFrame({'time':time, 'author':author, 'title':title, 'content': content, "href":href}, columns = ["time", "author", "title", "content", "href"])
df.to_csv("News_crawlers_filter.csv", encoding = "utf_8_sig")
