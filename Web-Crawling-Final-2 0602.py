#!/usr/bin/env python
# coding: utf-8

# In[15]:
# 匯入csv檔必須跟python此檔同一個位置

from bs4 import BeautifulSoup
import requests
from lxml import etree
import re
import csv
import os


#--------------------
#取得該網址連結的html
#--------------------

def get_html(url):
	try:
		user_agent = 'Mozilla/5.0'
		resp = requests.get(url, headers={'User-Agent': user_agent}, timeout = 30) #回傳為一個request.Response的物件
		resp.endcoding = 'utf8'
		# print(resp.text)
		return resp.text															#轉成文字(requests套件的一個功能)只要文字的部分(?
	except:
		return 'ERROR'


#--------------------
#辨認出每間公司10-K連結所在的網址
#--------------------

#每個cikcode所在url的邏輯
def get_url(cikcode):  
	url = "https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=" + str(cikcode) + "&type=10-k&dateb=&owner=exclude&count=40"
	return url


#--------------------
#把個別公司的各年度url加入到一個該公司專屬的list
#輸出為該公司10-K所在位置的html list
#--------------------

def get_url_list(cikcode, year_list):
	url = get_url(cikcode)
	resp_text = get_html(url)
	soup = BeautifulSoup(resp_text,"html.parser")					#轉為python可讀的指令，且包含位階
	sel = soup.select("table.tableFile2 tr")							
	url_list = []
	document_list = []
	for i in sel:
		if i.a == None:												#????????????????? a = 超連結????
			continue
		link = str(i.a["href"])										#href: a這個超連結連到的網址
		
		#----------
		#條件改為該公司需要的所有年度，目前僅有"-17","-18-"
		#----------
		for i in range(len(year_list)) :
			if "-" + str(year_list[i]) + "-" in link :			#決定想要那些年分
			# if '-17-' in link or '-18-' in link:  #年份2017、2018
				link_name = 'https://www.sec.gov'+ link
				url_list.append(link_name)
	if len(url_list) !=0:
		for i in url_list:
			resp_text = get_html(i)
			soup = BeautifulSoup(resp_text,"html.parser")
			sel = soup.select("table.tableFile tr")
			for i in sel:
				if '10-K' in i.text and "10-K/A" not in i.text :			#僅限定將10-K文件抓下來，但不要10-K/A
					link = 'https://www.sec.gov'+str(i.a["href"])
					document_list.append(link)
	
	return document_list


#--------------------
#透過該公司10-K的html檔，取得該公司當年度文章，並加入一個list
#--------------------

def get_article(document_list):
	all_article = []
	for k in document_list:
		text = get_html(k)
		html = etree.HTML(text)
		no_use_content = html.xpath('//*/text()')
		
		content = str()
		paragraph = str()
		
		for i in no_use_content :
			for ch in i :
			
				if ch == " " or (33 <= ord(ch) <= 125) or ch == "\n" :
					paragraph += ch
					# print("----------")
					# if (len(paragraph) >= 2) and (" " not in paragraph) and paragraph[len(paragraph) - 1] == "\n" :
					if (len(paragraph) >= 2) and (paragraph[0] == " " or paragraph[0] == "\n") and paragraph[len(paragraph) - 1] == "\n" :
						paragraph = " ".join(re.split(r"\s+", paragraph))
						paragraph = paragraph.strip(" ")
						paragraph = paragraph.strip("\n")
						paragraph = paragraph.strip(" ")
						paragraph = paragraph.strip("\n")
						
						if (" " not in paragraph) :
							try :
								paragraph = int(paragraph)
								
								paragraph = str()
							
							except :
								content += paragraph
								content += " "
						
								paragraph = str()
						
						else :
							paragraph = paragraph.strip(" ")
							if paragraph != "" :
								# print("----------")
								content += paragraph
								content += "\n"
						
						paragraph = str()
							
					
					elif (len(paragraph) >= 2) and (33 <= ord(paragraph[0]) <= 125) and paragraph[len(paragraph) - 1] == "\n" :
						# print("----------")
						paragraph = " ".join(re.split(r"\s+", paragraph))
						paragraph = paragraph.strip("\n")
						paragraph = paragraph.strip(" ")
						content += paragraph
						content += " "
						
						paragraph = str()
					
					# elif (len(paragraph) >= 2) and (" " not in paragraph) and paragraph[len(paragraph) - 1] == "\n" :
						# paragraph = paragraph.strip("\n")
						# content += paragraph
						# content += " "
						
						# paragraph = str()
					
					# elif (len(paragraph) >= 2) and (paragraph[0] == " " or paragraph[0] == "\n") and paragraph[len(paragraph) - 1] == "\n" :
						# paragraph = paragraph.strip(" ")
						# paragraph = paragraph.strip("\n")
						# paragraph = paragraph.strip(" ")
						
						# if paragraph != "" :
							# print("----------")
							# content += paragraph
							# content += "\n"
						
						# paragraph = str()
					
		all_article.append(content)
	return all_article


#--------------------
#讀入input的彙總公司代碼的csv檔，並轉為一個list
#小問題：code_list[0]會是 "cikcode"
#--------------------

def read_csv():
	code_list = []
	with open(fn, newline = "") as csvfile : #fn是匯入的檔案路徑 #crawltest0426.csv 是匯入的檔名
		rows = csv.reader(csvfile)
		print(rows)
		for row in rows:
			code_list.append(row)
	return code_list


#--------------------
#在電腦中建立儲存文件之資料夾
#--------------------

def createFolder(directory):
	try:
		if not os.path.exists(directory):
			os.makedirs(directory)
	except OSError:
		print ('Error: Creating directory. ' +  directory)


#--------------------
#將文件寫入txt檔並命名為 公司名稱_年度(目前還沒修正)
#--------------------

def write_file(code, article, year_list):
	for idx,i in enumerate(article):
		name = 'C:\\Users\\MichaelHong\\Desktop\\國立台灣大學會計研究所\\107學年度\\107學年度第二學期\\選修-商管程式設計\\期末報告\\10-K_data/' + code + '_' + str(idx+1) + '.txt'
		with open(name,'w+') as file:
			file.write(i)
			file.write('\n')


#--------------------
#正式執行程式
#--------------------


def start_crawling(year_list):
	# try:
	code_list = read_csv()
	
	#測試用
	print(code_list)
	
	all_article = []
	all_url = []
	createFolder("C:\\Users\\MichaelHong\\Desktop\\國立台灣大學會計研究所\\107學年度\\107學年度第二學期\\選修-商管程式設計\\期末報告\\10-K_data")
	for i in range(1,len(code_list)):
		document_list = get_url_list(code_list[i][0], year_list)
		article = get_article(document_list)
		write_file(code_list[i][0], article, year_list)
		all_article.append(article)
		all_url.append(document_list)
		
		#測試用
		# print(document_list)
	
	#測試用
	# print(all_url)
	
	# return all_article
	
	code_year_list = code_year(code_list, year_list)
	
	code_year_article_list = code_year_article(all_article, code_list, year_list)
	
	code_year_url_list = code_year_url(all_url, code_list, year_list)
	
	print(code_year_list)
	print(code_year_article_list[0][0])
	print(code_year_url_list)
	
	# return code_year_list, code_year_article_list, code_year_url_list
	# except:
	# print("ERROR")
	
def code_year(code_list, year_list) :
	temp_code_year = []
	code_year_list = []
	
	for i in range(1, len(code_list)) :
		for j in range(len(year_list)) :
			code_year = str(code_list[i][0]) + "-" + str(year_list[j])
			temp_code_year.append(code_year)
		
		code_year_list.append(temp_code_year)
		temp_code_year = []
	
	return code_year_list

def code_year_article(all_article, code_list, year_list) :
	temp_article = []
	code_year_article_list = []
	
	for i in range(1, len(code_list)) :
		for j in range(len(year_list)) :
			temp_article.append(all_article[j])
		
		code_year_article_list.append(temp_article)
		
		temp_article = []

	return code_year_article_list

def code_year_url(all_url, code_list, year_list) :
	temp_url = []
	code_year_url_list = []
	
	for i in range(len(code_list) - 1) :
		for j in range(len(year_list)) :
			temp_url.append(all_url[i][j])
		
		code_year_url_list.append(temp_url)
		
		temp_url = []

	return code_year_url_list

# In[27]:

#匯入整個公司代碼的csv檔案
fn = input()

#在視窗選取所要的年度
year_list = input().split(",")

#匯入所需的關鍵字
# keyword_list = input().split(",")


all_article = start_crawling(year_list)

# print(code_year_list)
# print(code_year_url_list)