#我修改了~
while True:
    try:
        x = int(input())
    except ValueError:
        print("One more time")         #當使用 try&except，這是在告訴電腦

print(x)
