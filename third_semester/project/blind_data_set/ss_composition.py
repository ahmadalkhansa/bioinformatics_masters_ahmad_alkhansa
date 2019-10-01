import sys
import matplotlib.pyplot as plt
import numpy as np
import pprint
#def autolabel(rects):
#   """Attach a text label above each bar in *rects*, displaying its height."""
#	for rect in rects:
#		height = rect.get_height()
#		ax.annotate('{}'.format(height), xy=(rect.get_x() + rect.get_width() / 2, height), xytext=(0, 3), textcoords="offset points", ha='center', va='bottom') # 3 points vertical offset

def count(ff):
	residue = {}
	total = {"H": 0, "-": 0, "E": 0, "#": 0}
	l = ff.read().splitlines()
	for n in l:
		if n[0] == ">":
			r = l.index(n)+2
			rr = l[r]
			s = l.index(n)+1
			ss = l[s]
			for p in rr:
				snr=ss[rr.index(p)]
				if p not in residue.keys():
					residue[str(p)] = {"H": 0, "-": 0, "E": 0, "#": 0}
					residue[str(p)][str(snr)] += 1
					residue[str(p)]["#"] += 1
					total[str(snr)] += 1
					total["#"] += 1
				else:
					residue[str(p)][str(snr)] += 1
					residue[str(p)]["#"] += 1
					total[str(snr)] += 1
					total["#"] += 1
		else:
			continue
#	print(total)
	return(residue, total)

def ratio(residue, total):
	ss_r = {}
	for r in residue:
		ss_r[str(r)] = residue[str(r)]
		ss_r[str(r)]["H"] = round(float(residue[str(r)]["H"])/total["H"], 2)*100
		ss_r[str(r)]["-"] = round(float(residue[str(r)]["-"])/total["-"], 2)*100
		ss_r[str(r)]["E"] = round(float(residue[str(r)]["E"])/total["E"], 2)*100
		ss_r[str(r)]["#"] = round(float(residue[str(r)]["#"])/total["#"], 2)*100
	return(ss_r)
	#Drawing the plot

def pie(ratio):

	label = []
	parts = []
	prelabel = ratio.keys()
	for i in prelabel:
		label.append(str(i)+"_Helix")
		parts.append(ratio[str(i)]["H"])
		label.append(str(i)+"_Strand")
		parts.append(ratio[str(i)]["E"])
		label.append(str(i)+"_Coil")
		parts.append(ratio[str(i)]["-"])


	fig, ax = plt.subplots(figsize=(6, 3), subplot_kw=dict(aspect="equal"))
	wedges, texts = ax.pie(parts, wedgeprops=dict(width=0.5), startangle=-40)
	bbox_props = dict(boxstyle="square,pad=0.3", fc="w", ec="k", lw=0.72)
	kw = dict(arrowprops=dict(arrowstyle="-"), bbox=bbox_props, zorder=0, va="center")
	for i, p in enumerate(wedges):
		ang = (p.theta2 - p.theta1)/2. + p.theta1
		y = np.sin(np.deg2rad(ang))
		x = np.cos(np.deg2rad(ang))
		horizontalalignment = {-1: "right", 1: "left"}[int(np.sign(x))]
		connectionstyle = "angle,angleA=0,angleB={}".format(ang)
		kw["arrowprops"].update({"connectionstyle": connectionstyle})
		ax.annotate(label[i], xy=(x, y), xytext=(1.35*np.sign(x), 1.4*y), horizontalalignment=horizontalalignment, **kw)

	ax.set_title("percentages")

	plt.show()
	
	return(label, parts)

def histo(ratio):
	labels = []
	helix = []
	strand = []
	coil = []
	total = []
	prelabel = ratio.keys()
	for i in prelabel:
		labels.append(str(i))
		helix.append(ratio[str(i)]["H"])
		strand.append(ratio[str(i)]["E"])
		coil.append(ratio[str(i)]["-"])
		total.append(ratio[str(i)]["#"])

	x = np.arange(len(labels))  # the label locations
	width = 0.15  # the width of the bars

	fig, ax = plt.subplots()
	rects1 = ax.bar(x - 3*width/2, helix, width, label='helix')
	rects2 = ax.bar(x - width/2, strand, width, label='strand')
	rects3 = ax.bar(x + width/2, coil, width, label='coil')
	rects4 = ax.bar(x + 3* width/2, total, width, label='overall')
	rects = [rects1, rects2, rects3, rects4]

	# Add some text for labels, title and custom x-axis tick labels, etc.
	ax.set_ylabel('percentage')
	ax.set_title('SS by residue')
	ax.set_xticks(x)
	ax.set_xticklabels(labels)
	ax.legend()
	fig.tight_layout()
	plt.show()
	return(labels, helix, strand, coil)

if __name__ == "__main__":
	ff = open(sys.argv[1], "r")
	a, b = count(ff)
	print(pie(ratio(a, b)))
