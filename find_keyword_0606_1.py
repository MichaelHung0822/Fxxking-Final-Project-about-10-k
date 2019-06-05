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
		#已可選擇所需的公司年度，但只能輸入年度後兩碼 (if '-17-' in link or '-18-' in link:  #年份2017、2018)
		#----------
		for i in range(len(year_list)) :
			if "-" + str(year_list[i]) + "-" in link :       #決定想要那些年分
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

			paragraph = " ".join(re.split(r"\s+", paragraph))

			try :
				paragraph = int(paragraph)

				paragraph = str()

			except :
				content += paragraph
				content = content.strip(" ")
				content = content.strip("\n")
				content += "\n"

				paragraph = str()

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
		# print(rows)
		for row in rows:
			code_list.append(row)
	return code_list


#--------------------
#爬蟲主程式
#--------------------

def start_crawling(year_list):
	# try:
	code_list = read_csv()

	#測試用
	print(code_list)

	all_article = []
	all_url = []
	# createFolder(str(path))
	for i in range(1,len(code_list)):
		document_list = get_url_list(code_list[i][0], year_list)
		article = get_article(document_list)
		# write_article(code_list[i][0], article, year_list)
		# write_url(code_list[i][0], document_list, year_list)
		all_article.append(article)
		all_url.append(document_list)

		#print(type(article))
		#print(document_list)

		#測試用
		# print(document_list)

	#測試用
	# print(all_url)

	code_year_list = code_year(code_list, year_list)

	return all_article, all_url, code_year_list



	# code_year_article_list = code_year_article(all_article, code_list, year_list)

	# code_year_url_list = code_year_url(all_url, code_list, year_list)

	# print(code_year_list)
	# print(code_year_article_list[0][0])
	# print(code_year_url_list)

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


# def code_year_article(all_article, code_list, year_list) :
	# temp_article = []
	# code_year_article_list = []

	# for i in range(1, len(code_list)) :
		# for j in range(len(year_list)) :
			# temp_article.append(all_article[j])

		# code_year_article_list.append(temp_article)

		# temp_article = []

	# return code_year_article_list


# def code_year_url(all_url, code_list, year_list) :
	# temp_url = []
	# code_year_url_list = []

	# for i in range(len(code_list) - 1) :
		# for j in range(len(year_list)) :
			# temp_url.append(all_url[i][j])

		# code_year_url_list.append(temp_url)

		# temp_url = []

	# return code_year_url_list

#------------------------------------------------------------------------------

#匯入整個公司代碼的csv檔案
fn = input("請匯入公司代碼的csv檔：").strip('"')

#在視窗選取所要的年度
year_list = input("請選取所需年分 (以逗點分離)：").split(",")

#觸發爬蟲主程式，並把 return 出的 all_article 指派到 all_article
all_article, all_url, code_year_list = start_crawling(year_list)
# print(all_url)
# print(type(all_url))


#=================================================================================================================

def noSpaceLow(Str):
    """把子串中的空格都改成一格然後全部變小寫"""
    ans = Str.split()
    newStr = ""
    for i in range(len(ans)):
        newStr += ans[i]
        if i != len(ans) - 1:
            newStr += " "
    return newStr.lower()


def matchcase(word):
    def replace(m):
        highlight_start = str('<<< ')
        highlight_end = str(' >>>')
        text = m.group()
        if text.isupper():
            return highlight_start + word.upper() + highlight_end
        elif text.islower():
            return highlight_start + word.lower() + highlight_end
        elif text[0].isupper():
            return highlight_start + word.capitalize() + highlight_end
        else:
            return highlight_start + word + highlight_end
    return replace



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
#將文件寫入txt檔並命名為 "公司名稱_result"
#這邊有個前提是：code_list 中的公ㄒ代碼順序，必須和 all_companies_results 中的文本順序100%對應，不然全部都匯錯位！(兩 list 長度也必須一樣！)
#看可不可以讓視窗幫我們避免掉 userrequestnum 填 0 的情況
#--------------------

def write_article(all_companies_results) :
	code_list = read_csv()
	for i in range(len(all_companies_results)) :
		if i % userrequestnum == 0:
			if i + userrequestnum <= len(all_companies_results):
				name = str(path) + "/" + code_list[i + 1][0] + " to " + code_list[i + userrequestnum][0] + "_result.txt"   #C:\Users\ewp52\Desktop\10-k_data/
				with open(name,'w+') as file:
					file.write("Keyword: " + search + "\n\n")
					for j in range(len(all_companies_results[i])):
						file.write(all_companies_results[i][j])
						file.write('\n')

			else: #剩下不到 userrequestnum 數量的公司所組成之txt檔
				name = str(path) + "/" + code_list[i + 1][0] + " to " + code_list[-1][0] + "_result.txt"   #C:\Users\ewp52\Desktop\10-k_data/
				with open(name,'w+') as file:
					file.write("Keyword: " + search + "\n\n")
					for j in range(len(all_companies_results[i])):
						file.write(all_companies_results[i][j])
						file.write('\n')

		else:
			with open(name,'a+') as file:
				for j in range(len(all_companies_results[i])):
					file.write(all_companies_results[i][j])
					file.write('\n')



# def write_article(all_companies_results) :
# 	code_list = read_csv()
# 	count = 0
# 	for i in range(len(all_companies_results)) :
# 		if userrequestnum == 1:
# 			name = str(path) + "/" + code_list[i + 1][0] + "_result.txt"   #C:\Users\ewp52\Desktop\10-k_data/
# 			with open(name,'w+') as file:
# 				for j in range(len(all_companies_results[i])):
# 					file.write(all_companies_results[i][j])
# 					file.write('\n')
# 		else:
# 			count += 1
# 			if count >= userrequestnum and (count % userrequestnum) == 0:
# 				"""產生一個檔名為 "cikcode to cikcode_result 的txt檔"""
# 				for j in range(len(code_list)):
# 					name = str(path) + "/" + code_list[count - userrequestnum + 1][0] + " to " + code_list[count][0] + "_result.txt"
# 					with open(name,'w+') as file:
#
#
# 			else:
# 				"""count 無法被 userrequestnum 整除的時候，就會剩下最後幾個不符合 userrequestnum 的公司數併在最後一個txt檔"""
#
# 				if (count % userrequestnum) == 1:
# 					"""產生一個檔名為 "cikcode_result 的最後一個txt檔，該檔裡面只有最後一家公司"""
# 					SSS
#
# 				else:
# 					"""產生一個檔名為 "cikcode to cikcode_result 的最後一個txt檔，該檔裡面有最後幾家公司"""
# 					SSS



#------------------------------------------------------------------------------

search = noSpaceLow(input('請輸入關鍵字：'))
sentencecount = int(input('請輸入欲瀏覽的前後段落數：'))
path = input("請指定檔案匯出路徑：").strip('"') + "\\10-k_matching_result"
userrequestnum = int(input("請輸入一份檔案欲包含幾家公司的搜尋結果："))


all_companies_results = []                     # 內容物為多個 公司list，每個  公司list 為「該家公司所有年分 match 文本與 No_match」
for m in range(len(all_article)):                # 每個 m 為一家公司
	one_company_all_years = []
	for n in range(len(all_article[m])):    	# 每個 n 為一個年度
		one_company_all_years.append("Company: " + code_year_list[m][n])
		one_company_all_years.append("See All: " + all_url[m][n])
		lines = all_article[m][n].split("\n")
		# result = []
		#-----------
		#待加入公司cikcode跟url(標題)
		#-----------
		matchcount = 0
		for i in range(len(lines)):
			line = noSpaceLow(lines[i])
			if search in line:
				matchcount += 1
				out = "----Match %d\n" % matchcount
				for j in range(sentencecount * -1, sentencecount + 1):   #j跑-1, 0, 1
					if j < 0:
						if i + j < 0:
							# 處理的是：文本第一段前面不存在的段落
							out += "    前%d段：\n" % (j * -1)
						else:
							out += "    前%d段：%s\n" % (j * -1, re.sub(search, matchcase(search), lines[i + j], flags=re.IGNORECASE).strip())
					elif j == 0:
						out += "    主  段：%s\n" % (re.sub(search, matchcase(search), lines[i + j], flags=re.IGNORECASE).strip())
					else:
						if i + j > len(lines) - 1:
							# 處理的是：文本最後一段後面不存在的段落
							if j == sentencecount:
								out += "    後%d段：\n\n" % (j)
							else:
								out += "    後%d段：\n" % (j)
						else:
							if j == sentencecount:
								out += "    後%d段：%s\n\n" % (j, re.sub(search, matchcase(search), lines[i + j], flags=re.IGNORECASE).strip())
							else:
								out += "    後%d段：%s\n" % (j, re.sub(search, matchcase(search), lines[i + j], flags=re.IGNORECASE).strip())

				one_company_all_years.append(out)

		if matchcount == 0:
			one_company_all_years.append("No_match\n\n")

	all_companies_results.append(one_company_all_years)


	# if len(company_article_set) == resultcompanynum * len(year_list):
	# 	user_request_set.append(company_article_set)
	# 	company_article_set.clear()

		# for i in range(len(result)):
		# 	print(result[i], end = "")

# print(len(all_companies_results))



createFolder(str(path))
write_article(all_companies_results)
