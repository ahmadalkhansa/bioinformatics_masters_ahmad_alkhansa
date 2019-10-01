import sys
import numpy as np
import os
import math
'''
The problem is to figure out how to build a matrix from a profile and secondary structure plus sequence we will see later what we can do
what is done:
	*the files that are needed to open arespecified
what is needed to be done:
	*find a way to read two files at the same time synchronuously
'''
def trainer(merger, random_list):
	l = merger.read().splitlines()
	q = random_list.read().splitlines()
	residue = ['', 'K', 'V', 'S', 'H', 'R', 'T', 'E', 'P', 'G', 'L', 'Q', 'D', 'N', 'M', 'A', 'I', 'C', 'Y', 'F', 'W']
	window_H = []
	window_E = []
	window_C = []
	window_R = []
	total = [['H',0],['E',0],['C',0]]
	data = []
	data_ss = []
	for i in range(-8,9):
		window_H.append(['res_H '+str(i)])
		window_H[i+8].extend([0 for j in range(20)])
		window_E.append(['res_E '+str(i)])
		window_E[i+8].extend([0 for j in range(20)])
		window_C.append(['res_C '+str(i)])
		window_C[i+8].extend([0 for j in range(20)])
		window_R.append(['res_R '+str(i)])
		window_R[i+8].extend([0 for j in range(20)])
	
	for n in l:
		for z in q:
			if n[0] == '>' and z == n:
				d = n.split(".")
				if len(d) == 2:
					if d[0][1:]+","+d[1]+",pssm,profile.npy" in os.listdir(sys.argv[3]):
						profile = np.load(sys.argv[3]+d[0][1:]+","+d[1]+",pssm,profile.npy")
					else: continue
				else:
					if d[0][1:]+",pssm,profile.npy" in os.listdir(sys.argv[3]):
						profile = np.load(sys.argv[3]+d[0][1:]+",pssm,profile.npy")
					else: continue
				r = l.index(n)+2
				rr = l[r]
				s = l.index(n)+1
				ss = l[s]	
				for m in range(len(rr)):
					if ss[m] == 'H' and rr[m] != 'X':
						for k in range(m-8, m+9):
							if k >= 0 and k < len(rr) and rr[k] != 'X':
								window_H[k-(m-8)][residue.index(rr[k])] += float(profile[k-(m-8)+1][list(profile[0]).index(rr[k])])
								total[0][1] += 1
								window_R[k-(m-8)][residue.index(rr[k])] += float(profile[k-(m-8)+1][list(profile[0]).index(rr[k])])
							else: continue
	
					elif ss[m] == 'E' and rr[m] != 'X':
						for k in range(m-8, m+9):
							if k >= 0 and k < len(rr) and rr[k] != 'X':
								window_E[k-(m-8)][residue.index(rr[k])] += float(profile[k-(m-8)+1][list(profile[0]).index(rr[k])])
								total[1][1] += 1
								window_R[k-(m-8)][residue.index(rr[k])] += float(profile[k-(m-8)+1][list(profile[0]).index(rr[k])])
							else: continue
	
					elif ss[m] == '-' and rr[m] != 'X':
						for k in range(m-8, m+9):
							if k >= 0 and k < len(rr) and rr[k] != 'X' :
								window_C[k-(m-8)][residue.index(rr[k])] += float(profile[k-(m-8)+1][list(profile[0]).index(rr[k])])
								total[2][1] += 1
								window_R[k-(m-8)][residue.index(rr[k])] += float(profile[k-(m-8)+1][list(profile[0]).index(rr[k])])
							else: continue
					else: continue
			else: continue

	t = total[0][1] + total[1][1] + total[2][1]

	total_mod = [['H',0],['E',0],['C',0]]
	for f in range(len(total)):
		total_mod[f][1]= float(total[f][1])/float(t)

	window_H_mod = []
	window_E_mod = []
	window_C_mod = []
	window_R_mod = []

	for i in range(len(window_H)):
		window_H_mod.append(window_H[i])
		window_E_mod.append(window_E[i])
		window_C_mod.append(window_C[i])
		window_R_mod.append(window_R[i])

	for k in range(len(window_H)):
		for j in range(1,len(window_H[k])):
			window_H_mod[k][j] = float(window_H[k][j])/t
			try:
				p = window_H_mod[k][j]
				window_H_mod[k][j] = math.log10(float(p)/float(total_mod[0][1]))
				window_E_mod[k][j] = float(window_E[k][j])/t
				p = window_E_mod[k][j]
				window_E_mod[k][j] = math.log10(float(p)/float(total_mod[1][1]))
				window_C_mod[k][j] = float(window_C[k][j])/t
				p = window_C_mod[k][j]
				window_C_mod[k][j] = math.log10(float(p)/float(total_mod[2][1]))
				window_R_mod[k][j] = float(window_R[k][j])/t
			except ValueError:
				continue

	for k in range(len(window_H)):
		for j in range(1,len(window_H[k])):
			p = window_H_mod[k][j]
			window_H_mod[k][j] = float(p)/float(window_R[k][j])
			p = window_E_mod[k][j]
			window_E_mod[k][j] = float(p)/float(window_R[k][j])
			p = window_C_mod[k][j]
			window_C_mod[k][j] = float(p)/float(window_R[k][j])

	data.append(residue)
	data.extend(window_H_mod)
	data.extend(window_E_mod)
	data.extend(window_C_mod)
	data.extend(window_R_mod)
#	data_ss.append(total_mod)

	check = np.save("training_set_"+sys.argv[4], data)
#	hell = np.save("total_ss_training_"+sys.argv[4], data_ss)
	return(check)

if __name__ == "__main__":
	merger = open(sys.argv[1], "r")
	random_list = open(sys.argv[2], "r")
	print(trainer(merger, random_list))
