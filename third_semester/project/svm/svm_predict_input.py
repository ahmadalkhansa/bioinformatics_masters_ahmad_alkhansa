import sys
import os
import numpy as np

'''
very similar to the previous script
'''


def vec_extractor(merged_file):
	l = merged_file.read().splitlines()
	output_file = open(sys.argv[3]+"svm_pred_prep.txt", "a+")
	residue = ['K', 'V', 'S', 'H', 'R', 'T', 'E', 'P', 'G', 'L', 'Q', 'D', 'N', 'M', 'A', 'I', 'C', 'Y', 'F', 'W']
	assigned_coefficient = []
	for f in range(20):
		assigned_coefficient.append(str(f))
	structures = ['','H','E','C']
	sec = {}
	for i in range(1,len(structures)):
		sec[i] = {}
		for j in range(1,341):
			sec[i][j] = 0

	for n in l:
		if n[0] == ">":
			rr = l[l.index(n)+2]
			ss = l[l.index(n)+1]

			try:
				t = np.load(sys.argv[2]+n[1:].split(".")[0].upper()+","+n[1:].split(".")[1]+",pssm,profile.npy")
				np.load(sys.argv[2]+n[1:].split(".")[0].upper()+","+n[1:].split(".")[1]+",pssm,profile.npy")
				try:
					for x in range(1,len(t)):
						if t[x][0] == rr[x-1]:
							if ss[x-1] == 'H':
								for k in range(x-8,x+9):
									if k > 0 and k < len(t) and t[k][0] != 'X' and rr[x-1] != 'X':
										struc_label = structures.index(ss[x-1])
										window_positions = k-x+9+17*(float(assigned_coefficient[residue.index(rr[x-1])]))
										frequency = float(t[k][list(t[0]).index(t[k][0])])
										sec[struc_label][window_positions] =+ frequency
									else: continue

								sec_list = ['1']
								for key, value in sec[1].items():
									if float(sec[1][key]) != float('0'):
										temp = [str(key)+":"+str(value)]
										sec_list.extend(temp)
										sec[1][key] = 0

								if len(sec_list) > 1:
									output_file.write(' '.join(sec_list)+'\n')
							elif ss[x-1] == 'E':
								for k in range(x-8,x+9):
									if k > 0 and k < len(t) and t[k][0] != 'X' and rr[x-1] != 'X':
										struc_label = structures.index(ss[x-1])
										window_positions = k-x+9+17*(float(assigned_coefficient[residue.index(rr[x-1])]))
										frequency = float(t[k][list(t[0]).index(t[k][0])])
										sec[struc_label][window_positions] =+ frequency
									else: continue
	
								sec_list = ['2']
								for key, value in sec[2].items():
									if float(sec[2][key]) != float('0'):
										temp = [str(key)+":"+str(value)]
										sec_list.extend(temp)
										sec[2][key] = 0
								if len(sec_list) > 1:
									output_file.write(' '.join(sec_list)+'\n')

							elif ss[x-1] == 'C':
								for k in range(x-8,x+9):
									if k > 0 and k < len(t) and t[k][0] != 'X' and rr[x-1] != 'X':
										struc_label = structures.index(ss[x-1])
										window_positions = k-x+9+17*(float(assigned_coefficient[residue.index(rr[x-1])]))
										frequency = float(t[k][list(t[0]).index(t[k][0])])
										sec_list = []
										sec[struc_label][window_positions] =+ frequency
									else: continue
							
								sec_list = ['3']
								for key, value in sec[3].items():
									if float(sec[3][key]) != float('0'):
										temp = [str(key)+":"+str(value)]
										sec_list.extend(temp)
										sec[3][key] = 0
	

								if len(sec_list) > 1:
									output_file.write(' '.join(sec_list)+'\n')
							else: continue
					
				except IndexError:
					print(n[1:])
					continue
									
			except IOError:
					continue
	return(output_file.close())


if __name__ == "__main__":
	grand_file = open(sys.argv[1], "r")
	vec_extractor(grand_file)
