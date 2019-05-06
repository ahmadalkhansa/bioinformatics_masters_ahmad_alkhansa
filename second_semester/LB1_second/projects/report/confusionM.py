import sys
import numpy as np
import math

def conf_mat(filename,th,sp=-2,cp=-1):
	#th is the treshold
	confusion_m = [[0.0,0.0],[0.0,0.0]] # row1 neg set, row2 pos set
	'''T Neg | F negative
	   ------------------
	   F Pos | T positive  '''
	with open(filename) as f:
		for line in f:
			v = line.rstrip().split()
			if int(v[cp])==0: i=1
			if int(v[cp])==1: i=0
			if float(v[sp])<th: 
				j=1
			else: 
				j=0
			confusion_m[i][j] += 1
	print('''	   T Neg | F positive %r
	   ------------------
	   F Neg | T positive %r '''%(confusion_m[0],confusion_m[1]))
	return confusion_m 
	
def print_performance(cm):
	TP = cm[1][1]
	TN = cm[0][0]
	FP = cm[0][1]
	FN = cm[1][0]
	acc = (TP+TN)/(sum(cm[0])+sum(cm[1]))
	d = math.sqrt((TP+FP)*(TP+FN)*(TN+FP)*(TN+FN))
	mc=((TP*TN)-(FP*FN))/d
	precision = TP/(TP+FP)
	TPR = (TP)/(TP+FN)
	FPR = (FP)/(FP+TN)
	print ( '>>','TPR ',TPR,'FPR ',FPR ,'Q2=', acc,'MCC ',mc, 'PRECISION ', precision)
  

				
		

if __name__ == '__main__':
	filename = sys.argv[1] #labeled data
	th = float(sys.argv[2])  # threshold
	score_pos = -2          # position of the score
	if len(sys.argv)>3:
		score_pos = int(sys.argv[3])-1
	print('Threshold ',th)
	cm = conf_mat(filename,th,score_pos)
	print_performance(cm)
	print()
