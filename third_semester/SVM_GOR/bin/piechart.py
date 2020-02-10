import matplotlib.pyplot as plt
from eval_gor_svm_prj_last.bin.modules.paths import Path
from eval_gor_svm_prj_last.bin.modules.idmanager import Idmanager
import os
import numpy as np

def data_preparator():
	helix = 0
	coil = 0
	strand = 0
	# prediction_file = open(Path.blind_svm_dir+"predicted_files/thunder_trans_pred_2.0_0.5.fasta_ss").read().splitlines()
	# for ss_seq in range(2, len(prediction_file), 3):
	# 	for ss in prediction_file[ss_seq]:
	# profile_dir = os.listdir(Path.profile_dir)
	# for profile in profile_dir:
	# Gor_blind= os.listdir(Path.blind_gor_dir+"predicted_files/")
	for profile in os.listdir(Path.blind_profile_selected_dir):
		ss_seq = open(Path.blind_ss_sel_dir+Idmanager(profile).id()+".dssp").read().splitlines()[2]
		#ss_seq = open(Path.blind_gor_dir+"predicted_files/"+something).read().splitlines()[2]
		for ss in ss_seq:
			if ss == "H":
				helix += 1
			elif ss == "E":
				strand += 1
			elif ss == "-":
				coil += 1
	perc_helix = helix/(helix+strand+coil)
	perc_strand = strand/(helix+strand+coil)
	perc_coil = coil/(helix+strand+coil)
	return(perc_helix, perc_strand, perc_coil)

def piechart(perc_helix, perc_strand, perc_coil):
	dist = [perc_helix*100, perc_strand*100, perc_coil*100]
	labeling = ["Helix "+str(round(perc_helix*100))+"%", "Strand "+str(round(perc_strand*100))+"%", "Coil "+str(round(perc_coil*100))+"%"]
	# fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(aspect="equal"))
	fig, ax = plt.subplots(subplot_kw=dict(aspect="equal"))

	wedges, texts = ax.pie(dist, wedgeprops=dict(width=0.3), startangle=45)

	# bbox_props = dict(boxstyle="square,pad=0.3", fc="w", ec="k", lw=0.72)
	kw = dict(arrowprops=dict(arrowstyle="-"), zorder=0, va="center", size="xx-large")

	for i, p in enumerate(wedges):
		ang = (p.theta2 - p.theta1) / 2. + p.theta1
		y = np.sin(np.deg2rad(ang))
		x = np.cos(np.deg2rad(ang))
		horizontalalignment = {-1: "right", 1: "left"}[int(np.sign(x))]
		connectionstyle = "angle,angleA=0,angleB={}".format(ang)
		kw["arrowprops"].update({"connectionstyle": connectionstyle})
		# ax.annotate(labeling[i], xy=(x, y), xytext=(1.35 * np.sign(x), 1.4 * y),
		# 			horizontalalignment=horizontalalignment, **kw)
		ax.annotate(labeling[i], xy=(x, y), xytext=(1.2 * np.sign(x), 1 * y),
					horizontalalignment=horizontalalignment, **kw)


	plt.rcParams.update({'font.size': 22})
	ax.set_title("Blind SS")

	plt.show()

	# plt.pie(dist, radius=1, labels=labeling, wedgeprops=dict(width=0.32, edgecolor="w"), startangle=90, arrowstyle="-")
	# plt.show()


if __name__=="__main__":

	h, s, c = data_preparator()
	print(h, s, c)
	piechart(h, s, c)
