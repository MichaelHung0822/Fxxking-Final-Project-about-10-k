
# imports
#======================
import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext
from tkinter import Menu
from tkinter import Spinbox
from tkinter import messagebox as mBox
import tkinter.filedialog
 
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
    answer = mBox.askyesno("確認暱稱", "您確定設定這個暱稱嗎？\n後續將無法修改") 
    if answer == True:
        action.configure(text='Hello,\n' + name.get())
        action.configure(state='disabled')    # Disable the Button Widget
        nameEntered.configure(state='disabled')
        
        labelsFrame = ttk.LabelFrame(monty)
        labelsFrame.grid(column=1, row=3,columnspan=4,sticky=tk.W)
        # Place labels into the container element - vertically
        ttk.Label(labelsFrame, text=name.get()+"\n"+"你才20多歲，你可以成为任何你想成為的人。").grid(column=0, row=0, sticky=tk.W)

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
book = tk.StringVar()
bookChosen = ttk.Combobox(monty, width=12, textvariable=book)
bookChosen['values'] = ( '孔令傑 老師','盧信銘 老師','林世銘 老師')
bookChosen.grid(column=1, row=1)
bookChosen.current(0)  #设置初始显示值，值为元组['values']的下标
bookChosen.config(state='readonly')  #设为只读模式

# Adding a Button
action = ttk.Button(monty,text="確認",width=10,command=clickMe)   
action.grid(column=2,row=1,rowspan=2,ipady=7)

# Add Tooltip
createToolTip(action,'確認')
createToolTip(nameEntered,'請輸入暱稱')
createToolTip(bookChosen, '請選擇導師')

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
    filenames = tkinter.filedialog.askopenfilenames()
    if len(filenames) != 0:
        string_filename =""
        for i in range(0,len(filenames)):
            string_filename += str(filenames[i])+"\n"
        fileLabel.configure(text = "您選擇的文件是：")
        fileName.set(string_filename)
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
year = ttk.Combobox(monty2, width=10, textvariable = year)
yr=[]
for i in range(50):
    yr.append(2019-i)
year['values'] = yr
year.grid(column=1, row=4, sticky='W')
year.current(0)  #设置初始显示值，值为元组['values']的下标
year.config(state='readonly')  #设为只读模式

ttk.Label(monty2, text="資料分組 : ").grid(column=0, row=5, sticky='W')
scr=tk.StringVar()
scr.set(10)
# Spinbox callback 
def _spin():
    value = spin.get()
    #print(value)
spin = Spinbox(monty2, from_=1,to=100, width=5, bd=8, command=_spin, increment = 5, textvariable = scr)
spin.grid(column=1, row=5)
ttk.Label(monty2, text="(可以自行輸入1-100整數)").grid(column=2, row=5,columnspan = 2, sticky='W')
 
# Create a container to hold labels
labelsFrame = ttk.LabelFrame(monty2)
labelsFrame.grid(column=0, row=6,columnspan=4, sticky=tk.W)
 
# Place labels into the container element - vertically
ttk.Label(labelsFrame, text="你才25岁，你可以成为任何你想成为的人。").grid(column=0, row=0)
ttk.Label(labelsFrame, text="不要在乎一城一池的得失，要执着。").grid(column=0, row=1,sticky=tk.W)
 

for child in monty2.winfo_children(): 
    child.grid_configure(padx=3,pady=1)
for child in labelsFrame.winfo_children(): 
    child.grid_configure(padx=8,pady=4)
#---------------Tab2控件介绍------------------#
 
"""
#---------------Tab3控件介绍------------------#
tab3 = tk.Frame(tab3, bg='#AFEEEE')
tab3.pack()
for i in range(2):
    canvas = 'canvas' + str(col)
    canvas = tk.Canvas(tab3, width=162, height=95, highlightthickness=0, bg='#FFFF00')
    canvas.grid(row=i, column=i)
#---------------Tab3控件介绍------------------#
 """
 
#----------------菜单栏介绍-------------------#    
# Exit GUI cleanly
def _quit():
    win.quit()
    win.destroy()
    exit()
    
# Creating a Menu Bar
menuBar = Menu(win)
win.config(menu=menuBar)
 
# Add menu items
fileMenu = Menu(menuBar, tearoff=0)
fileMenu.add_separator()
fileMenu.add_command(label="退出", command=_quit)

 
 
# Display a Message Box
def _msgBox1():
    mBox.showinfo('Python Message Info Box', '通知：程序运行正常！')
def _msgBox2():
    mBox.showwarning('Python Message Warning Box', '警告：程序出现错误，请检查！')
def _msgBox3():
    mBox.showwarning('Python Message Error Box', '错误：程序出现严重错误，请退出！')
def _msgBox4():
    answer = mBox.askyesno("Python Message Dual Choice Box", "你喜欢这篇文章吗？\n您的选择是：") 
    if answer == True:
        mBox.showinfo('显示选择结果', '您选择了“是”，谢谢参与！')
    else:
        mBox.showinfo('显示选择结果', '您选择了“否”，谢谢参与！')
 
# Add another Menu to the Menu Bar and an item
msgMenu = Menu(menuBar, tearoff=0)
msgMenu.add_command(label="通知 Box", command=_msgBox1)
msgMenu.add_command(label="警告 Box", command=_msgBox2)
msgMenu.add_command(label="错误 Box", command=_msgBox3)
msgMenu.add_separator()
msgMenu.add_command(label="判断对话框", command=_msgBox4)
menuBar.add_cascade(label="消息框", menu=msgMenu)
#----------------菜单栏介绍-------------------#
 

# Place cursor into name Entry
nameEntered.focus()      
#======================
# Start GUI
#======================
win.mainloop()
