import sys

def purifier(f1, f2,f3):
	l = f1.read().splitlines()
	m = f2.read().splitlines()
	for n in l:
		ids = n.split("\t")
#		print(ids[2])
		if float(ids[2]) < 30.0:
			for k in m:
#				print(k[1:5])
#				print(ids[0])
				r = ids[0]
#				print(r[0:4])
				if k[1:5] == r[0:4]:
					f3.write(k+"\n"+m[m.index(k)+1]+"\n")
				else: continue
		else: continue
	return(f3.close())

if __name__ == "__main__":
	f1 = open(sys.argv[1], "r")
	f2 = open(sys.argv[2], "r")
	f3 = open(sys.argv[3], "w+")
	print(purifier(f1,f2,f3))
