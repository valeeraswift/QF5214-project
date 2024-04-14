#!/usr/bin/env python
# coding: utf-8

# In[1]:


from selenium import webdriver
browser = webdriver.Chrome()  

import re
data_all = ''
for i in range(2,20):  # 这里演示爬取10页
    url = f'https://guba.eastmoney.com/list,zssh000001,f_{i}.html'
    browser.get(url)
    data = browser.page_source
    data_all = data_all + data  # 拼接每一页网页源代码
p_title = '<a href=".*?" title="(.*?)"'
title = re.findall(p_title, data_all)

text = []
for i in range(len(title)):
    text.append(str(i+1) + '.' + title[i])
    
txt_file_path = "data.txt"
# 将列表写入txt文件
with open(txt_file_path, "w") as txtfile:
    for row in text:
        txtfile.write("".join(map(str, row)) + "\n")

print("TXT文件已成功保存！")


# In[4]:


from selenium import webdriver
import time
import re

# 启动一个Chrome浏览器实例
driver = webdriver.Chrome()

# 打开网页
driver.get("https://www.jiuyangongshe.com")

# 设置一个时间延迟，等待页面加载完成
time.sleep(2)

# 记录当前页面高度
last_height = driver.execute_script("return document.body.scrollHeight")

# 模拟向下滚动页面
while True:
    # 模拟滚动到页面底部
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    
    # 等待页面加载
    time.sleep(2)
    
    # 计算新的页面高度
    new_height = driver.execute_script("return document.body.scrollHeight")
    
    # 检查是否已经到达页面底部
    if new_height == last_height:
        break
    
    # 更新页面高度
    last_height = new_height

# 获取页面源码
html_content = driver.page_source

# 关闭浏览器
driver.quit()

# 使用正则表达式匹配目标内容
pattern = r'<div class="book-title\s+click\s+fs17-bold"\s+data-v-f2485b86="">(.*?)</div>'
title = re.findall(pattern, html_content)

pattern2 = r'<div\s+data-v-f2485b86=""\s+class="book-title\s+click\s+fs17-bold">(.*?)</div>'
matches2 = re.findall(pattern2, html_content)

# 合并两种格式的匹配结果
titles_combined = title + matches2

# 将匹配到的内容写入txt文件
with open('book_titles.txt', 'w', encoding='utf-8') as file:
    for idx, item in enumerate(titles_combined):
        file.write(f"{idx+1}. {item}\n")

# 输出匹配到的内容
for i in range(len(titles_combined)):
    print(str(i+1) + '.' + titles_combined[i])

print("Titles written to 'book_titles.txt'.")


# In[12]:


import jieba
from collections import Counter
from nltk.sentiment import SentimentIntensityAnalyzer

# 读取文本文件
file_path = 'book_titles.txt'
with open(file_path, 'r', encoding='utf-8') as file:
    text = file.read()

# 中文分词
words = jieba.lcut(text)

# 加载中文停用词表
stop_words_path = 'stopwords_cn.txt'  # 停用词表文件路径，需要提前准备好
with open(stop_words_path, 'r', encoding='utf-8') as sw_file:
    stop_words = set(sw_file.read().splitlines())

# 去除停用词
filtered_words = [word for word in words if word.strip() and word not in stop_words]

# 计算词频
word_counts = Counter(filtered_words)
most_common_words = word_counts.most_common(10)  # 获取前 10 个高频词

print("Top 10 Most Common Words:")
for word, count in most_common_words:
    print(f"{word}: {count}")


# In[14]:


from snownlp import SnowNLP
from collections import Counter
import jieba

# 读取文本文件
file_path = 'data.txt'
with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
    text = file.read()


# 中文分词
words = jieba.lcut(text)

# 情感分析
sentiments = []
for word in words:
    if word.strip():  # 去除空字符
        s = SnowNLP(word)
        sentiments.append(s.sentiments)

# 计算情感得分
average_sentiment = sum(sentiments) / len(sentiments)

# 输出情感分析结果 越高越积极
print("Average Sentiment Score (from SnowNLP):", average_sentiment)


# In[ ]:




