from modules.paths import Path
from modules.gor import Gor
import os
import pickle
import numpy as np

def gor_train_blind(training_ids):
	novalue_ids = open(Path.training_ids_novalues, "r").read().splitlines()
	modeling_file = open(Path.blind_gor_dir + "modeling_results/blind_model_info.txt", "w+")
	for training_id in training_ids:
		if training_id in novalue_ids:
			print(training_id+" has no values")
		else:
			ss_seq_training = open(Path.dssp_dir + training_id + ".dssp").read().splitlines()[1]
			with open(Path.profile_dir + training_id + ".profile", "rb") as pickled_profile:
				blind_set.windows_calculator(pickle.load(pickled_profile), ss_seq_training)
				pickled_profile.close()
				print(training_id+" probability incrementation is done")

	blind_set.normalize()
	modeling_file.write("helix_window:" + "\n" + str(blind_set.h_window) + "\n\n" + \
						"strand_window:" + "\n" + str(blind_set.e_window) + "\n\n" + \
						"coil_window:" + "\n" + str(blind_set.c_window) + "\n\n" + \
						"common_window:" + "\n" + str(blind_set.common_window) + "\n\n" + \
						"helix_probability = " + str(blind_set.h_probability) + "\n" + \
						"strand_probability = " + str(blind_set.e_probability) + "\n" + \
						"coil_probability = " + str(blind_set.c_probability))
	modeling_file.close()

def gor_predict_blind(predicting_ids):
	for predicting_id in predicting_ids:
		try:
			fasta_seq_predicting = open(Path.blind_fasta_sel_dir + predicting_id + ".fasta").read().splitlines()[1]
			pickled_profile = open(Path.blind_profile_selected_dir + predicting_id + ".profile", "rb")
			prediction_file = open(Path.blind_gor_dir + "predicted_files/" + predicting_id + ".fasta_ss", "w+")
			unpickled_profile = pickle.Unpickler(pickled_profile)
			prediction = blind_set.predict(fasta_seq_predicting, unpickled_profile.load())
			prediction_file.write(">" + predicting_id + "\n" + fasta_seq_predicting + "\n" + prediction)
			prediction_file.close()
			pickled_profile.close()
			print(predicting_id + " blind prediction is successful")

		except:
			print(predicting_id + " prediction id didn't get a hit in psiblast")

def gor_evaluate_blind():
	for predicted_file in os.listdir(Path.blind_gor_dir + "predicted_files/"):
		ss_seq_observed = open(Path.blind_ss_sel_dir + predicted_file.split(".")[0] + ".dssp", "r").read().splitlines()[2]
		ss_seq_predicted = open(Path.blind_gor_dir + "predicted_files/" + predicted_file, "r").read().splitlines()[2]
		blind_set.obs_seq.extend(list(ss_seq_observed))
		blind_set.sov_obs_seq += "b" + ss_seq_observed + "e"
		blind_set.pred_seq.extend(list(ss_seq_predicted))
		blind_set.sov_pred_seq += "b" + ss_seq_predicted + "e"

	# confusion matrix
	blind_set.confusion_matrix()
	blind_set.confusion_reducer("H")
	blind_set.confusion_reducer("E")
	blind_set.confusion_reducer("-")
	blind_set.parameters("H")
	blind_set.parameters("E")
	blind_set.parameters("-")

	# sov part
	blind_set.segment_detector("H")
	blind_set.segment_detector("E")
	blind_set.segment_detector("-")
	blind_set.ov_norm("H")
	blind_set.ov_norm("E")
	blind_set.ov_norm("-")
	blind_set.delta("H")
	blind_set.delta("E")
	blind_set.delta("-")
	blind_set.sov_calculate("H")
	blind_set.sov_calculate("E")
	blind_set.sov_calculate("-")
	evaluation_file = open(Path.blind_gor_dir + "evaluation/blind_evaluation_info.txt", "w+")
	evaluation_file.write(
		"multi-class confusion matrix: \n\n" + np.array2string(blind_set.general_confusion) +"\n"+str(blind_set.accuracy)+ "\n\n" + \
		"Helix 2-class confusion matrix and paramters: \n\n" + np.array2string(
			blind_set.specific_confusion["H"]) + "\n" \
		+ str(blind_set.H_parameters) + "\n\n" + \
		"Strand 2-class confusion matrix and paramters: \n\n" + np.array2string(
			blind_set.specific_confusion["E"]) + "\n" \
		+ str(blind_set.E_parameters) + "\n\n" + \
		"Coil 2-class confusion matrix and paramters: \n\n" + np.array2string(
			blind_set.specific_confusion["-"]) + "\n" \
		+ str(blind_set.C_parameters) + "\n\n" + \
		"sov_H = " + str(blind_set.sov_H) + "\n" + \
		"sov_E = " + str(blind_set.sov_E) + "\n" +
		"sov_C = " + str(blind_set.sov_C) + "\n" +
		"sov = " + str(blind_set.sov))
	evaluation_file.close()



def gor_train_cv(test_instance, training_ids, test_name:str):
	novalue_ids = open(Path.training_ids_novalues, "r").read().splitlines()
	nohits_ids = open(Path.gor_dir+test_name+"nohits_ids.txt", "w+")
	nohits_ids_string = ""
	modeling_file = open(Path.gor_dir + test_name + "/modeling_results/" + test_name + "_model_info.txt", "w+")
	for training_id in training_ids:
		try:
			if training_id in novalue_ids:
				print(training_id+" has no values")
			else:
				ss_seq_training = open(Path.dssp_dir + training_id + ".dssp").read().splitlines()[1]
				with open(Path.profile_dir + training_id + ".profile", "rb") as pickled_profile:
					test_instance.windows_calculator(pickle.load(pickled_profile), ss_seq_training)
					pickled_profile.close()
					print(training_id+" probability incrementation is done")
		except:
			if training_id not in nohits_ids.read().splitlines():
				print(training_id+" has no hits")
				nohits_ids_string += training_id+"\n"

	nohits_ids.write(nohits_ids_string)
	test_instance.normalize()
	modeling_file.write("helix_window:" + "\n" + str(test_instance.h_window) + "\n\n" + \
						"strand_window:" + "\n" + str(test_instance.e_window) + "\n\n" + \
						"coil_window:" + "\n" + str(test_instance.c_window) + "\n\n" + \
						"common_window:" + "\n" + str(test_instance.common_window) + "\n\n" + \
						"helix_probability = " + str(test_instance.h_probability) + "\n" + \
						"strand_probability = " + str(test_instance.e_probability) + "\n" + \
						"coil_probability = " + str(test_instance.c_probability))
	modeling_file.close()
	nohits_ids.close()

def gor_predict_cv(test_instance, predicting_ids, test_name:str):
	novalue_ids = open(Path.training_ids_novalues, "r").read().splitlines()
	for predicting_id in predicting_ids:
		try:
			if predicting_id in novalue_ids:
				print(predicting_id+" has no values")
			else:
				fasta_seq_predicting = open(Path.fasta_dir + predicting_id + ".fasta").read().splitlines()[1]
				pickled_profile = open(Path.profile_dir + predicting_id + ".profile", "rb")
				prediction_file = open(Path.gor_dir+test_name+"/predicted_files/"+predicting_id+".fasta_ss", "w+")
				unpickled_profile = pickle.Unpickler(pickled_profile)
				prediction = test_instance.predict(fasta_seq_predicting, unpickled_profile.load())
				prediction_file.write(">"+predicting_id+"\n"+fasta_seq_predicting+"\n"+prediction)
				prediction_file.close()
				pickled_profile.close()
				print(predicting_id+" prediction is successful")

		except:
			if predicting_id not in novalue_ids:
				print(predicting_id+" has no hits")
			else:
				print("UNKNOWN ERROR + "+predicting_id+"!!! CHECK IT AND MODIFY SCRIPT!!!")

def gor_evaluate_cv(test_instance, test_name:str):
	for predicted_file in os.listdir(Path.gor_dir+test_name+"/predicted_files"):
		if len(predicted_file.split(".")) == 2:
			ss_seq_observed = open(Path.dssp_dir+predicted_file.split(".")[0]+".dssp", "r").read().splitlines()[1]
		elif len(predicted_file.split(".")) == 3:
			ss_seq_observed = open(Path.dssp_dir + predicted_file.split(".")[0] + "." + predicted_file.split(".")[1] + ".dssp", "r").read().splitlines()[1]
		ss_seq_predicted = open(Path.gor_dir+test_name+"/predicted_files/"+predicted_file, "r").read().splitlines()[2]

		test_instance.obs_seq.extend(list(ss_seq_observed))
		test_instance.sov_obs_seq += "b" + ss_seq_observed + "e"
		test_instance.pred_seq.extend(list(ss_seq_predicted))
		test_instance.sov_pred_seq += "b" + ss_seq_predicted + "e"


	#confusion matrix
	test_instance.confusion_matrix()
	test_instance.confusion_reducer("H")
	test_instance.confusion_reducer("E")
	test_instance.confusion_reducer("-")
	test_instance.parameters("H")
	test_instance.parameters("E")
	test_instance.parameters("-")

	#sov part
	test_instance.segment_detector("H")
	test_instance.segment_detector("E")
	test_instance.segment_detector("-")
	test_instance.ov_norm("H")
	test_instance.ov_norm("E")
	test_instance.ov_norm("-")
	test_instance.delta("H")
	test_instance.delta("E")
	test_instance.delta("-")
	test_instance.sov_calculate("H")
	test_instance.sov_calculate("E")
	test_instance.sov_calculate("-")
	evaluation_file = open(Path.gor_dir+test_name+"/evaluation/"+test_name+"_evaluation_info.txt", "w+")
	evaluation_file.write("multi-class confusion matrix: \n\n"+np.array2string(test_instance.general_confusion)+"\n"+str(test_instance.accuracy)+"\n\n"+\
						"Helix 2-class confusion matrix and paramters: \n\n"+np.array2string(test_instance.specific_confusion["H"])+"\n"\
						+ str(test_instance.H_parameters)+"\n\n"+\
						"Strand 2-class confusion matrix and paramters: \n\n"+np.array2string(test_instance.specific_confusion["E"])+"\n"\
						+ str(test_instance.E_parameters)+"\n\n"+\
						"Coil 2-class confusion matrix and paramters: \n\n"+np.array2string(test_instance.specific_confusion["-"])+"\n"\
						+ str(test_instance.C_parameters)+"\n\n"+\
						"sov_H = "+str(test_instance.sov_H)+"\n"+\
						  "sov_E = "+str(test_instance.sov_E)+"\n"+
						  "sov_C = "+str(test_instance.sov_C)+"\n"+
						  "sov = "+str(test_instance.sov))
	evaluation_file.close()


if __name__ == "__main__":
	input_file = pickle.load(open(Path.input_file, "rb"))
	test0 = Gor(input_file['window_size'])
	test1 = Gor(input_file['window_size'])
	test2 = Gor(input_file['window_size'])
	test3 = Gor(input_file['window_size'])
	test4 = Gor(input_file['window_size'])
	blind_set = Gor(input_file['window_size'])

	training_ids_test0 = []
	training_ids_test1 = []
	training_ids_test2 = []
	training_ids_test3 = []
	training_ids_test4 = []
	training_ids_blind_set = []

	cv_prediction_ids_test0 = open(Path.cv_ids_test0, "r").read().splitlines()
	cv_prediction_ids_test1 = open(Path.cv_ids_test1, "r").read().splitlines()
	cv_prediction_ids_test2 = open(Path.cv_ids_test2, "r").read().splitlines()
	cv_prediction_ids_test3 = open(Path.cv_ids_test3, "r").read().splitlines()
	cv_prediction_ids_test4 = open(Path.cv_ids_test4, "r").read().splitlines()
	prediction_ids_blind_set = []
	for ids in os.listdir(Path.blind_fasta_sel_dir):
		prediction_ids_blind_set.append(ids.split(".")[0])


	for cv in os.listdir(Path.cv_dir):
		if "test0" not in cv:
			training_ids_test0.extend(open(Path.cv_dir + cv, 'r').read().splitlines())
		if "test1" not in cv:
			training_ids_test1.extend(open(Path.cv_dir+cv, 'r').read().splitlines())
		if "test2" not in cv:
			training_ids_test2.extend(open(Path.cv_dir+cv, 'r').read().splitlines())
		if "test3" not in cv:
			training_ids_test3.extend(open(Path.cv_dir+cv, 'r').read().splitlines())
		if "test4" not in cv:
			training_ids_test4.extend(open(Path.cv_dir+cv, 'r').read().splitlines())

	training_ids_blind_set.extend(training_ids_test0)
	training_ids_blind_set.extend(training_ids_test1)
	training_ids_blind_set.extend(training_ids_test2)
	training_ids_blind_set.extend(training_ids_test3)
	training_ids_blind_set.extend(training_ids_test4)


	# gor_train_cv(test0, training_ids_test0, "test0")
	# gor_train_cv(test1, training_ids_test1, "test1")
	# gor_train_cv(test2, training_ids_test2, "test2")
	# gor_train_cv(test3, training_ids_test3, "test3")
	# gor_train_cv(test4, training_ids_test4, "test4")
	gor_train_blind(training_ids_test2)

	# gor_predict_cv(test0, cv_prediction_ids_test0, "test0")
	# gor_predict_cv(test1, cv_prediction_ids_test1, "test1")
	# gor_predict_cv(test2, cv_prediction_ids_test2, "test2")
	# gor_predict_cv(test3, cv_prediction_ids_test3, "test3")
	# gor_predict_cv(test4, cv_prediction_ids_test4, "test4")
	gor_predict_blind(prediction_ids_blind_set)


	# gor_evaluate_cv(test0, "test0")
	# gor_evaluate_cv(test1, "test1")
	# gor_evaluate_cv(test2, "test2")
	# gor_evaluate_cv(test3, "test3")
	# gor_evaluate_cv(test4, "test4")
	gor_evaluate_blind()

