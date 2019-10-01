import sys
import matplotlib.pyplot as plt
import numpy as np
import pprint
#tail -n 2839 tabularResults.csv| head -n 2837 | sed 's/"//g' | sed 's/^/>/g' | sed 's/,/\t/g' | cut -f 1,3 | awk -F '\t' '($2!="")' | sort -u > species.txt



def counter(fou):
	lines=fou.read().splitlines()
#	print(lines)
	species = {}
	t = 0
	for i in lines:
		name = i[i.index(",")+1:len(i)]
		if name not in species.keys():
			species[str(name)] = 0
			species[str(name)] += 1
			t += 1
		else:
			species[str(name)] += 1
			t += 1
	
	return(species, t)

def pie(species, t):
	ratio = {}
	rratio = {}
	ratio["Others"] = 0
	for k in species.keys():
		if species[str(k)] < 25:
			ratio["Others"] += (float(species[str(k)])/t)*100
		else:
			ratio[str(k)] = (float(species[str(k)])/t)*100
	
	for l in ratio.keys():
		rratio[str(l)] = round(ratio[str(l)])
	
	label = []
	parts = []
	prelabel = rratio.keys()
	for i in prelabel:
		label.append(str(i))
		parts.append(rratio[str(i)])

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

if __name__ == "__main__":
	fou = open(sys.argv[1], "r")
	a, b = counter(fou)
	print(pie(a, b))
