import sys

def ran(f1, f2, f3):
	n = f1.read().splitlines()
	m = f2.read().splitlines()
	for l in n:
		for k in m:
			if l == k:
				f3.write(l + "\n"+m[m.index(l)+1]+"\n")
			else: continue
	return('')
if __name__ == "__main__":
	f1 = open(sys.argv[1], "r")
	f2 = open(sys.argv[2], "r")
	f3 = open(sys.argv[3], "w+")
	print(ran(f1,f2,f3))
