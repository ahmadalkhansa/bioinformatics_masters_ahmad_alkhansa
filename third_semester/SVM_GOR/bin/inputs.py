from modules.paths import Path
import pickle
"""The script is for organizing inputs and sharing them among different scripts by creating a pickled file that
can be accessed by several scripts"""

def window_adder(inputs):
	window = input("please enter window size \n")
	while (int(window) % 2 == 0):
		print("ERROR: window size is not odd")
		window = input("please try again \n")
	inputs['window_size'] = int(window)

def svm_models(inputs):
	model_number = 1
	while model_number == 1:
		model_request = input("Would you like to train svm models? (y or n): ")
		if model_request.lower() == "y":
			print("enter model 1 parameters: ")
			C_model_SVM = input("C parameter = ")
			G_model_SVM = input("G parameter = ")
			inputs['1_C_SVM'] = float(C_model_SVM)
			inputs['1_G_SVM'] = float(G_model_SVM)
			model_number += 1
		elif model_request.lower() == "n":
			break
		else:
			print("Incomprehensible response, please try again")
	while model_number <= 10 and model_number > 1:
		additional_models = input("Additional SVM models? (y or n): ")
		if additional_models.lower() == "y":
			print("enter model "+str(model_number)+" parameters: ")
			C_model_SVM = input("C parameter = ")
			G_model_SVM = input("G parameter = ")
			inputs[str(model_number)+'_C_SVM'] = float(C_model_SVM)
			inputs[str(model_number)+'_G_SVM'] = float(G_model_SVM)
			model_number += 1
		elif additional_models.lower() == "n":
			break
		else:
			print("Incomprehensible response, please try again")




if __name__ == "__main__":
	inputs = {}
	input_file = open(Path.input_file, "wb")
	window_adder(inputs)
	svm_models(inputs)
	print(inputs)
	pickle.dump(inputs, input_file)
	input_file.close()