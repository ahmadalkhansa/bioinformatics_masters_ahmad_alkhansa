#!/urs/bin/
import sys
import numpy as np

'''
def Pretty_CM(cm):
    print '     Neg     Pos'
    a = 0
    for i in cm:
        if a == 0
            print Neg   i
            a += 1
        else:
            print Pos   i

'''
def conf_mat(filename, th, sp = -2, cp =-1): # Used to defive default variables in a function: score position, class position 
    cm = [[0.0,0.0],[0.0,0.0]] # Confusion matrix
    f = open(filename) 
    for line in f:
        v = line.rstrip().split()

        if int(v[cp]) == 1: 
            i = 1 # It belong to the positive set -> kunitz
        else:
            i = 0 # It belong to the negative set -> non-kunitz
        if float(v[sp]) < th: 
            j = 1 # Predicted as kunitz
        else:
            j = 0 # Predicted as non-kunitz 

        cm[i][j] = cm[i][j] +1
        #print cm
        #raw_input("continue")

    return cm

def print_performance(cm):
    acc = (cm[0][0]+cm[1][1])/(cm[0][0]+cm[1][1]+cm[1][0]+cm[0][1])
    
    d = np.sqrt(cm[0][0]+cm[0][1])*(cm[0][0]+cm[1][0])*(cm[1][1]+cm[0][1])*(cm[1][1]+cm[1][0]) #denominator 
    mc = (cm[0][0]*cm[1][1]-cm[0][1]*cm[1][0])/d # metwe correlation 

    print 'Parameter:\n', 'Q2 = ', acc, 'MCC = ', mc/d


if __name__='__main__':
    filename = sys.argv[1]
    th = float(sys.argv[2]) # E-value treashold 
    cm = conf_mat(filename,th)
    print cm
    print_performance(cm)

'''
By changing the E-value in input you can perform the optimization of your model 
'''