import sys

def merger(f1, f2, f3):
	l1 = f1.readlines()
	l2 = f2.readlines()
	for i in l1:
		if i[0]==">":
			f3.write(i)
			f3.write(l1[l1.index(i)+1])
			for j in l2:
				if j in i:
					f3.write(l2[l1.index(j)+1])
				else:
					continue
		else:
			continue
	return(f3.close())

if __name__ == "__main__":
	f1 = open(sys.argv[1], "r")
	f2 = open(sys.argv[2], "r")
	f3 = open(sys.argv[3], "w+")
	print(merger(f1,f2,f3))
