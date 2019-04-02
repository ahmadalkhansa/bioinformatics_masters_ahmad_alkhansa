seq1 = 'ACTGCGCTGACCC'
seq2 = 'ATGGGCGATTA'

matrix = [[0 for i in range(len(seq1)+1)] for j in range(len(seq2)+1)]

scores = {'match': 3, 'mismatch': 0, 'gap': -2}

def scoring(nuc1, nuc2):
	score = 0
	if nuc1 == nuc2:
		score = scores['match']
	elif '-' == nuc1 or '-' == nuc2:
		score = scores['gap']
	else:
		score = scores['mismatch']
	return(score)

def NW(seq1, seq2, matrix, scoring, scores):
	for i in range(len(seq1)+1):
		matrix[0][i] == scores['gap']* i
	for i in range(len(seq2)+1):
		matrix[i][0] == scores['gap']* i
	for i in range(1, len(seq2)+1):
		for j in range(1, len(seq1)+1):
			diag = matrix[i-1][j-1] + scoring(seq2[i-1], seq1[j-1])
			gap1 = matrix[i-1][j] + scores['gap']
			gap2 = matrix[i][j-1] + scores['gap']
			matrix[i][j] = max(diag, gap1, gap2)
	I = len(seq2)
	J = len(seq1)
	align1 = ''
	align2 = ''
	while I > 0 and J > 0:
		current = matrix[I][J]
		diagonal = matrix[I-1][J-1]
		up = matrix[I-1][J]
		left = matrix[I][J-1]
		if current == diagonal + scoring(seq2[I-1], seq1[J-1]):
			align1 += seq1[J-1]
			align2 += seq2[I-1]
			I -= 1
			J -= 1
		elif current == up + scores['gap']:
			align1 += '-'
			align2 += seq2[I-1]
			I -= 1
		elif current == left + scores['gap']:
			align1 += seq1[J-1]
			align2 += '-'
			J -= 1
	
	while I > 0:
		align1 += '-'
		align2 += seq2[I-1]
		I -= 1
	while J > 0:
		align1 += seq1[J-1]
		align2 += '-'
		J -= 1
	return(align1, align2)
align1, align2 = NW(seq1, seq2, matrix, scoring, scores)
for i in range(len(seq2)+1):
	print(matrix[i])
print(align1+'\n'+align2)
