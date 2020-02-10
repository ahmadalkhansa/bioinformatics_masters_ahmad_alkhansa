import sys

def extractor(filename):
	f = filename.read().splitlines()
	for i in f:
		ids = i.split()
		best = 0
		best_id = ''
		for m in ids:
			res = m.split('_')[2]
			if float(res) > float(best):
				best = float(res)
				best_id = m
			else: continue
		print(best_id)

if __name__ == "__main__":
	name = open(sys.argv[1], "r")
	extractor(name)
		
