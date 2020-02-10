import sys


def extractor(inputidsfile, totalfastafile):
	ids = inputidsfile.read().splitlines()
	fasta = totalfastafile.read().splitlines()
	for pdbid in range(len(ids)):
		for fasid in range(0,len(fasta),2):
			if ids[pdbid] in fasta[fasid]:
				output = open(sys.argv[3]+ids[pdbid]+".fasta", "w+")
				output.write(fasta[fasid] +"\n"+ fasta[fasid+1])
				output.close()

if __name__ == "__main__":
	id_inp = open(sys.argv[1], "r")
	fasta_inp = open(sys.argv[2], "r")
	extractor(id_inp, fasta_inp)