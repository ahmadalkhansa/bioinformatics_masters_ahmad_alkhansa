import sys
import os

def extractor(f1, f2):
	l = f1.read().splitlines()
#	m = f2.read().splitlines()
# open first file through lines
	for n in l:
#open second file through lines
		for k in f2:
#			print(n[0:4])
#			print(k[0:4])
# if you find the same ids
			if n.split("_")[0] == k.split(".")[0].upper():
#				print(n)
# open the dssp file and create new file
				f3 = open(sys.argv[2]+str(k), "r")
				q = f3.read().splitlines()
				f4 = open(sys.argv[3]+str(n.split("_")[0])+"_"+str(n.split("_")[1])+".dssp", "w+")
# through the lines and characters of dssp file
				for s in q:
					for w in s:
						letter = s[s.index(w)]
#if the charcter is #
						if w == "#":
#from the beginning of the file till this line -> write all lines to the new file
							for v in range(0,q.index(s)+1):
								f4.write(q[v]+"\n")
#								print(q[v])
#from this line to the end
							for z in range(q.index(s), len(q)):
#								print(q[z][11])
#								print(n[5])
#if the character 11 on the line is the chain -> write the line to the new file
								if q[z][11] == str(n[5]):
									f4.write(q[z]+"\n")
#									print(q[z])
								else:
									continue
						else: continue

				f4.close()

			elif n.split("_")[0] == k.split("-")[0].upper():
				f3 = open(sys.argv[2]+str(k), "r")
				q = f3.read().splitlines()
				f4 = open(sys.argv[3]+str(n.split("_")[0])+"_"+str(n.split("_")[1])+".dssp", "w+")
# through the lines and characters of dssp file
				for s in q:
					for w in s:
						letter = s[s.index(w)]
#if the charcter is #
						if w == "#":
#from the beginning of the file till this line -> write all lines to the new file
							for v in range(0,q.index(s)+1):
								f4.write(q[v]+"\n")
#								print(q[v])
#from this line to the end
							for z in range(q.index(s), len(q)):
#								print(q[z][11])
#								print(n[5])
#if the character 11 on the line is the chain -> write the line to the new file
								if q[z][11] == str(n[5]):
									f4.write(q[z]+"\n")
#									print(q[z])
								else:
									continue
						else: continue

				f4.close()				

	return("")

if __name__ == "__main__":
	f1 = open(sys.argv[1], "r")
	f2 = os.listdir(sys.argv[2])
	print(extractor(f1, f2))
