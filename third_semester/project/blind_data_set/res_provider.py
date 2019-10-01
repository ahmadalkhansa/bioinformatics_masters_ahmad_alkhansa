import sys
# sou):
def res(fou, mou): #,sou):
	l = fou.read().splitlines()
	p = mou.read().splitlines()
#	tlist = []
	for n in l:
		tlist = []
#		print(tlist)
		ids = n.split(" ")
		for i in ids:
#			print(tlist)
			for j in p:
				header = j.split(" ")
#					print(header)
				for k in header:
#					print(k)
					if len(k) == 5:
						if k[1:5] == i:
#							print(k[1:5]+"_"+header[2])
							tlist.append(k[1:5]+"_"+header[2])
#							print(tlist)
							break
						else:
							continue
					else:
						continue
		tlist.sort(key=lambda x: float(x[5:9]))
		
		print(*tlist)
#print(n)
	return('')

if __name__ == "__main__":
	fou = open(sys.argv[1], "r")
	mou = open(sys.argv[2], "r")
#	sou = open(sys.argv[3], "w+")
	print(res(fou, mou))#,sou))
