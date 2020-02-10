import matplotlib.pyplot as plt
from eval_gor_svm_prj_last.bin.modules.paths import Path
from eval_gor_svm_prj_last.bin.modules.idmanager import Idmanager
import os
import numpy as np

def data_preparator():
	data = [0,0,0,0,0,0,0]
	cla = ['a','b','c','d','e','g','o']
	total = 0
	scop_file = open("../data/dir.cla.scope.2.06-stable.txt").read().splitlines()
	for line in range(4,len(scop_file)):
#		print(scop_file[line].split()[3][0])
		try:
			data[cla.index(scop_file[line].split()[3][0])] += 1
			total += 1
		except:
			data[6] += 1
			total += 1

	for d in range(len(data)):
		data[d] = round(100*data[d]/total)
	return(data)

def piechart(data):
	dist = data
	labeling = ["All alpha "+str(data[0])+"%", "All beta "+str(data[1])+"%", "Alpha / Beta "+str(data[2])+"%", \
				"Alpha + Beta "+str(data[3])+"%", "Multi-domain proteins "+str(data[4])+"%", "Small Protiens "+str(data[5])+"%", \
				"Others "+ str(data[6])+"%"]
	fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(aspect="equal"))

	wedges, texts = ax.pie(dist, wedgeprops=dict(width=0.99), startangle=45, explode=(0.01,0.01,0.01,0.01,0.01,0.01,0.01))

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
	ax.set_title("SCOP classes 2016")

	plt.show()



if __name__=="__main__":
	data = data_preparator()
	piechart(data)
