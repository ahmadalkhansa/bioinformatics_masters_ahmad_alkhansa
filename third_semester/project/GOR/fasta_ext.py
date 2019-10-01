import sys

def extractor(fasta):
	n = fasta.read().splitlines()
	for k in n:
		if k[0] == ">":
			p = k.split(",")
			name_out = p[0][1:]+"."+p[1]
			f = open(name_out+".fasta", "w+")
			f.write(p[0]+"."+p[1]+"\n"+n[n.index(k)+1])
			f.close()
		else: continue

if __name__ == "__main__":
	input_file = open(sys.argv[1], "r")
	extractor(input_file)
