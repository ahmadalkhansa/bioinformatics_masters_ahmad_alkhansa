import sys

def merger(f1, f2, f3):
	l = f1.readlines()
	s = f2.readlines()
#	print(l)
	for i in l:
		for j in s:
			if i[0:4] == j[0:4]:
				f3.write(">"+j[0:14])
				f3.write('\n')
				f3.write(j[14:len(j)-1])
				f3.write('\n')
				break
			else: continue

		
	return(f3.close())

if __name__ == "__main__":
	f1 = open(sys.argv[1], "r")
	f2 = open(sys.argv[2], "r")
	f3 = open(sys.argv[3], "w+")
	print(merger(f1,f2,f3))

else:
	print("something is wrong")
