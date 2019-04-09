
T = {'Y':{'Y':0.7, 'N':0.2, 'End':0.1},\
'N':{'Y':0.1, 'N':0.8, 'End':0.1},\
'Begin':{'Y':0.2, 'N':0.8}}

E = {'Y':{'A':0.1, 'C':0.4, 'G':0.4, 'T':0.1},\
'N':{'A':0.25, 'C':0.25, 'G':0.25, 'T':0.25}}

seq = 'ATGCCG'
states = ['Y','N']


def frw(seq, T, E):
	end = 0
	matrix = [[0 for i in range(len(seq))] for j in range(len(states))]
	for l in range(len(states)):
		matrix[l][0] = T['Begin'][states[l]] * E[states[l]][seq[0]]
	for i in range(1, len(seq)):
		for k in range(len(states)):
			score_list = []
			for s in range(len(states)):
				score = matrix[s][i-1] * T[states[s]][states[k]]
				score_list.append(score)

			matrix[k][i] = sum(score_list) * E[states[k]][seq[i]]
	end_list = []
	for k in range(len(states)):
		end = matrix[k][len(seq)-1] * T[states[k]]['End']
		end_list.append(end)
	end = sum(end_list)

	for j in range(len(matrix)):
		print(matrix[j])

	return(end)
		
print(frw(seq, T, E))

