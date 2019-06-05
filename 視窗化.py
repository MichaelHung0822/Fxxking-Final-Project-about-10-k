
# imports
#======================
#視窗用
import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext
from tkinter import Menu
from tkinter import Spinbox
from tkinter import messagebox as mBox
import tkinter.filedialog
from PIL import Image,ImageTk
#爬蟲用
from bs4 import BeautifulSoup
import requests
from lxml import etree
import re
import csv
import os

#===================================================
#爬蟲主要函數定義
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
	url = "https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=" + str(cikcode) +"&type=10-k&dateb=&owner=exclude&count=40"
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
			if "-" + str(year_list[i][2:4]) + "-" in link :			#決定想要那些年分
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
	with open(fileName.get(), newline = "") as csvfile : #fn是匯入的檔案路徑 #crawltest0426.csv 是匯入的檔名
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

def write_article(code, article, year_list) :
	for i in range(len(year_list)) :
		name = str(path) + "/" + code + "_" + "article" + "_" + str(year_list[i]) + ".txt"
		with open(name,'w+') as file:
			file.write(article[i])
			file.write('\n')

def write_url(code, document_list, year_list) :
	for i in range(len(year_list)) :
		name = str(path) + "/" + code + "_" + "url" + "_" + str(year_list[i]) + ".txt"
		with open(name,'w+') as file:
			file.write(document_list[i])
			file.write('\n')
	
	
	# for i in range(len(year_list)) :
		# name = str(path) + "/" + code + "_" + "url" + "_" + str(year_list[i]) + ".txt"
		 
		# for idx, j in enumerate(document_list) :
			# with open(name,'w+') as file:
				# file.write(j)
				# file.write('\n')
		
	# for i, j in document_list, range(len(year_list)) :
		
		# name = str(path) + "/" + code + "_" + "url" + "_" + str(year_list[j]) + ".txt"
		# with open(name,'w+') as file:
			# file.write(i)
			# file.write('\n')


#--------------------
#正式執行程式
#--------------------

def start_crawling(year_list,csvOrnot):
	# try:
	if csvOrnot == 1:
		code_list = read_csv()
	else:
		code_list = [['cikcode'],[Cikode.get()]]
	
	#測試用
	print(code_list)
	
	all_article = []
	all_url = []
	path = storepath.get()+"\\"+StoreName.get()
	createFolder(str(path))
	
	for i in range(1,len(code_list)):
		document_list = get_url_list(code_list[i][0], year_list)
		article = get_article(document_list)
		write_article(code_list[i][0], article, year_list)
		write_url(code_list[i][0], document_list, year_list)
		all_article.append(article)
		all_url.append(document_list)
		
		print(type(article))
		
		print(document_list)
		
		#測試用
		# print(document_list)
	
	#測試用
	#print(all_url)
	
	# return all_article
	
	code_year_list = code_year(code_list, year_list)
	
	code_year_article_list = code_year_article(all_article, code_list, year_list)
	
	code_year_url_list = code_year_url(all_url, code_list, year_list)
	
	print(code_year_list)
	# print(code_year_article_list[0][0])
	print(code_year_url_list)

#--------------------
	return (code_year_list, code_year_article_list, code_year_url_list)
#--------------------
	
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
#======================================================
#視窗架構
#由于tkinter中没有ToolTip功能，所以自定义这个功能如下
class ToolTip(object):
    def __init__(self, widget):
        self.widget = widget
        self.tipwindow = None
        self.id = None
        self.x = self.y = 0
 
    def showtip(self, text):
        "Display text in tooltip window"
        self.text = text
        if self.tipwindow or not self.text:
            return
        x, y, _cx, cy = self.widget.bbox("insert")
        x = x + self.widget.winfo_rootx() + 27
        y = y + cy + self.widget.winfo_rooty() +27
        self.tipwindow = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(1)
        tw.wm_geometry("+%d+%d" % (x, y))
 
        label = tk.Label(tw, text=self.text, justify=tk.LEFT,
                      background="#ffffe0", relief=tk.SOLID, borderwidth=1,
                      font=("tahoma", "8", "normal"))
        label.pack(ipadx=1)
 
    def hidetip(self):
        tw = self.tipwindow
        self.tipwindow = None
        if tw:
            tw.destroy()
            
#===================================================================          
def createToolTip( widget, text):
    toolTip = ToolTip(widget)
    def enter(event):
        toolTip.showtip(text)
    def leave(event):
        toolTip.hidetip()
    widget.bind('<Enter>', enter)
    widget.bind('<Leave>', leave)
 
# Create instance
win = tk.Tk()   
 
# Add a title       
win.title("10-K Search")
 
# Disable resizing the GUI
win.resizable(0,0)
 
# Tab Control introduced here --------------------------------------
tabControl = ttk.Notebook(win)          # Create Tab Control
 
tab1 = ttk.Frame(tabControl)            # Create a tab 
tabControl.add(tab1, text='使用者資料')      # Add the tab
 
tab2 = ttk.Frame(tabControl)            # Add a second tab
tabControl.add(tab2, text='搜尋內容')      # Make second tab visible
 
tabControl.pack(expand=1, fill="both")  # Pack to make visible
# ~ Tab Control introduced here -----------------------------------------
 
#---------------Tab1控件介绍------------------#
# We are creating a container tab3 to hold all other widgets
monty = ttk.LabelFrame(tab1, text='使用者名稱')
monty.grid(column=0, row=0, padx=8, pady=4)


# Modified Button Click Function
def clickMe():
    answer = mBox.askyesno("確認暱稱", "您確定設定這個暱稱及心靈導師嗎？\n後續將無法修改") 
    if answer == True:
        action.configure(text='Hello,\n' + name.get())
        action.configure(state='disabled')    # Disable the Button Widget
        nameEntered.configure(state='disabled')
        
        # Place labels into the container element - vertically
        img.configure(file = teacher.get()+".gif")
        talk1.configure(text=name.get()+"\n"+"你才20多歲，你可以成为任何你想成為的人。")
       
        tab2Label.configure(text = name.get()+"\n"+"不要在乎一城一池的得失，要执着。")
    else:
        nameEntered.configure(state='active')
    
 
# Changing our Label
ttk.Label(monty, text="輸入暱稱:").grid(column=0, row=0, sticky='W')
 
# Adding a Textbox Entry widget
name = tk.StringVar()
nameEntered = ttk.Entry(monty, width=12, textvariable=name,state = 'active')
nameEntered.grid(column=0, row=1, sticky='W')
  
ttk.Label(monty, text="请选择一位心靈導師:").grid(column=1, row=0,sticky='W')
 
# Adding a Combobox
teacher = tk.StringVar()
teacherChosen = ttk.Combobox(monty, width=12, textvariable=teacher)
teacherChosen['values'] = ( '孔令傑老師','盧信銘老師','林世銘老師')
teacherChosen.grid(column=1, row=1)
teacherChosen.current(0)  #设置初始显示值，值为元组['values']的下标
teacherChosen.config(state='readonly')  #设为只读模式

# Adding a Button
action = ttk.Button(monty,text="確認",width=10,command=clickMe)   
action.grid(column=2,row=1,rowspan=2,ipady=7)

labelsFrame = ttk.LabelFrame(monty)
labelsFrame.grid(column=0, row=3,columnspan=4,sticky=tk.W)

img = tk.PhotoImage()
teaImg = tk.Label(labelsFrame,image = img).grid(column=0,row=0,sticky = tk.W)
talk1 = ttk.Label(labelsFrame)
talk1.grid(column=1, row=0, sticky=tk.W)

# Add Tooltip
createToolTip(action,'確認')
createToolTip(nameEntered,'請輸入暱稱')
createToolTip(teacherChosen, '請選擇導師')

# 一次性控制各控件之间的距离
for child in monty.winfo_children(): 
    child.grid_configure(padx=3,pady=1)
# 单独控制个别控件之间的距离
action.grid(column=2,row=1,rowspan=2,padx=6)
#---------------Tab1控件介绍------------------#
 
 
#---------------Tab2控件介绍------------------#
# We are creating a container tab3 to hold all other widgets -- Tab2
monty2 = ttk.LabelFrame(tab2, text='搜尋條件')
monty2.grid(column=0, row=0, padx=8, pady=4)
"""
ttk.Label(monty2, text="公司名稱 : ").grid(column=0, row=0, sticky='W')
 
# Adding a Textbox Entry widget
CopName = tk.StringVar()
CopNameEntered = ttk.Entry(monty2, width=12, textvariable=CopName)
CopNameEntered.grid(column=1, row=0, sticky='W')
"""
codeName = ttk.Label(monty2, text="公司代碼 : ", state='disabled')
codeName.grid(column=0, row=2, sticky='W')          

# Adding a Textbox Entry widget
Cikode = tk.StringVar() 
CikodeEntered = ttk.Entry(monty2, width=12, textvariable=Cikode, state='disabled')
CikodeEntered.grid(column=1, row=2, sticky='W')

def openFile():
    filename = tkinter.filedialog.askopenfilename()
    if len(filename) != 0:        
        fileLabel.configure(text = "您選擇的文件是：")
        fileName.set(filename)
    else:
        fileLabel.configure(text = "您沒有選擇任何文件")
        fileEntered.configure(state='disabled')

fileLabel = tk.Label(monty2 , text = "您选择的文件是：",state='disabled')
fileLabel.grid(column=0, row=3,sticky='W')
fileName = tk.StringVar() 
fileEntered = ttk.Entry(monty2, width=12, textvariable=fileName,state='disabled')
fileEntered.grid(column=1, row=3, sticky='W')
btn = tk.Button(monty2,text="瀏覽",command=openFile, state='disabled')
btn.grid(column=2, row=3, sticky='W')


# Radiobutton list
values = ["輸入代碼", "匯入代碼清單(csv檔案)"]
 
# Radiobutton callback function
def radCall():
    radSel=radVar.get()
    if   radSel == 0:
        btn.configure(state='disabled')
        fileEntered.configure(state = 'disabled')
        fileLabel.configure(state = 'disabled')
        CikodeEntered.configure(state='normal')
        codeName.configure(state='normal')
    elif radSel == 1:
        CikodeEntered.configure(state='disabled')
        codeName.configure(state='disabled')
        btn.configure(state='normal')
        fileEntered.configure(state = 'readonly')
        fileLabel.configure(state = 'normal')
                     

# create three Radiobuttons using one variable
radVar = tk.IntVar()
# Selecting a non-existing index value for radVar
radVar.set(99)

for col in range(0,2):
    #curRad = 'rad' + str(col)  
    curRad = tk.Radiobutton(monty2, text=values[col], variable=radVar, value=col, command=radCall)
    curRad.grid(column=col, row=0, sticky=tk.W, columnspan=2)


ttk.Label(monty2, text="年份 : ").grid(column=0, row=4, sticky='W')
    
year = tk.StringVar()
yearChoice = ttk.Combobox(monty2, width=10, textvariable = year)
yr=[]
for i in range(50):
    yr.append(2019-i)
yearChoice['values'] = yr
yearChoice.grid(column=1, row=4, sticky='W')
yearChoice.current(0)  #设置初始显示值，值为元组['values']的下标
yearChoice.config(state='readonly')  #设为只读模式

def addYear():
    value = year.get()
    #print(value)
    last = yearL.get()
    yearL.set(last+value+" ")

def clearYear():
    yearL.set("")
        
add = ttk.Button(monty2,text="加入",width=7,command=addYear)
clear = ttk.Button(monty2,text="清除",width=7,command = clearYear)
add.grid(column=2,row=4)
clear.grid(column=3,row=4)

yearL = tk.StringVar() 
yearLEntered = ttk.Entry(monty2, width=30, textvariable=yearL, state='disabled')
yearLEntered.grid(column=1, row=5,columnspan=3, sticky='W')

ttk.Label(monty2, text="搜尋關鍵字 : ").grid(column=0, row=6, sticky=tk.W)

keyWord = tk.StringVar() 
keyWordEntered = ttk.Entry(monty2, width=12, textvariable=keyWord)
keyWordEntered.grid(column=1, row=6, sticky='W')

outset = ttk.LabelFrame(tab2, text='輸出設定')
outset.grid(column=0, row=1,padx=8, pady=4,sticky=tk.W)

ttk.Label(outset, text="資料夾名稱 : ").grid(column=0, row=0, sticky=tk.W) 
# Adding a Textbox Entry widget
StoreName = tk.StringVar()
StoreNameEntered = ttk.Entry(outset, width=12, textvariable=StoreName)
StoreNameEntered.grid(column=1, row=0, sticky=tk.W)

ttk.Label(outset, text="儲存資料夾 : ").grid(column=0, row=1, sticky=tk.W)

ttk.Label(outset, text="資料分組 : ").grid(column=0, row=2, sticky='W')
scr=tk.StringVar()
scr.set(10)
# Spinbox callback 
def _spin():
    value = spin.get()
    #print(value)
spin = Spinbox(outset, from_=1,to=100, width=5, bd=8, command=_spin, increment = 5, textvariable = scr)
spin.grid(column=1, row=2)
ttk.Label(outset, text="(可以自行輸入1-100整數)").grid(column=1, row=3,columnspan = 2, sticky=tk.W)



def storePath():
    path_ = tk.filedialog.askdirectory()
    storepath.set(path_)

storepath = tk.StringVar()
storePathEntered = ttk.Entry(outset, width=12, textvariable=storepath)
storePathEntered.grid(column=1, row=1, sticky=tk.W)
storebtn = tk.Button(outset,text="瀏覽",command=storePath)
storebtn.grid(column=2, row=1, sticky=tk.W)

startBtn = ttk.LabelFrame(tab2,text="開始輸出")
startBtn.grid(column=0, row=1 ,columnspan=2,sticky=tk.E)
#######按鍵後開始
year_list = []
path=""
code = []
def startAll():
        check = mBox.askyesno("確認資訊", "請再次確認輸入的代碼、年份、關鍵字，及輸出資料。\n要繼續嗎？")
        if check == 1:
                year_list = yearL.get().split()
                if radVar.get() == 1:        
                        all = start_crawling(year_list,1)
                        
                        #-------------------------
                        code_year_list = all[0]
                        code_year_article_list = all[1]
                        code_year_url_list = all[2]
                        #-------------------------
                        
                elif radVar.get() == 0:        
                        all = start_crawling(year_list,0)
                        
                        #-------------------------
                        code_year_list = all[0]
                        code_year_article_list = all[1]
                        code_year_url_list = all[2]
                        #-------------------------
        
#######
startOver = tk.Button(startBtn,text="開始",width=15,height =3,command=startAll)
startOver.grid(column = 0,row  = 0,rowspan = 2,sticky = tk.E)

# Create a container to hold labels
labelsFrame2 = ttk.LabelFrame(tab2)
labelsFrame2.grid(column=0, row=2,columnspan=4, sticky=tk.W)
 
# Place labels into the container element - vertically
teaImg2 = tk.Label(labelsFrame2,image = img).grid(column=0,row=0,sticky = tk.W)
tab2Label = ttk.Label(labelsFrame2, text="")
tab2Label.grid(column=1, row=0,sticky = tk.W)


for child in monty2.winfo_children(): 
    child.grid_configure(padx=3,pady=1)
for child in labelsFrame2.winfo_children(): 
    child.grid_configure(padx=8,pady=4)
#---------------Tab2控件介绍------------------#
 
# Place cursor into name Entry
nameEntered.focus()      
#======================
# Start GUI
#======================
win.mainloop()



