input_file = open('neuron_data-2.txt')

L1 = []; L2=[]

for line in input_file:
	columns = line.split()
	#print(columns)
	if columns[0] == '1':
		L1.append(float(columns[1]))
	else:
		L2.append(float(columns[1]))

print(L1,'\n', L2)

def average(l):

	average = sum(l) / len(l)
	return(average)

print(average(L1), '\n', average(L2))
	
def standard_dev(q):
	from math import sqrt
	s = 0
	average = sum(q) / len(q)
	for nums in q:
		s = s + nums
		stdev = sqrt((s - average)**2 / (len(q) - 1))
		return(stdev)

print(standard_dev(L1),'\n',standard_dev(L2))

        
