import sys
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

#                        for m in range(7,len(n)-7):
#                                for k in range(m-7,m+7):
#					if 
#                                        if n[r] not in window.keys():
#						window_H[str(rr[m])] = pos
def window(fil):
	l = fil.read().splitlines()
	window_H = {}
	window_H_mod = {}
	window_E = {}
	window_E_mod = {}
	pos_H_total = {}
	pos_E_total = {}
	for q in l:
		if q[0] == ">":
			r = l.index(q)+2
			rr = l[r]
			s = l.index(q)+1
			ss = l[s]
			for p in rr:
				if p not in window_H.keys():
					window_H[str(p)] = [0 for i in range(17)]
					window_E[str(p)] = [0 for i in range(17)]
					window_H_mod[str(p)] = [0 for i in range(17)]
					window_E_mod[str(p)] = [0 for i in range(17)]
				else:
					continue
		else:
			continue
	
	for n in l:
		if n[0] == ">":
			r = l.index(n)+2
			rr = l[r]
			s = l.index(n)+1
			ss = l[s]
			if len(rr) >= 17:
				for m in range(8,len(rr)-9):
					if ss[m] == "H":
						for k in range(m-8,m+9):
							window_H[rr[k]][k-(m-8)] += 1
#							pos_H_total[k-(m-8)] += 1
					elif ss[m] == "E":
						for k in range(m-8,m+9):
							window_E[rr[k]][k-(m-8)] += 1
#							pos_E_total[k-(m-8)] += 1
					else:
						continue
			
			else:
				continue

		else:
			continue
	
	for g in range(17):
		pos_H_total[str(g)] = 0	
		pos_E_total[str(g)] = 0
		for f in window_H.keys():
			pos_H_total[str(g)] += window_H[f][g]
			pos_E_total[str(g)] += window_E[f][g]
	
	for j in range(17):
		for f in window_H.keys():
			window_H_mod[f][j] = float(window_H[f][j])/pos_H_total[str(j)]
			window_E_mod[f][j] = float(window_E[f][j])/pos_E_total[str(j)]

	df_H = pd.DataFrame(window_H_mod).T # generate a dataframe
	df_E = pd.DataFrame(window_E_mod).T

	grid_kws = {"height_ratios": (.9, .05), "hspace": .3}
	f, ((ax1, ax2), (cbar_ax1, cbar_ax2)) = plt.subplots(2, 2, gridspec_kw=grid_kws)
	f.suptitle('Residue composition: windows', fontname="DejaVu Sans", fontweight="bold", fontsize=14)

	ax1 = sns.heatmap(df_H, ax=ax1, cbar_ax=cbar_ax1, cmap="mako", cbar_kws={"orientation": "horizontal", "label": "Residue frequency"},)
	ax1.set_title("Helix")
	ax2 = sns.heatmap(df_E, ax=ax2, cbar_ax=cbar_ax2, cmap="mako", cbar_kws={"orientation": "horizontal", "label": "Residue frequency"},)
	ax2.set_title("Strand")
	plt.show()

	return(window_H_mod, window_E_mod)
if __name__ == "__main__":
	ff = open(sys.argv[1], "r")
	print(window(ff))	
