T = {'Y':{'Y':0.7, 'N':0.2, 'End':0.1},\
'N':{'Y':0.1, 'N':0.8, 'End':0.1},\
'Begin':{'Y':0.2, 'N':0.8}}

#emission:
E = {'Y':{'A':0.1, 'C':0.4, 'G':0.4, 'T':0.1},\
'N':{'A':0.25, 'C':0.25, 'G':0.25, 'T':0.25}}

#sequence:
seq = 'ATGCG'

#states:
states = ['Y','N']

def bck(seq, T, E, states):
	matrix = [[0 for i in range(len(seq))]for j in range(len(states))]
	for i in range(len(states)):
		matrix[i][len(seq)-1] = T[states[i]]['End']
	for i in range(len(seq)-1, 0, -1):
		for j in range(len(states)):
			for k in range(len(states)):
				matrix[j][i-1] += matrix[k][i] * T[states[j]][states[k]] * E[states[k]][seq[i]]
	Begin = []
	for i in range(len(states)):
		Beginscores = matrix[i][0] * T['Begin'][states[i]] * E[states[i]][seq[0]]
		Begin.append(Beginscores)
		Beginscore = sum(Begin)
	print(Beginscore)
	for i in range(len(states)):
		print(matrix[i])
	return('')
print(bck(seq, T, E, states))
