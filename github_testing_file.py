while True:
    try:
        x = int(input())
    except ValueError:
        print("One more time")         #當使用 try&except，這是在告訴電腦

print(x)


'''
while True:
    x = int(input())

print(x)
'''



'''
d = {}   #字典資料庫，所有用戶的帳戶名和明碼都存在這裡
d["D"] = 123
d["A"] = 1234
d["V"] = 12345
d["I"] = 123456
d["E"] = 1234567


#只要帳戶名或是密碼一個出錯，就會直接跳出程式
name = input('您的帳戶名：')
if name in d:
    password = int(input('您的密碼：'))
    if d[name] == password:
        print('進入系統')
    else:
        print('密碼錯誤，請重新輸入')
else:
    print('帳戶名錯誤，請重新輸入')



#當帳戶名或是密碼出錯，程式會跳回迴圈原點而不是直接離開
while True:
    name = input('您的帳戶名：')
    if name in d:
        break
    else:
        print('帳戶名錯誤，請重新輸入')

while True:
    password = int(input('您的密碼：'))
    if d[name] == password:
        print('進入系統')
        break
    else:
        print('密碼錯誤，請重新輸入')
'''
