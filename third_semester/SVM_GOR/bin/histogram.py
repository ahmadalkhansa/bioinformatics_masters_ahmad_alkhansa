import matplotlib.pyplot as plt
from eval_gor_svm_prj_last.bin.modules.paths import Path
from eval_gor_svm_prj_last.bin.modules.idmanager import Idmanager
import os
import numpy as np

def data_preparator():
	residues = ["A", "R", "N", "D", "C", "Q", "E", "G", "H", "I", "L", "K", "M", "F", "P", "S", "T", "W", \
				"Y", "V"]
	residue_info = {}
	ss_list = ["H", "E", "-", "t"]
	t_s = [0, 0, 0, 0]
	for r in residues:
		residue_info[r] = {"H": 0, "E": 0, "-": 0, "t": 0}
	profile_dir = os.listdir(Path.blind_profile_selected_dir)
	for profile in profile_dir:
		train_file = open(Path.blind_ss_sel_dir + Idmanager(profile).id() + ".dssp").read().splitlines()
		ss_seq = train_file[2]
		fasta_seq = train_file[1]
		for ss in range(len(ss_seq)):
			try:
				residue_info[fasta_seq[ss]][ss_seq[ss]] += 1
				residue_info[fasta_seq[ss]]["t"] += 1
				t_s[ss_list.index(ss_seq[ss])] += 1
				t_s[3] += 1
			except:
				residue_info["C"][ss_seq[ss]] += 1
				residue_info["C"]["t"] += 1
				t_s[ss_list.index(ss_seq[ss])] += 1
				t_s[3] += 1
	# prediction_file = open(
	# 	Path.svm_dir + "test1/predicted_files/thunder_trans_pred_2.0_0.5.fasta_ss").read().splitlines()
	# for ss_seq in range(2, len(prediction_file), 3):
	# 	for ss in range(len(prediction_file[ss_seq])):
	# 		try:
	# 			residue_info[prediction_file[ss_seq-1][ss]][prediction_file[ss_seq][ss]] += 1
	# 			residue_info[prediction_file[ss_seq - 1][ss]]["t"] += 1
	# 			t_s[ss_list.index(prediction_file[ss_seq][ss])] += 1
	# 			t_s[3] += 1
	# 		except:
	# 			residue_info["C"][prediction_file[ss_seq][ss]] += 1
	# 			residue_info["C"]["t"] += 1
	# 			t_s[ss_list.index(prediction_file[ss_seq][ss])] += 1
	# 			t_s[3] += 1
	for key in residue_info.keys():
		for inkey in residue_info[key].keys():
				residue_info[key][inkey] = round((residue_info[key][inkey]/(t_s[ss_list.index(inkey)]))*100, 2)
	return(residue_info)

def histogram(residue_info):

	residues = ["A", "R", "N", "D", "C", "Q", "E", "G", "H", "I", "L", "K", "M", "F", "P", "S", "T", "W", \
				"Y", "V"]
	ss_str=["Helix", "Strand", "Coil", "Overall"]
	data = [[0 for i in range(len(residues))] for j in range(4)]
	for item in range(len(list(residue_info['A'].items()))):
		for key in range(len(list(residue_info.keys()))):
			data[item][key] = residue_info[list(residue_info.keys())[key]][list(residue_info['A'].items())[item][0]]
#			data[item].append(list(residue_info[key])[item][1])
#	print(data)
#	values = np.array(data)
	colors=["blue", "orange", "green", "red"]
	number_groups = 4
	bin_width = 1.0 / (number_groups+1)
	fig, ax = plt.subplots(figsize=(6,6))
	for i in range(len(residues)):
		for j in range(4):
			ax.bar(x=np.arange(len(residues))+0.1+float(j+j)*(bin_width*0.5), height=data[j], width=bin_width, color=colors[j], align='center')

	ax.set_xticks(np.arange(len(residues)) + number_groups / (2 * (number_groups + 1)))
	plt.rcParams.update({'font.size': 22})
	ax.set_xticklabels(residues)
	ax.tick_params(axis='both', which='major', labelsize=22)
	ax.legend(ss_str, facecolor='w')
	ax.set_title("Blind original")
	plt.xlabel("Residues", fontsize=22)
	plt.ylabel("Frequency %", fontsize=22)
	plt.show()

if __name__=="__main__":
	data = data_preparator()
	histogram(data)
