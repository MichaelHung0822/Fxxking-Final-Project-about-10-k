#!/usr/bin/env python
# coding: utf-8

# In[15]:
# 匯入csv檔必須跟python此檔同一個位置

from bs4 import BeautifulSoup
import requests
from lxml import etree
import csv
import os


# In[2]:


def get_html(url):
    try:
        user_agent = 'Mozilla/5.0'
        resp = requests.get(url, headers={'User-Agent': user_agent}, timeout = 30) #回傳為一個request.Response的物件
        resp.endcoding = 'utf8'
        return resp.text															#只要文字的部分(?
    except:
        return 'ERROR'


# In[3]:

#每個cikcode所在url的邏輯
def get_url(cikcode):  
    url = "https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=" + str(cikcode) + "&type=10-k&dateb=&owner=exclude&count=40"
    return url


# In[4]:


def get_url_list(cikcode):
    url = get_url(cikcode)
    resp_text = get_html(url)
    soup = BeautifulSoup(resp_text,"html.parser")
    sel = soup.select("table.tableFile2 tr")
    url_list = []
    document_list = []
    for i in sel:
        if i.a==None:
            continue
        link = str(i.a["href"])
        if '-17-' in link or '-18-' in link:  #年份2017、2018
            link_name = 'https://www.sec.gov'+ link
            url_list.append(link_name)
    if len(url_list) !=0:
        for i in url_list:
            resp_text = get_html(i)
            soup = BeautifulSoup(resp_text,"html.parser")
            sel = soup.select("table.tableFile tr")
            for i in sel:
                if '10-K' in i.text:
                    link = 'https://www.sec.gov'+str(i.a["href"])
                    document_list.append(link)
    return document_list


# In[5]:


def get_article(document_list):
    all_article = []
    for k in document_list:
        text = get_html(k)
        html = etree.HTML(text)
        no_use_content = html.xpath('//*/text()')
        content = str()
        for i in no_use_content:
            for ch in i:
                if ch == '\n':
                    ch = ' '
                if ch == ' ' or (33 <= ord(ch) <=125) :
                    content+=ch
        all_article.append(content)
    return all_article


# In[6]:


def read_csv():
    code_list = []
    with open('C:\\Users\\MichaelHong\\Desktop\\國立台灣大學會計研究所\\107學年度\\107學年度第二學期\\選修-商管程式設計\\期末報告\\crawltest0426.csv', newline='') as csvfile: #crawltest0426.csv 是匯入的檔名
        print("x")
        rows = csv.reader(csvfile)
        print(rows)
        for row in rows:
            code_list.append(row)
    return code_list


# In[24]:


def createFolder(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print ('Error: Creating directory. ' +  directory)


# In[25]:


def write_file(code,article):
    for idx,i in enumerate(article):
        name = 'C:\\Users\\MichaelHong\\Desktop\\國立台灣大學會計研究所\\107學年度\\107學年度第二學期\\選修-商管程式設計\\期末報告\\10-K_data/'+code+'_'+str(idx+1)+'.txt'
        with open(name,'w+') as file:
            file.write(i)
            file.write('\n')


# In[26]:


def demo():
    # try:
	code_list = read_csv()
	print(code_list)
	print("code_list")
	all_article = []
	createFolder('C:\\Users\\MichaelHong\\Desktop\\國立台灣大學會計研究所\\107學年度\\107學年度第二學期\\選修-商管程式設計\\期末報告\\10-K_data')
	for i in range(1,len(code_list)):
		document_list = get_url_list(code_list[i][0])
		article = get_article(document_list)
		write_file(code_list[i][0],article)
		all_article.append(article)
	return all_article
    # except:
	print("ERROR")


# In[27]:


all_article = demo()