
# imports
#======================
#視窗用
import tkinter as tk
import tkinter.font as tkFont
from tkinter import ttk
from tkinter import scrolledtext
from tkinter import Menu
from tkinter import Spinbox
from tkinter import messagebox as mBox
import tkinter.filedialog
import webbrowser
#爬蟲用
from bs4 import BeautifulSoup
import requests
from lxml import etree
import re
import csv
import os


#顯示進度條的功能定義
def process(maxT,index= None):  
        maxArrow = 30 #總進度條長度
        if index == None:
                index = i
        else:                
                block = int(index*(maxArrow/maxT))  #現進度條長度
                elseBlock = maxArrow - block #剩下的空格長度
                Per = tk.StringVar()
                percent = index * 100.0 / maxT #完成百分比                
                Pro.configure(text = '['+'▉' * int(block/2) + ' '*elseBlock+']'+str(percent)+'%\r')
                #
                if index >= maxT:
                        index = 0
                        
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
	path = storepath.get()+"\\"+StoreName.get()
	for i in range(len(year_list)) :
		
		
		name = str(path) + "\\" + code + "_" + "article" + "_" + str(year_list[i]) + ".txt"
		with open(name,'w+') as file:
			file.write(article[i])
			file.write('\n')

def write_url(code, document_list, year_list) :
	path = storepath.get()+"\\"+StoreName.get()
	for i in range(len(year_list)) :
		name = str(path) + "\\" + code + "_" + "url" + "_" + str(year_list[i]) + ".txt"
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
        path = storepath.get()+"\\"+StoreName.get()
	# try:
        if csvOrnot == 1:
                code_list = read_csv()
        else:
                if ',' in Cikode.get():
                        code_list = [['cikcode']]
                        tmp = Cikode.get().split(',')
                        for j in tmp:
                                pl = [j]                                
                                code_list.append(pl)
                else:
                        code_list = [['cikcode'],[Cikode.get()]]                             
		
	#測試用
        print(code_list)
        all_article = []
        all_url = []
        createFolder(str(path))

        nowNum = 0
        for i in range(1,len(code_list)):
                document_list = get_url_list(code_list[i][0], year_list)
                article = get_article(document_list)
                write_article(code_list[i][0], article, year_list)
                write_url(code_list[i][0], document_list, year_list)
                all_article.append(article)
                all_url.append(document_list)

                process(maxT = len(code_list)-1 , index = i )

                print(type(article))

                print(document_list)
		
		#測試用
		# print(document_list)
	
	#測試用
	#print(all_url)
	
	# return all_article
	
	#code_year_list = code_year(code_list, year_list)
	
	#code_year_article_list = code_year_article(all_article, code_list, year_list)
	
	#code_year_url_list = code_year_url(all_url, code_list, year_list)
	
	#print(code_year_list)
	# print(code_year_article_list[0][0])
	#print(code_year_url_list)

#--------------------
	#return (code_year_list, code_year_article_list, code_year_url_list)
#--------------------
	
	# return code_year_list, code_year_article_list, code_year_url_list
	# except:
	# print("ERROR")
	
def code_year(code_list, year_list) :
	temp_code_year = []
	code_year_list = []
	
	for i in range(1, len(code_list)) :
		for j in range(len(year_list)) :
			code_year = str(code_list[i][0]) + "-" + str(year_list[j][2:4])
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
#由於tkinter中沒有ToolTip功能，自定義
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
                      font=("微軟正黑體", "10", "normal"))
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
win.configure(background='#9370DB')

f1 = tkFont.Font(size = 12,family = "微軟正黑體")
 
# Add a title       
win.title("10-K Search")
 
# Disable resizing the GUI
win.resizable(0,0)

ttk.Style().configure("TButton", padding=6, relief="flat",   background="#ccc")
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
        talk1.configure(text=name.get()+"\n"+"你才20多歲，你可以成為任何你想成為的人。")
       
        tab2Label.configure(text = name.get()+"\n"+"不要在乎一城一池的得失，要執著。")
    else:
        nameEntered.configure(state='active')
    
 
# Changing our Label
tk.Label(monty, text="輸入暱稱:",font = f1).grid(column=0, row=0, sticky='W')
 
# Adding a Textbox Entry widget
name = tk.StringVar()
nameEntered = ttk.Entry(monty, width=12, textvariable=name,state = 'active',font = f1)
nameEntered.grid(column=0, row=1, sticky='W')
  
ttk.Label(monty, text="請選擇一位心靈導師:",font = f1).grid(column=1, row=0,sticky='W')
 
# Adding a Combobox
teacher = tk.StringVar()
teacherChosen = ttk.Combobox(monty, width=12, textvariable=teacher,font = f1)
teacherChosen['values'] = ( '孔令傑老師','盧信銘老師','林世銘老師','林嬋娟老師','高偉娟老師','李艷榕老師','陳坤志老師','曾智揚老師')
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
createToolTip(action,'確認後不可修改')
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

codeName = ttk.Label(monty2, text="公司代碼 : ", state='disabled',font = f1)
codeName.grid(column=0, row=2, sticky='W')  

# Adding a Textbox Entry widget
Cikode = tk.StringVar() 
CikodeEntered = ttk.Entry(monty2, width=12, textvariable=Cikode, state='disabled',font = f1)
CikodeEntered.grid(column=1, row=2, sticky='W')

def openFile():
    filenames = tkinter.filedialog.askopenfilename()
    filename = ""
    for i in filenames:
        if i == "/":
            filename += "\\"
            continue
        filename += i    
    if len(filename) != 0:
        if filename[-3:] == "csv":
            fileLabel.configure(text = "您選擇的文件是：")        
            fileName.set(filename)
        else:
            mBox.showinfo("檔案類型錯誤","您選擇的檔案類型非csv檔，請重新選擇！")
    else:
        fileLabel.configure(text = "您沒有選擇任何文件")
        fileEntered.configure(state='disabled')

fileLabel = ttk.Label(monty2 , text = "您選擇的文件是：",state='disabled',font = f1)
fileLabel.grid(column=0, row=3,sticky='W')
fileName = tk.StringVar() 
fileEntered = ttk.Entry(monty2, width=12, textvariable=fileName,state='disabled',font = f1)
fileEntered.grid(column=1, row=3, sticky='W')
btn = tk.Button(monty2,text="瀏覽",command=openFile, state='disabled',relief='raised',activeforeground="#696969")
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
        tab2Label.configure(text = name.get()+"\n"+"請輸入公司代碼，接著選擇年份及關鍵字。\n並設定輸出資料夾。")
    elif radSel == 1:
        CikodeEntered.configure(state='disabled')
        codeName.configure(state='disabled')
        btn.configure(state='normal')
        fileEntered.configure(state = 'readonly')
        fileLabel.configure(state = 'normal')
        tab2Label.configure(text = name.get()+"\n"+"請匯入公司代碼的csv檔，接著選擇年份及關鍵字。\n並設定輸出資料夾。")
                     

# create three Radiobuttons using one variable
radVar = tk.IntVar()
# Selecting a non-existing index value for radVar
radVar.set(99)

for col in range(0,2):
    #curRad = 'rad' + str(col)  
    curRad = tk.Radiobutton(monty2, text=values[col], variable=radVar, value=col, command=radCall,font = f1)
    curRad.grid(column=col, row=0, sticky=tk.W, columnspan=2)


ttk.Label(monty2, text="起迄年份 : ").grid(column=0, row=4, sticky='W')
    
yearst = tk.StringVar()
yearstChoice = ttk.Combobox(monty2, width=10, textvariable = yearst,font = f1)
yr=[]
for i in range(50):
    yr.append(2019-i)
yearstChoice['values'] = yr
yearstChoice.grid(column=1, row=4, sticky='W')
yearstChoice.current(0)  #设置初始显示值，值为元组['values']的下标
yearstChoice.config(state='readonly')  #设为只读模式

yeared = tk.StringVar()
yearedChoice = ttk.Combobox(monty2, width=10, textvariable = yeared,font = f1)
yr=[]
for i in range(50):
    yr.append(2019-i)
yearedChoice['values'] = yr
yearedChoice.grid(column=2, row=4, sticky='W')
yearedChoice.current(0)  #设置初始显示值，值为元组['values']的下标
yearedChoice.config(state='readonly')  #设为只读模式
yearL = tk.StringVar()
"""
def yearcheck():
    try:
        if int(yeared.get()) >= int(yearst.get()):      
            yl=""
            for i in range(int(yearst.get()),int(yeared.get())+1):
                yl += str(i)+" "
        yearL.set(yl)
    except:
        mBox.showinfo("年份錯誤","您選擇的年份有誤，請重新選擇！")
        yearedChoice.current(0)
"""

#yearCheck = ttk.Button(monty2,text="確認年份",width=7,command=yearcheck)
#yearCheck.grid(column=3,row=4)
#yearPrint = ttk.Entry(monty2,width=30, textvariable=yearL, state='disabled')
#yearPrint.grid(column=1, row=5,columnspan=3, sticky='W')


"""
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
"""
ttk.Label(monty2, text="搜尋關鍵字 : ",font = f1).grid(column=0, row=6, sticky=tk.W)

keyWord = tk.StringVar() 
keyWordEntered = ttk.Entry(monty2, width=12, textvariable=keyWord,font = f1)
keyWordEntered.grid(column=1, row=6, sticky='W')

outset = ttk.LabelFrame(tab2, text='輸出設定')
outset.grid(column=0, row=1,padx=8, pady=4,sticky=tk.W)

ttk.Label(outset, text="資料夾名稱 : ").grid(column=0, row=0, sticky=tk.W) 
# Adding a Textbox Entry widget
StoreName = tk.StringVar()
StoreNameEntered = ttk.Entry(outset, width=12, textvariable=StoreName,font = f1)
StoreNameEntered.grid(column=1, row=0, sticky=tk.W)

ttk.Label(outset, text="儲存資料夾 : ").grid(column=0, row=1, sticky=tk.W)

def storePath():
    path_ = tk.filedialog.askdirectory()
    path = ""
    for i in path_:
        if i == "/":
            path += "\\"
            continue
        path += i    
    storepath.set(path)

storepath = tk.StringVar()
storePathEntered = ttk.Entry(outset, width=12, textvariable=storepath)
storePathEntered.grid(column=1, row=1, sticky=tk.W)
storebtn = tk.Button(outset,text="瀏覽",command=storePath,relief='raised',activeforeground="#696969")
storebtn.grid(column=2, row=1, sticky=tk.W)

ttk.Label(outset, text="資料分組 : ").grid(column=0, row=2, sticky='W')
scr=tk.StringVar()
scr.set(10)
# Spinbox callback 
def _spin():
    value = spin.get()
    #print(value)
spin = Spinbox(outset, from_=1,to=100, width=5, bd=8, command=_spin, increment = 5, textvariable = scr)
spin.grid(column=1, row=2,sticky='W')
#ttk.Label(outset, text="(可以自行輸入1-100整數)").grid(column=1, row=3,columnspan = 2, sticky=tk.W)

Pro= ttk.Label(outset, text='['+" "*50+']'+' 0.0%',width = 30)
Pro.grid(column=0, row=3, columnspan = 3, sticky='W')

star =  ttk.LabelFrame(tab2,text = "開始輸出")
star.grid(column = 0,row = 1,sticky = "E")
 
#######按鍵後開始
path = ""
code = []
def startAll():
    #try:
        if radVar.get() == 99:
            mBox.showinfo("錯誤","請選擇代碼輸入")
            tab2Label.configure(text = name.get()+"\n"+"選一個指定公司代碼的方式。")
        elif radVar.get() == 0 and Cikode.get() =="":
            mBox.showinfo("錯誤","請輸入代碼")
            tab2Label.configure(text = name.get()+"\n"+"代碼呢？")
        elif radVar.get() == 1 and fileName.get() =="":
            mBox.showinfo("錯誤","請選擇代碼清單路徑")
            tab2Label.configure(text = name.get()+"\n"+"代碼清單呢？")
        elif int(yeared.get()) <  int(yearst.get()):
            mBox.showinfo("錯誤","您選擇的年份有誤，請重新選擇！")
            tab2Label.configure(text = name.get()+"\n"+"起訖...先有開始，才會有結束。")
            yearedChoice.current(0)
        #elif keyWord.get()=="":
        elif StoreName.get() == "":
            mBox.showinfo("錯誤","輸出資料夾名稱為空")
            tab2Label.configure(text = name.get()+"\n"+"取一個知道在幹嘛的資料夾名字吧。")
        elif storepath.get() == "":
            mBox.showinfo("錯誤","請選擇輸出路徑")
            tab2Label.configure(text = name.get()+"\n"+"請存在你找的到的地方。")
        else:      
            yl=""
            for i in range(int(yearst.get()),int(yeared.get())+1):
                yl += str(i)+" "
            yearL.set(yl)
            check = mBox.askyesno("確認資訊", "請再次確認輸入的代碼、年份、關鍵字，及輸出資料。\n要繼續嗎？")
            if check == 1:
                openGame = mBox.askyesno("開啟遊戲", "爬蟲需要一些時間，請問要開啟網頁小遊戲嗎？\n爬蟲完成後將出現提示視窗。")
                if openGame == 1:
                    webbrowser.open("https://chromedino.com/", new=2, autoraise=True)
                    if teacher.get() == "孔令傑老師" or "盧信銘老師":
                        tab2Label.configure(text = name.get()+"\n"+"chrome的恐龍遊戲意外地受歡迎，\n有興趣可以自己換角色。\n......順便學一下網頁語法。")
                    else:
                        tab2Label.configure(text = name.get()+"\n"+"遊戲玩膩了還沒爬完的話...不如複習一下中會？")   
                year_list = yearL.get().split()                
                if radVar.get() == 1:        
                    all = start_crawling(year_list,1)
                    mBox.showinfo("完成","資料已儲存在"+StoreName.get()+"資料夾")
                    tab2Label.configure(text = name.get()+"\n"+"恭喜完成了一批爬蟲，\n你離畢業又更進一步囉！")
                    """
                            #-------------------------
                    code_year_list = all[0]
                    code_year_article_list = all[1]
                    code_year_url_list = all[2]
                            #-------------------------
                      """      
                elif radVar.get() == 0:        
                    all = start_crawling(year_list,0)
                    mBox.showinfo("完成","資料已儲存在"+StoreName.get()+"資料夾")
                    tab2Label.configure(text = name.get()+"\n"+"恭喜完成了一批爬蟲，離畢業又更進一步囉！")
                    """       
                            #-------------------------
                    code_year_list = all[0]
                    code_year_article_list = all[1]
                    code_year_url_list = all[2]
                        #-------------------------
                        """
                
        
    #except:
            #mBox.showinfo("錯誤","程式執行錯誤，請檢查輸入資訊！")
#######
startOver = tk.Button(star,text="開始",width=10,height = 3,command=startAll)
startOver.grid(column = 0,row  = 0,rowspan = 2,sticky = tk.E)



# Create a container to hold labels
labelsFrame2 = ttk.LabelFrame(tab2)
labelsFrame2.grid(column=0, row=2,columnspan=4, sticky=tk.W)
 
# Place labels into the container element - vertically
teaImg2 = tk.Label(labelsFrame2,image = img).grid(column=0,row=0,sticky = tk.W)
tab2Label = ttk.Label(labelsFrame2, text="",font = f1)
tab2Label.grid(column=1, row=0,sticky = tk.W)

#createToolTip(CikodeEntered,'請輸入公司代碼')
#createToolTip(fileEntered,'請選擇要匯入的csv檔案')
createToolTip(btn,'選取檔案路徑')
#createToolTip(yearChoice, '請選擇年份後按加入')
#createToolTip(add, '請選擇年份後按加入')
#createToolTip(clear, '清除所選年分')
createToolTip(keyWordEntered, '請輸入搜尋關鍵字')
createToolTip(StoreNameEntered, '請設定欲儲存輸出資料的資料夾名稱')
createToolTip(storePathEntered, '請設定資料夾路徑')
createToolTip(storebtn,'選取檔案路徑')
createToolTip(spin,'選擇資料分檔筆數，可以自行輸入1-100整數')
#createToolTip(startOver,'確定輸入資料正確後開始')

for child in monty2.winfo_children(): 
    child.grid_configure(padx=3,pady=1)
for child in outset.winfo_children(): 
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



