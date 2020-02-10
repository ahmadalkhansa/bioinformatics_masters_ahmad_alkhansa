import sys

def extractor(inputfile):
	PDB_tab_results = inputfile.read().splitlines()
	output = open(sys.argv[2] + "PDBs.fasta", 'w+')
	for pdb in range(1,len(PDB_tab_results)):
		pdb_line = PDB_tab_results[pdb].split(',')
		if len(pdb_line) == 6:
			output.write('>'+pdb_line[0]+'_'+pdb_line[1]+'_'+pdb_line[2]+'\n'+pdb_line[4]+'\n')
	output.close()

if __name__=="__main__":
	tabular = open(sys.argv[1], 'r')
	extractor(tabular)
