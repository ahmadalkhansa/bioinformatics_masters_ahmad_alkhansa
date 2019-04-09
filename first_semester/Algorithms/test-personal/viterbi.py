seq = 'ACTGTC'

T = {'Y':{'Y':0.7, 'N':0.2, 'End':0.1},\
'N':{'Y':0.1, 'N':0.8, 'End':0.1},\
'Begin':{'Y':0.2, 'N': 0.8}}

E = {'Y':{'A':0.1, 'G':0.4, 'C':0.4, 'T':0.1},\
'N':{'A':0.25, 'G':0.25, 'C':0.25, 'T':0.1}}

states = ['Y', 'N']

def viterbi(seq, T, E, states):
	traceback = []
	matrix = [[0 for i in range(len(seq))]for j in range(len(states))]
	for i in range(len(states)):
		Begin = []
		matrix[i][0] = T['Begin'][states[i]] * E[states[i]][seq[0]]
		Begin.append(matrix[i][0])
	if matrix[i][0] == max(Begin):
		traceback.append(states[i])



	for i in range(1, len(seq)):
		for j in range(len(states)):
			scores = []
			for k in range(len(states)):
				score = matrix[k][i-1] * T[states[k]][states[j]] * E[states[j]][seq[i]]
				scores.append(score)
			if score == max(scores):
				matrix[j][i] = score
				traceback.append(states[j])
	
	for z in range(len(states)):
		endscore = 0
		endlist = []
		endscores = matrix[z][len(seq)-1] * T[states[z]]['End']
		endlist.append(endscores)
	if endscores == max(endlist):
		endscore = max(endlist)
		traceback.append(states[z]+'E')
	for i in range(len(states)):
		print(matrix[i])
	print(traceback)
	return(endscore)
print(viterbi(seq, T, E, states))
