seq1 = 'ACTTAAAAGCTACG'
seq2 = 'TTGAATGCCCCCTACGA'

matrix = [[0 for i in range(len(seq1)+1)]for j in range(len(seq2)+1)]

traceback = [['stop' for I in range(len(seq1)+1)]for J in range(len(seq2)+1)]

scoring = {'match': 2, 'mismatch': 0, 'gap': -2}
submat = {'A':{'A':2, 'C':0, 'T':0, 'G':1}, \
'C':{'A':0, 'C':2, 'T':1, 'G':0}, \
'T':{'A':0, 'C':1, 'T':2, 'G':0}, \
'G':{'A':1, 'C':0, 'T':0, 'G':2}}

def scoringmatch(nuc1, nuc2):
	return(submat[nuc1][nuc2])
#	if nuc1 == nuc2:
#		score_match = scoring['match']
#		return score_match
#	else:
#		score_mismatch = scoring['mismatch']
#		return score_mismatch
def smw(seq1, seq2, matrix,traceback):
	scores = []
	path = []
	score_up = 0
	score_left = 0
	score_diagonal = 0

	for cols in range(len(seq1)+1):
		matrix[0][cols] = 0
	for rows in range(len(seq2)+1):
		matrix[rows][0] = 0

	for i in range(1, len(seq1)+1):
		for j in range(1, len(seq2)+1):
			score_up = matrix[j-1][i] + scoring['gap']
			score_left = matrix[j][i-1] + scoring['gap']
			score_diagonal = matrix[j-1][i-1] + scoringmatch(seq1[i-1], seq2[j-1])
			scores = [score_up, score_left, score_diagonal, 0]
			path = ['up', 'left', 'diag', 'stop']
			matrix[j][i] = max(scores)
			for k in range(len(scores)):
				if scores[k] == max(scores):
					traceback[j][i] = path[k]
	for i in range(len(matrix)):
		print(matrix[i])
	for i in range(len(traceback)):
		print(traceback[i])
	align1 = ''
	align2 = ''
	start = 0
	startposition = (0,0)
	for i in range(len(seq1)+1):
		for j in range(len(seq2)+1):
			if matrix[j][i] > start:
				start = matrix[j][i]
				startposition = (j,i)
	I = startposition[1]
	J = startposition[0]	
	while traceback[J][I] != 'stop':
		if traceback[J][I] == 'up':
			align1 += '-'
			align2 += seq2[J-1]
			J -= 1
		elif traceback[J][I] == 'left':
			align1 += seq1[I-1]
			align2 += '-'
			I -= 1
		elif traceback[J][I] == 'diag':
			align1 += seq1[I-1]
			align2 += seq2[J-1]
			I -= 1
			J -= 1
	align1 = align1[::-1]
	align2 = align2[::-1]
	return align1, align2

align1,align2 = smw(seq1,seq2,matrix,traceback)
print(align1+'\n'+align2)


