#Dictionary for Transitions:
T = {'Y':{'Y':0.7, 'N':0.2, 'End':0.1},\
'N':{'Y':0.1, 'N':0.8, 'End':0.1},\
'Begin':{'Y':0.2, 'N': 0.8}}

#Dictionary for emmisions:
E = {'Y':{'A':0.1, 'G':0.4, 'C':0.4, 'T':0.1},\
'N':{'A':0.25, 'G':0.25, 'C':0.25, 'T':0.1}}

#sequence:
seq = 'ACTGTC'

#states:
states = ['Y', 'N']

#A function for detecting the max:
def find_max(scores, states):
	max_score = float('-inf')
	max_state = None
	for i in range(len(scores)):
		if scores[i] > max_score:
			max_score = scores[i]
			max_state = states[i]
	return(max_score, max_state)

#The viterbi function:
def viterbi(seq, T, E, states):
#	The matrix is of columns with the sequence length and rows of number of states:
	matrix = [[0 for i in range(len(seq))]for j in range(len(states))]
#	traceback is a list that needs to be filled by the states with the highest probability:
	traceback = []
#	Filling the first column in the matrix and the first element in the traceback:
	for l in range(len(states)):
		matrix[l][0] = T['Begin'][states[l]] * E[states[l]][seq[0]]
		Begin = [matrix[l][0]]
	if matrix[l][0] == max(Begin):
		traceback.append(states[l])
#	filling the rest of the matrix
	for i in range(1, len(seq)): #scanning in the columns
		for p in range(len(states)): #scanning in the rows
			scores = []
			for o in range(len(states)): #scanning in the rows of previous columns
				score = matrix[o][i-1] * T[states[o]][states[p]]
				scores.append(score) #making a list of scores without emmision
			max_score, max_state = find_max(scores, states) #choosing the highest value of a state
			matrix[p][i] = max_score * E[states[p]][seq[i]] #after choosing multiply by the emmision
		traceback.append(max_state) #append the state that gave the score
	for z in range(len(states)): # for the End scan the best score, append the best state and show the end score
		final_score = [matrix[z][len(seq)-1] * T[states[z]]['End']]
	if (matrix[z][len(seq)-1] * T[states[z]]['End']) == max(final_score):
		traceback.append(states[z]+'E') 
	for u in range(len(matrix)):
		print(matrix[u])
	print(traceback)
	return(final_score)
print(viterbi(seq, T, E, states))
