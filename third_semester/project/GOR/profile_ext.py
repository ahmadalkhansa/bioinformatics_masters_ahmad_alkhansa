import sys
import pandas as pd
import numpy as np

def profiling(f1):
#open file and split lines to elements in list
	l = f1.read().splitlines()
#output file
	output_name = ""
# this will be the dataframe
	profile =[]
#look at the second line
	n = l[2].split()
	k = [" "]
#extend a list of space element first and residues in the rest
	k.extend(n[20:42])
#append the list to the grand list for construction of the data frame
	profile.append(k)
#iterate through the rest of the file
	for i in range(3,len(l)):
#if there isn't an empty line (the empty line comes directly after the profile in the main file)
		if l[i] != "":
#parse though the lines
			m = l[i].split()
#type the sequence in list of the line
			q = [m[1]]
#and the frequencies as remaining elements of each list corresponding to each line
			for i in m[22:42]:
				q.append(int(i)/100)
#append the lists(corresponding to each line) to the grand list
			profile.append(q)
		else: break

#build an array	

#give a file name and apply the function of formatting the whole profile in csv format where each two columns are separated by a tab
	for g in sys.argv[1].split("."):
		if "/" in g:
			output_name += g[g.index("/")+1:]
			output_name += ","
		elif g != "fasta":
			output_name += g
			output_name += ","
		else: continue
	output_name += "profile.npy"

	np.save(sys.argv[2]+output_name, profile)

	return(output_name+" done successfully")

if __name__ == "__main__":
	f1 = open(sys.argv[1], "r")
	print(profiling(f1))
