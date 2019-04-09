#let's try to build a matrix

seq1 = 'ATCG'
seq2 = 'TGCAA'

matrix = [[0 for cols in range(len(seq1) + 1)]for rows in range(len(seq2) + 1)]

#this is just for proper visualization
'''for rows in range(len(seq2)+1):
	print(matrix[rows])'''

scores = {'match': 3, 'mismatch': -1, 'gap': -2}

#scoring function

def scoring(nuc1, nuc2):
	score = 0
	if nuc1 == nuc2:
		score_match = scores['match']
		return score_match
	elif '-' == nuc1 or '-' == nuc2:
		score_penalty = scores['gap']
		return score_penalty
	else:
		score_mismatch = scores['mismatch']
		return score_mismatch

# first column and row = 0
def ndl(seq1, seq2):
	for cols in range(1, len(seq1) + 1):
		matrix[0][cols] = scores['gap'] + matrix[0][cols - 1]
	for rows in range(1, len(seq2) + 1):
		matrix[rows][0] = scores['gap'] + matrix[rows - 1][0]

#how core matrix works
	for cols in range(1, len(seq1) +1):
		for rows in range(1, len(seq2) +1):		
			match = matrix[rows - 1][cols - 1] + scoring(seq1[cols - 1], seq2[rows - 1])
			gap1 = matrix[rows][cols - 1] + scores['gap']
			gap2 = matrix[rows - 1][cols] + scores['gap']
			matrix[rows][cols] = max(match, gap1, gap2)
#let's do the trace back
	i = len(seq1)
	j = len(seq2)
	align1 = ''
	align2 = ''

	while i > 0 and j > 0:
		current = matrix[j][i]
		diagonal = matrix[j-1][i-1]
		up = matrix[j-1][i]
		left = matrix[j][i-1]

		if current == diagonal + scoring(seq1[i - 1], seq2[j - 1]):
			align1 += seq1[i-1]
			align2 += seq2[j-1]
			i -= 1
			j -= 1

		elif current == up + scores['gap']:
			align1 += '-'
			align2 += seq2[j-1]
			j -= 1

		elif current == left + scores['gap']:
			align1 += seq1[i-1]
			align2 += '-'
			i -= 1
		
	while i > 0:
		align1 += seq1[i-1]
		align2 += '-'
		i -= 1

	while j > 0:
		align1 += '-'
		align2 += seq2[j-1]
		j -= 1
	align1 = align1[::-1]
	align2 = align2[::-1]

	return(align1+'\n'+align2)

#align1, align2 = ndl(seq1, seq2)

for rows in range(len(seq2)+1):
	print(matrix[rows])
#print(align1+'\n'+align2)
print(ndl(seq1, seq2))

