import pickle
import os
import sys
#from eval_gor_svm_prj.bin.idmanager import Idmanager
from modules.idmanager import Idmanager
#from eval_gor_svm_prj.bin.paths import Path
from modules.paths import Path

"""
The profile curator will extract and adjust the information from a pssm file to a proper profile with proper values.
In addition, it will get rid of profiles that don't contain information and print the ids. Moreover, if there is not a hit,
it will also write to a different file the id.
"""
#This function will add zeros according to the size window to the begining and the end of the profile.
#The addition will ensure an easy calculation of the propensities of the residues.

def add_extremes_zeros(profile, window_size: int):
	extreme = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
	for i in range(window_size // 2):
		profile.insert(0,extreme)
		profile.append(extreme)
	return(profile)

def profile_extractor(pssm, state):
	f1 = open(pssm, "r")
	# open file and split lines to elements in list
	l = f1.read().splitlines()
	# this will be the dataframe
	profile = []
	# iterate through the rest of the file
	for i in range(3, len(l)):
		# if there isn't an empty line (the empty line comes directly after the profile in the main file)
		if l[i] != "":
			# parse through the lines
			m = l[i].split()
			#create the list that will contain the values
			q = []
			# and the frequencies as remaining elements of each list corresponding to each line
			for i in m[22:42]:
				q.append(int(i) / 100)
			# append the lists(corresponding to each line) to the grand list
			profile.append(q)
		else:
			break


	#this function is a decision function to determine wether the file is going to be printed or not.
	#it will also manage the removing of the ids that had zero hits.
	def profile_manager(profile):
		profile_dest = Path.profile_dir
		if state == "blind":
			profile_dest = Path.blind_profile_dir
		elif state == "selected":
			profile_dest = Path.blind_profile_selected_dir
		elif state == "cv":
			pass
		input_file = pickle.load(open(Path.input_file, "rb"))
		sum_values = 0
		for j in range(len(profile)):
			for i in range(len(profile[j])):
				sum_values += profile[j][i]
		id = Idmanager(pssm)
		if sum_values != float(0):
			profile_z = add_extremes_zeros(profile, input_file['window_size'])
#			print(profile_z)
			with open(profile_dest+id.modify(".profile"), "wb") as profile_file:
				return(pickle.dump(profile_z, profile_file))
		else:
			if state == "blind" or state == "selected":
				pass
			elif state == "cv":
				with open(Path.results_dir + "cv_ids_novalues.txt", "a") as novalue:
					return (novalue.write(id.id() + "\n"))

	return(profile_manager(profile))


if __name__=="__main__":
	if sys.argv[1] == "blind":
		for pssm_files in os.listdir(Path.blind_pssm_dir):
			profile_extractor(Path.blind_pssm_dir + pssm_files, "blind")
	elif sys.argv[1] == "selected":
		for pssm_files in os.listdir(Path.blind_pssm_selected_dir):
			profile_extractor(Path.blind_pssm_selected_dir + pssm_files, "selected")
	elif sys.argv[1] == "cv":
		for pssm_files in os.listdir(Path.pssm_dir):
			profile_extractor(Path.pssm_dir+pssm_files, "cv")