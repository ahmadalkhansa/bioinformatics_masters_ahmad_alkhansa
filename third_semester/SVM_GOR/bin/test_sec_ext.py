import sys
import os

def ss_dssp(cc):
	for i in cc:
		x = open(sys.argv[1]+i, "r")
		output = open(sys.argv[2]+i.split('.')[0]+'.fasta.ss', 'w+')
		a = x.readlines()
		ss = ''
		flag = 0
		helix=['H', 'I', 'G']
		beta=['E', 'B']
		coil=['S', 'T',' ']
		rr= ''
		for j in a:
#			print(j)
#			print(j[13])
			if '#' in j:
#				print(j)
				flag = 1
#				print(flag)
				continue
			if flag == 0: continue
			if flag == 1:
#				print(j)
#				print(j[13])
#                                              print(i[11])
				if j[16] in helix:
#					print(j[13])
					ss += 'H'
					if j[13].isupper():
						rr += j[13]
					else:
						rr += 'C'
				elif j[16] in beta:
					ss += 'E'
					if j[13].isupper():
						rr += j[13]
					else:
						rr += 'C'
				elif j[16] in coil:
					ss += 'C'
					if j[13].isupper():
						rr += j[13]
					else:
						rr += 'C'
#                               print(ss)
#                               print(str_len)
		output.write('>'+i.split('_')[0]+'.'+i.split('_')[1]+'\n'+ss+'\n'+rr+'\n')
		output.close()

if __name__ == '__main__':
	
	filein = os.listdir(sys.argv[1])
	print(ss_dssp(filein))
