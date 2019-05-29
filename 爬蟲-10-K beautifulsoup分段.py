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
        user_agent = 'Mozilla/5.0'#?UA問題
        resp = requests.get(url, headers={'User-Agent': user_agent}, timeout = 30) #回傳為一個request.Response的物件
        resp.endcoding = 'utf8'
        return resp.text
    except:
        return 'ERROR'


# In[3]:

#每個cikcode所在url的邏輯
def get_url(cikcode):  
    url = "https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=" + str(cikcode) + "&type=10-k" + "&type=10-k&dateb=&owner=exclude&count=40"
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
                if '10-K' in i.text:#年份中10-K格式的財報
                    link = 'https://www.sec.gov'+str(i.a["href"])
                    document_list.append(link)
    return document_list


# In[5]:


def get_article(url_list):
    all_article = []
    for k in url_list:
        text = get_html(k)
        html = BeautifulSoup(text,"html.parser")
        no_use_content = html.find_all('font')
        content = str()
        for i in range(len(no_use_content)):
            no_use_content[i] = no_use_content[i].text.strip()
            ent = 1
            for j in no_use_content[i]:
                if j != '\n':
                    ent = 0
                    break
            if ent == 0:
                for j in range(len(no_use_content[i])):
                    ch = no_use_content[i][j]
                    if j!= len(no_use_content[i]) and ch == '\n' :
                        ch = ' '
                    if ch == ' ' or ch == '\n' or (33 <= ord(ch) <=125):
                        content+=ch
                content += '\n'
        all_article.append(content)
    return all_article


# In[6]:


def read_csv():
    code_list = []
    with open('crawltest0426.csv', newline='') as csvfile: #crawltest0426.csv 是匯入的檔名
        rows = csv.reader(csvfile)
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
        name = '10-K_data/'+code+'_'+str(idx+1)+'.txt'
        with open(name,'w+') as file:
            file.write(i)
            file.write('\n')


# In[26]:


def demo():
    #try:
        code_list = read_csv()
        all_article = []
        createFolder('10-K_data')
        for i in range(1,len(code_list)):
            document_list = get_url_list(code_list[i][0])
            article = get_article(document_list)
            write_file(code_list[i][0],article)
            all_article.append(article)
        return all_article
    #except:
        #print("ERROR")


# In[27]:


all_article = demo()


# In[ ]:




