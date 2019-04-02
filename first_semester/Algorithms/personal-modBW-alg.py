#Transition:
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


def BWD(seq, T, E):
	#matrix:
	matrix = [[0 for i in range(len(seq))] for j in range(len(states))]

	#transition from last position to the end:
	for l in range(len(states)):
		matrix[l][len(seq)-1] = T[states[l]]['End']

	#populating the matrix:
	#moving backward throught the sequence and between states:
	for i in range(len(seq)-1, 0, -1): # not 0 but -1
		for k in range(len(states)):
			#introduce a scoring list:
			#score_list = []
			#calculate the score of by multiplying the current score by the transition from the current state to any of the other state and by the emmision of the residue before:
			for s in range(len(states)):
				matrix[k][i-1] += matrix[s][i] * T[states[k]][states[s]] * E[states[s]][seq[i]]
				#append scores of each states at the current position to a list
				#score_list.append(score)
			#sum the elements in the list and introduce it as the score in the position before the current:
			#matrix[k][i-1] = sum(score_list) 
	#introduce a list:
	begin_list = []
	#
	for k in range(len(states)):
		begin = matrix[k][0] * T['Begin'][states[k]] * E[states[k]][seq[0]]
		begin_list.append(begin)
	begin = sum(begin_list)
	
	print(begin)

	for j in range(len(matrix)):
		print(matrix[j])
	return('')
print(BWD(seq, T, E))

