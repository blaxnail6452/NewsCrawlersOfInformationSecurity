#步驟1 import所有需要的library
import pandas as pd
import csv
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
from scipy.ndimage import gaussian_gradient_magnitude
from snownlp import SnowNLP

#步驟2 將篩選出的新聞的csv讀入
df_news = pd.read_csv("News_crawlers_filter.csv")

#步驟3 將所有記者的名字串聯一起
location = 0 #跟content同時定位
author = "" #取得同content的作者
positive_text_author = "" #正面新聞的記者
negative_text_author = "" #負面新聞的記者
all_author = "" #所有記者
for i in df_news["content"]:
	author = df_news.iloc[location]["author"]
	all_author = all_author + "  " + author #全部的記者
	text = SnowNLP(str(i))
	if text.sentiments > 0.5: #此篇文章是正面的，加入正面記者
		positive_text_author = positive_text_author + "  " + author
	else: ##此篇文章是負面的，加入負面記者
		negative_text_author = negative_text_author + "  " + author
	location += 1

#步驟4 記者的名字中會有一些雜字，因為有可能是轉載自其他網站，因此先做預處理，把這些字都清除
no_author = ["中央社", "台北", "日電", "聯合", "新聞網", "日", "電", "報", "財訊雙週刊", "/", "苗栗"]
for i in no_author:
	all_author = all_author.replace(i, " ")
	positive_text_author = positive_text_author.replace(i, " ")
	negative_text_author = negative_text_author.replace(i, " ")

#步驟5 輸出文字雲
font_path = "kaiu.ttf"

#mask image，設定輸出的造型
mask_color = np.array(Image.open("parrot.jpg"))
mask_color = mask_color[::3, ::3]
mask_image = mask_color.copy()
mask_image[mask_image.sum(axis = 2) == 0] = 255

#edge detection ，邊界設定
edges = np.mean([gaussian_gradient_magnitude(mask_color[:, :, i] / 255., 2) for i in range(3)], axis = 0)
mask_image[edges > .08] = 255

#正式輸出，文字雲樣式設定
wc = WordCloud(font_path = font_path, repeat = True, background_color = "white", colormap = "magma", mask = mask_image)
#因為是人名，所以不加上結巴分割字元的功能
wc.generate(all_author) 
wc.to_file("wordcloudAuthor.jpg") #所有記者的文字雲
wc.generate(positive_text_author) 
wc.to_file("wordcloudPositiveAuthor.jpg") #正面記者的文字雲
wc.generate(negative_text_author) 
wc.to_file("wordcloudNegativeAuthor.jpg") #負面記者的文字雲


