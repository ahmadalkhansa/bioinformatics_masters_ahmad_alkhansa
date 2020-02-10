#from eval_gor_svm_prj.bin.modules.paths import Path
from modules.paths import Path
import os

def chain_extractor(nominated_id, dssp_file):
	helix = ['H', 'I', 'G']
	beta = ['E', 'B']
	coil = ['S', 'T', ' ']
	chain = nominated_id.split("_")[1]
	ss = ""
	fasta_sequence = ""
	flag = 0
	for lines in dssp_file:
		if "#" in lines:
			flag = 1
			continue
		elif flag == 0:
			continue
		if flag == 1:
			if lines[11] == chain and lines[16] in helix:
				fasta_sequence += lines[13]
				ss += 'H'
			elif lines[11] == chain and lines[16] in beta:
				fasta_sequence += lines[13]
				ss += 'E'
			elif lines[11] == chain and lines[16] in coil:
				fasta_sequence += lines[13]
				ss += '-'
	for ids in os.listdir(Path.blind_report_fasta_dir):
		if nominated_id == ids[0:6]:
			ss_file = open(Path.blind_ss_sel_dir+nominated_id+".dssp", "w+")
			fasta_file = open(Path.blind_fasta_sel_dir+nominated_id+".fasta", "w+")
			ss_file.write(">"+nominated_id+"\n"+fasta_sequence+"\n"+ss+"\n")
			fasta_file.write(">"+nominated_id+"\n"+fasta_sequence+"\n")
			ss_file.close()
			fasta_file.close()

if __name__ == "__main__":
	nominated_ids = open(Path.blind_nominated_chids, "r").read().splitlines()
	for dssp_id in os.listdir(Path.blind_dssp_dir):
		for nominated_id in nominated_ids:
			if dssp_id.split(".")[0] == nominated_id.split("_")[0]:
				dssp_file = open(Path.blind_dssp_dir+dssp_id, "r")
				chain_extractor(nominated_id, dssp_file)







