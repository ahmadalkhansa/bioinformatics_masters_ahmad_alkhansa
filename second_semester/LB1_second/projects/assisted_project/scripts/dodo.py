#!/usr/bin/python
import sys
"""
def get_fasta(sid, fasta):
    f = open(fasta)
    c = 0
    for line in f:
        line = line.rstrip()
        if line[0] == '>':
            tid = line.split('|')[1]
        if tid == sid:
            c = 1
            print(line)
        else:
            c = 0
"""
def get_list_fasta(lid, fasta):
	f = open(fasta)
	c = 0
	for line in f:
		line = line.rstrip()
		if line[0] == '>':
			tid = line.split('|')[1]
		if tid in lid:
			c = 1
		else:
			c = 0
		if c == 1:
			print(line)


if __name__ == "__main__":
	# sid = sys.argv[1]
	fid = sys.argv[1]  # seq ids stored in a file passed as input
	fasta=sys.argv[2]
	# get_fasta(sid, fasta)
	lid = open(fid).read().split('\n')  # open the file containing ids and make a list out of it
	get_list_fasta(lid, fasta)

