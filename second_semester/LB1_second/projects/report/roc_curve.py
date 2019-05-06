# roc curve
import matplotlib.pyplot as plt
import sys
import numpy as np
from sklearn.metrics import roc_curve, auc

def get_data(dataf):
	with open(dataf) as f:
		label = []
		e_val = []
		for line in f:
			label.append(float(line.split()[-1]))
			e_val.append(1*float(line.split()[-2]))
	return label,e_val
	
def roc2(fpr,tpr,roc_auc):
	plt.figure()
	plt.plot(fpr, tpr, color='darkorange', lw=1, label='ROC curve (area = %0.2f)' % roc_auc)
	plt.plot([0, 1], [0, 1], color='navy', lw=1, linestyle='--')
	plt.xlim([0.0, 1.0])
	plt.ylim([0.0, 1.05])
	plt.xlabel('False Positive Rate')
	plt.ylabel('True Positive Rate')
	plt.title('Receiver operating characteristic')
	plt.legend(loc="lower right")
	plt.show()	
	
def roc1(fpr,tpr,roc_auc):
	fig, ax = plt.subplots(1,1, figsize=(10,5))
	ax.plot(fpr, tpr)
	#~ ax.plot(x,x, "--")
	ax.set_xlim([0,1])
	ax.set_ylim([0,1])
	ax.set_title("ROC Curve", fontsize=14)
	ax.set_ylabel('TPR', fontsize=12)
	ax.set_xlabel('FPR', fontsize=12)
	ax.grid()
	ax.legend(["AUC=%.5f"%roc_auc])	
	plt.show()


if __name__ == '__main__':
	''' usage: python roc_curve.py labeled_data.txt
	 labeled data comprises both pos and neg data, each with its nice label '''
	labeled_data = sys.argv[1]
	# The input data is split into labels and e-values
	label,e_val = get_data(labeled_data)
	# THE REAL BEEF --> this magic function takes in input the labels and the "predictions" (aka e-val)
	# and returns a list of FPRs and TPRs
	fpr, tpr, thresholds = roc_curve(label, e_val, pos_label=1)
	# Another magical function that computes the area under the curve
	roc_auc = auc(fpr, tpr)
	print roc_auc
	''' two ways to plot it, I prefer the second one'''
	roc2(fpr,tpr,roc_auc)
	roc1(fpr,tpr,roc_auc)
	
	
