## transition probabilities
## MEMO: from ... to..
transition = {  'B':{'Y':0.2, 'N':0.8},
                'Y':{'Y':0.7, 'N':0.2, 'E':0.1}, 
                'N':{'N':0.8, 'Y':0.1, 'E':0.1}}

## emission probabilitlies 
emission = {    'Y':{'A':0.1, 'C':0.4, 'G':0.4, 'T':0.1},
                'N':{'A':0.25, 'C':0.25, 'G':0.25, 'T':0.25}} 

seq = 'ATGCG'

## The order is meaningful
states = ['B', 'Y', 'N', 'E']

def pretty_matrix(m):
    for i in m:
        print(i)

def sum_overStates(scores):
    sum_score = 0.0
    for i in range(len(scores)):
        sum_score += scores[i]
       
    return(sum_score)

## Backward computations
def backward(seq, transition, emission, states):
    n = len(seq) + 2 #number of columns of B
    m = len(states) #number of rows of B
    
    ## Initialization
    B = [[0 for col in range(n)] for row in range(m)]    
    
     ## Transition from end state to termination one
    for i in range(1, m-1):
        B[i][n-2] = transition[states[i]]['E']
    #print(B)

    ## Iteration
    for j in range(n-2, 1, -1):
        for i in range(1, m-1): 
            scores = []           
            for state in range(1, m-1):
                score = B[state][j] * transition[states[i]][states[state]] * emission[states[state]][seq[j-1]] 
                scores.append(score)
                            
            B[i][j-1] = sum_overStates(scores)
                
    ## Termination
    final_score = []
    for k in range(1, m-1):
        final_score.append(B[k][1] * transition['B'][states[k]] * emission[states[k]][seq[0]])
    
    B[0][0] = sum_overStates(final_score)  
    print('The p = (sequence | model) is: %f' %B[0][0])    
    
    return(B)


B = backward(seq, transition, emission, states)
print()
pretty_matrix(B)
print()


