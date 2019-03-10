# 1
DNA = 'ATGAATGAATGATGAATGAGGGAAAATGAATGA'
def dna2rna(DNA):
	RNA = ''
	i = 0
	while i < len(DNA):
		if DNA[i] != 'T':
			RNA += DNA[i]
			i += 1
		else:
			RNA += 'U'
			i += 1
	return(RNA)
print(dna2rna(DNA))

#2 and 3
genetic_code =  {'GCU':'A','GCC':'A','GCA':'A', 'GCG':'A',
                'CGU':'R','CGC':'R','CGA':'R', 'CGG':'R', 'AGA':'R', 'AGG':'R', 
                'AAU':'N','AAC':'N',
                'GAU':'D','GAC':'D',
                'UGU':'C','UGC':'C',
                'CAA':'Q','CAG':'Q',
                'GAA':'E','GAG':'E',
                'GGU':'G','GGC':'G','GGA':'G', 'GGG':'G', 
                'CAU':'H','CAC':'H',
                'AUU':'I','AUC':'I', 'AUA':'I',
                'UUA':'L','UUG':'L','CUU':'L', 'CUC':'L', 'CUA':'L', 'CUG':'L',
                'AAA':'K','AAG':'K',
                'AUG':'M',
                'UUU':'F','UUC':'F',
                'CCU':'P','CCC':'P','CCA':'P','CCG':'P',
                'UCU':'S','UCC':'S','UCA':'S','UCG':'S','AGU':'S', 'AGC':'S', 
                'ACU':'T','ACC':'T','ACA':'T','ACG':'T',
                'UGG':'W', 
                'UAU':'Y', 'UAC':'Y',
                'GUU':'V', 'GUC':'V', 'GUA':'V', 'GUG':'V',
                'UAG':'STOP', 'UGA':'STOP', 'UAA':'STOP' }
RNA = 'AUGAAUGAAUGAUGAAUGAGGGAAAAUGAAUGA'
def translate(RNA):
	aa = ''
	if len(RNA)%3 == 0: 
		for i in range(0, len(RNA), 3): 
			codon = RNA[i:i + 3]
			aa += genetic_code[codon]
			for j in range(len(aa)):
				if aa[j:j+4] == 'STOP':
					aa = aa[:j]
					
	return(aa)
print(translate(RNA))
