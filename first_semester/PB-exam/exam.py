sequenceA = 'ACTG'
sequenceB = 'TGCC'

gap = -2

match = {'A':{'A':2, 'C':0, 'T':0, 'G':1}, \
'C':{'A':0, 'C':2, 'T':1, 'G':0}, \
'T':{'A':0, 'C':1, 'T':2, 'G':0}, \
'G':{'A':1, 'C':0, 'T':0, 'G':2}}

def score_match(nuc1, nuc2):
	return(match[nuc1][nuc2])

def ndl(sequenceA, sequenceB, gap, match, score_match):
	matrix = [[0 for i in range(len(sequenceA)+1)]for j in range(len(sequenceB)+1)]
	traceback = [['' for i in range(len(sequenceA)+1)]for j in range(len(sequenceB)+1)]

#filling first row and column of the two matrices:
	for i in range(len(sequenceA)+1):
		matrix[0][i] = gap * i
		traceback[0][i] = 'left'
	for j in range(len(sequenceB)+1):
		matrix[j][0] = gap * i
		traceback[j][0] = 'up'
#populating:
	for i in range(1, len(sequenceA) +1):
		for j in range(1, len(sequenceB) +1):		
			diag = matrix[j - 1][i - 1] + score_match(sequenceA[i - 1], sequenceB[j - 1])
			left = matrix[j][i - 1] + gap
			up = matrix[j - 1][i] + gap
			score_list = [diag, left, up]
			path = ['diagonal', 'left', 'up']
			for k in range(len(score_list)):
				if score_list[k] == max(score_list):
					matrix[j][i] = score_list[k]
					traceback[j][i] = path[k]
	for i in range(len(sequenceB)+1):
		print(matrix[i])
	for i in range(len(sequenceB)+1):
		print(traceback[i])
#traceback for alignment:
	I = len(sequenceA)
	J = len(sequenceB)
	align1 = ''
	align2 = ''
	while I > 0 and J > 0:
		if matrix[J][I] == matrix[J-1][I-1] + score_match(sequenceA[I-1], sequenceB[J-1]):
			align1 += sequenceA[I-1]
			align2 += sequenceB[J-1]
			I -= 1
			J -= 1
		elif matrix[J][I] == matrix[J][I-1] + gap:
			align1 += sequenceA[I-1]
			align2 += '-'
			I -= 1
		elif matrix[J][I] == matrix[J-1][I] + gap:
			align1 += '-'
			align2 += sequenceB[J-1]
			J -= 1
	
	while I > 0:
		align1 += sequenceA[I-1]
		align2 += '-'
		I -= 1
	while J > 0:
		align1 += '-'
		align2 += sequenceB[J-1]
		J -= 1

#pretty matrix
#	for i in range(len(sequenceB)+1):
#		print(matrix[i])
#	for i in range(len(sequenceB)+1):
#		print(traceback[i])
	return(align1[::-1]+'\n'+align2[::-1])

print(ndl(sequenceA, sequenceB, gap, match, score_match))
	
