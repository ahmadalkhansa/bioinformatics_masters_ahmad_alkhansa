from math import sqrt

def calculator(val_list):
	avg = 0
	for val in val_list:
		avg += val
	avg = float(avg)/len(val_list)
	pre_SE = 0
	for val in val_list:
		pre_SE += (val-avg)**2
	SE = sqrt(pre_SE)/len(val_list)
	print(avg)
	return(SE)

if __name__ == "__main__":
	val_list = [66,69,68,65,65]
	print(calculator(val_list))