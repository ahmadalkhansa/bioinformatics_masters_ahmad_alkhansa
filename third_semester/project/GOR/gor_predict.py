import os
import sys
import numpy as np
import math

def tester(training_model):
#	residue = ['', 'K', 'V', 'S', 'H', 'R', 'T', 'E', 'P', 'G', 'L', 'Q', 'D', 'N', 'M', 'A', 'I', 'C', 'Y', 'F', 'W']
	t = np.load(training_model)
#	for i in t:
#		print(i)
	np.load(training_model)
	I = 0
#	print(t)
	for n in os.listdir(sys.argv[2]):
		q = np.load(n)
		e = n.split(",")
		open(sys.argv[3]+str(e[0])+"."+str(e[1])+".ss", "w+")
		output = open(sys.argv[3]+str(e[0])+"."+str(e[1])+".ss", "w+")
		output.write(">"+n.split(",")[0]+"."+n.split(",")[1]+"\n")
		rr = ""
		ss = ""
#		for v in q:
#			print(v)
		for m in range(1,len(q)):
#			print(k[m])
			I_H = 0
			I_E = 0
			I_C = 0
			I = []
			for s in range(1,len(t)):
				h = "res_H 0"
				e = "res_E 0"
				c = "res_C 0"
#				print(t[s][0])
#				print(h)
				if t[s][0] == h:
#					print(t[s][0])
					for k in range(m-8, m+9):
						if k > 0 and k < len(q)-1 and q[k][0] != 'X':
#							print(k)
#							print(m)
#							print(q[k])
							I_H =+ float(q[k][list(q[0]).index(q[k][0])])*float(t[k-(m-8)+1][list(t[0]).index(q[k][0])])
#							print(t[k-(m-8)+1])
							continue
						else: continue
				elif t[s][0] == e:
					for k in range(m-8, m+9):
						if k > 0 and k < len(q)-1 and q[k][0] != 'X':
#							print(k)
#							print(m)
#							print(q[k])
							I_E =+ float(q[k][list(q[0]).index(q[k][0])])*float(t[k-(m-8)+18][list(t[0]).index(q[k][0])])
#							print(t[k-(m-8)+18])
							continue
						else: continue
				elif t[s][0] == c:
					for k in range(m-8, m+9):
						if k > 0 and k < len(q)-1 and q[k][0] != 'X':
#							print(k)
#							print(m)
#							print(q[k])
							I_C =+ float(q[k][list(q[0]).index(q[k][0])])*float(t[k-(m-8)+35][list(t[0]).index(q[k][0])])
#							print(t[k-(m-8)+35])
							continue
						else: continue		
				else: continue
			I.append(I_H)
			I.append(I_E)
			I.append(I_C)
#			print(I)
			if max(I) == I_H:
				rr += q[m][0]
				ss += "H"
			elif max(I) == I_E:
				rr += q[m][0]
				ss += "E"
			elif max(I) == I_C:
				rr += q[m][0]
				ss += "C"
			else: continue
#		print(rr)
		output.write(rr+"\n"+ss+"\n")
		output.close()
#		break

if __name__ == "__main__":
	train = sys.argv[1]
#	total = sys.argv[2]
	print(tester(train))
