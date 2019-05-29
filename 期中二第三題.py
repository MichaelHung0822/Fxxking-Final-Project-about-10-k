fn1 = input()
fh1 = open(fn1, 'r', encoding = 'utf-8')

notneed ='" " \n \t'

all=[]      #原始的文字檔list
for Line1 in fh1 :
	Line1=Line1.rstrip(notneed)
	all.append(Line1)
#print(all)

def clean(x):
	need="0123456789(),$"
	N=[]
	for i in x:   
		if i in need:   
			N.append(i)
	X="".join(N)
	return X
check=[]
for Line2 in all :
	Line3 = clean(Line2)
	check.append(Line3)
#print(check)
A = []
y = 0
z = 0
for i in check :
	y+=1
	A.append([len(i),all[z],y])
	A.sort(key = lambda x: (-x[0],x[2]))
	z+=1
#print(A)

B = []
for j in range(0,10) :
	B.append(A[j])
#print(B)

for k in B :
	print("@"+str(k[2])+":"+" "+k[1])