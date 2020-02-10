from modules.svm import Svmlocal
from modules.paths import Path
import pickle
import os
import numpy as np


def svm_prepare(test_instance, ids, activity, state):
	sec_seq = ""
	if activity == "cv":
		for name in ids:
			sec_struct_seq = open(Path.dssp_dir + name + ".dssp").read().splitlines()[1]
			sec_seq += sec_struct_seq
			pickled_profile = open(Path.profile_dir + name + ".profile", "rb")
			unpickled_profile = pickle.load(pickled_profile)
			test_instance.context_extractor(unpickled_profile, sec_struct_seq, state)
	#		print(len(sec_seq))
	elif activity == "blind_set":
		for name in ids:
			sec_struct_seq = open(Path.blind_ss_sel_dir + name + ".dssp").read().splitlines()[2]
			sec_seq += sec_struct_seq
			pickled_profile = open(Path.blind_profile_selected_dir + name + ".profile", "rb")
			unpickled_profile = pickle.load(pickled_profile)
			test_instance.context_extractor(unpickled_profile, sec_struct_seq, state)


def svm_translate_cv(prediction_ids: list, test_name, c_parameter, g_parameter, method):
	classes = {"1.0": "H", "2.0": "E", "3.0": "-"}
	if method == "thunder":
		prediction_output = np.load(
			Path.svm_dir + test_name + "/evaluation/thunderprediction_" + str(c_parameter) + "_" + str(
				g_parameter) + ".npy")
		translated_file = open(
			Path.svm_dir + test_name + "/predicted_files/thunder_trans_pred_" + str(c_parameter) + "_" + str(
				g_parameter) + ".fasta_ss", "w+")
		read = 0
		while read < len(prediction_output):
			file_string = ""
			for prediction_id in prediction_ids:
				fasta_seq = open(Path.fasta_dir + prediction_id + ".fasta").read().splitlines()[1]
				ss_seq = ""
				for residue in fasta_seq:
					ss_seq += classes[str(prediction_output[read])]
					read += 1
				file_string += ">" + prediction_id + "\n" \
							   + fasta_seq + "\n" + ss_seq + "\n"
		translated_file.write(file_string)
		translated_file.close()


def svm_translate_blind(prediction_ids: list, c_parameter, g_parameter, method):
	classes = {"1.0": "H", "2.0": "E", "3.0": "-"}
	if method == "thunder":
		prediction_output = np.load(Path.blind_svm_dir + "/evaluation/thunderprediction_" + str(c_parameter) + "_" + str(g_parameter) + ".npy")
		translated_file = open(Path.blind_svm_dir + "/predicted_files/thunder_trans_pred_" + str(c_parameter) + "_" + str(g_parameter) + ".fasta_ss", "w+")
		read = 0
		length = 0
		for prediction_id in prediction_ids:
			fasta_seq = open(Path.blind_ss_sel_dir + prediction_id + ".dssp").read().splitlines()[1]
			length += len(fasta_seq)

		while read < len(prediction_output):
			print(len(prediction_output))
			print(read)
			file_string = ""
			for prediction_id in prediction_ids:
				fasta_seq = open(Path.blind_ss_sel_dir + prediction_id + ".dssp").read().splitlines()[1]
				ss_seq = ""
				for residue in fasta_seq:
					ss_seq += classes[str(prediction_output[read])]
					read += 1
				file_string += ">" + prediction_id + "\n" \
							   + fasta_seq + "\n" + ss_seq + "\n"
				#print(">" + prediction_id + "\n" \
				#			   + fasta_seq + "\n" + ss_seq + "\n")
		translated_file.write(file_string)
		translated_file.close()


def svm_evaluate_cv(test_instance, test_name: str, c_parameter, g_parameter, method):
	if method == "thunder":
		prediction_file = open(Path.svm_dir + test_name + "/predicted_files/thunder_trans_pred_" + str(c_parameter) \
							   + "_" + str(g_parameter) + ".fasta_ss").read().splitlines()
		for pred_id in range(0, len(prediction_file) - 2, 3):
			obs_seq = open(Path.dssp_dir + prediction_file[pred_id][1:] + ".dssp").read().splitlines()[1]
			test_instance.obs_seq.extend(list(obs_seq))
			test_instance.sov_obs_seq += "b" + obs_seq + "e"
			pred_seq = prediction_file[pred_id + 2]
			test_instance.pred_seq.extend(list(pred_seq))
			test_instance.sov_pred_seq += "b" + pred_seq + "e"

		# confusion matrix
		test_instance.confusion_matrix()
		test_instance.confusion_reducer("H")
		test_instance.confusion_reducer("E")
		test_instance.confusion_reducer("-")
		test_instance.parameters("H")
		test_instance.parameters("E")
		test_instance.parameters("-")

		# sov part
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
		evaluation_file = open(Path.svm_dir + test_name + "/evaluation/thunder_" + str(c_parameter) + "_" \
							   + str(g_parameter) + "_" + test_name + "_evaluation_info.txt", "w+")
		evaluation_file.write(
			"multi-class confusion matrix: \n\n" + np.array2string(test_instance.general_confusion) + "\n" + str(
				test_instance.accuracy) + "\n\n" + \
			"Helix 2-class confusion matrix and paramters: \n\n" + np.array2string(
				test_instance.specific_confusion["H"]) + "\n" \
			+ str(test_instance.H_parameters) + "\n\n" + \
			"Strand 2-class confusion matrix and paramters: \n\n" + np.array2string(
				test_instance.specific_confusion["E"]) + "\n" \
			+ str(test_instance.E_parameters) + "\n\n" + \
			"Coil 2-class confusion matrix and paramters: \n\n" + np.array2string(
				test_instance.specific_confusion["-"]) + "\n" \
			+ str(test_instance.C_parameters) + "\n\n" + \
			"sov_H = " + str(test_instance.sov_H) + "\n" + \
			"sov_E = " + str(test_instance.sov_E) + "\n" +
			"sov_C = " + str(test_instance.sov_C) + "\n" +
			"sov = " + str(test_instance.sov))
		evaluation_file.close()


def svm_evaluate_blind(test_instance, c_parameter, g_parameter, method):
	if method == "thunder":
		prediction_file = open(Path.blind_svm_dir + "predicted_files/thunder_trans_pred_" + str(c_parameter) \
							   + "_" + str(g_parameter) + ".fasta_ss").read().splitlines()
		for pred_id in range(0, len(prediction_file) - 2, 3):
			obs_seq = open(Path.blind_ss_sel_dir + prediction_file[pred_id][1:] + ".dssp").read().splitlines()[2]
			test_instance.obs_seq.extend(list(obs_seq))
			test_instance.sov_obs_seq += "b" + obs_seq + "e"
			pred_seq = prediction_file[pred_id + 2]
			test_instance.pred_seq.extend(list(pred_seq))
			test_instance.sov_pred_seq += "b" + pred_seq + "e"

		# confusion matrix
		test_instance.confusion_matrix()
		test_instance.confusion_reducer("H")
		test_instance.confusion_reducer("E")
		test_instance.confusion_reducer("-")
		test_instance.parameters("H")
		test_instance.parameters("E")
		test_instance.parameters("-")

		# sov part
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
		evaluation_file = open(Path.blind_svm_dir + "evaluation/thunder_" + str(c_parameter) + "_" \
							   + str(g_parameter) + "_evaluation_info.txt", "w+")
		evaluation_file.write(
			"multi-class confusion matrix: \n\n" + np.array2string(test_instance.general_confusion) + "\n" + str(
				test_instance.accuracy) + "\n\n" + \
			"Helix 2-class confusion matrix and paramters: \n\n" + np.array2string(
				test_instance.specific_confusion["H"]) + "\n" \
			+ str(test_instance.H_parameters) + "\n\n" + \
			"Strand 2-class confusion matrix and paramters: \n\n" + np.array2string(
				test_instance.specific_confusion["E"]) + "\n" \
			+ str(test_instance.E_parameters) + "\n\n" + \
			"Coil 2-class confusion matrix and paramters: \n\n" + np.array2string(
				test_instance.specific_confusion["-"]) + "\n" \
			+ str(test_instance.C_parameters) + "\n\n" + \
			"sov_H = " + str(test_instance.sov_H) + "\n" + \
			"sov_E = " + str(test_instance.sov_E) + "\n" +
			"sov_C = " + str(test_instance.sov_C) + "\n" +
			"sov = " + str(test_instance.sov))
		evaluation_file.close()


if __name__ == "__main__":

	inputs = pickle.load(open(Path.input_file, "rb"))
	novalue_ids = open(Path.training_ids_novalues, "r").read().splitlines()
	#	nohits_ids = open(Path.training_ids_nohits, "r").read().splitlines()

	if len(inputs.keys()) > 1:
		input_file = pickle.load(open(Path.input_file, "rb"))
		test0 = Svmlocal(input_file['window_size'])
		test1 = Svmlocal(input_file['window_size'])
		test2 = Svmlocal(input_file['window_size'])
		test3 = Svmlocal(input_file['window_size'])
		test4 = Svmlocal(input_file['window_size'])
		blind_set = Svmlocal(input_file['window_size'])

		training_ids_test0 = []
		training_ids_test1 = []
		training_ids_test2 = []
		training_ids_test3 = []
		training_ids_test4 = []
		training_blind_ids = []

		cv_prediction_ids_test0 = []
		cv_prediction_ids_test1 = []
		cv_prediction_ids_test2 = []
		cv_prediction_ids_test3 = []
		cv_prediction_ids_test4 = []
		blind_prediction_ids = []

		for ids in open(Path.cv_ids_test0, "r").read().splitlines():
			if ids + ".profile" in os.listdir(Path.profile_dir):
				cv_prediction_ids_test0.append(ids)
		for ids in open(Path.cv_ids_test1, "r").read().splitlines():
			if ids + ".profile" in os.listdir(Path.profile_dir):
				cv_prediction_ids_test1.append(ids)
		for ids in open(Path.cv_ids_test2, "r").read().splitlines():
			if ids + ".profile" in os.listdir(Path.profile_dir):
				cv_prediction_ids_test2.append(ids)
		for ids in open(Path.cv_ids_test3, "r").read().splitlines():
			if ids + ".profile" in os.listdir(Path.profile_dir):
				cv_prediction_ids_test3.append(ids)
		for ids in open(Path.cv_ids_test4, "r").read().splitlines():
			if ids + ".profile" in os.listdir(Path.profile_dir):
				cv_prediction_ids_test4.append(ids)

		for cv in os.listdir(Path.cv_dir):
			if "test0" not in cv:
				for ids in open(Path.cv_dir + cv, 'r').read().splitlines():
					if ids + ".profile" in os.listdir(Path.profile_dir):
						training_ids_test0.append(ids)
			if "test1" not in cv:
				for ids in open(Path.cv_dir + cv, 'r').read().splitlines():
					if ids + ".profile" in os.listdir(Path.profile_dir):
						training_ids_test1.append(ids)
			if "test2" not in cv:
				for ids in open(Path.cv_dir + cv, 'r').read().splitlines():
					if ids + ".profile" in os.listdir(Path.profile_dir):
						training_ids_test2.append(ids)
			if "test3" not in cv:
				for ids in open(Path.cv_dir + cv, 'r').read().splitlines():
					if ids + ".profile" in os.listdir(Path.profile_dir):
						training_ids_test3.append(ids)
			if "test4" not in cv:
				for ids in open(Path.cv_dir + cv, 'r').read().splitlines():
					if ids + ".profile" in os.listdir(Path.profile_dir):
						training_ids_test4.append(ids)

		training_blind_ids.extend(cv_prediction_ids_test0)
		training_blind_ids.extend(cv_prediction_ids_test1)
		training_blind_ids.extend(cv_prediction_ids_test2)
		training_blind_ids.extend(cv_prediction_ids_test3)
		training_blind_ids.extend(cv_prediction_ids_test4)

		for ids in os.listdir(Path.blind_profile_selected_dir):
			ids = ids.split(".")[0]
			blind_prediction_ids.append(ids)
		# print()
		input_value = list(inputs.values())
		# svm_prepare(test0, training_ids_test0, "cv", "train")
		# svm_prepare(test0, cv_prediction_ids_test0, "cv", "predict")
		# for i in range(1, len(input_value) - 1, 2):
		# 	test0.train_thunder(input_value[i], input_value[i+1], "test0")
		# 	test0.predict_thunder(input_value[i], input_value[i+1], "test0")
		# svm_translate(cv_prediction_ids_test0, "test0", input_value[i], input_value[i + 1], "thunder", "cv")
		# svm_evaluate(Svmlocal(input_file['window_size']), "test0", input_value[i], input_value[i + 1], "thunder", "cv")

		# svm_prepare(test1, training_ids_test1, "cv", "train")
		# svm_prepare(test1, cv_prediction_ids_test1, "cv", "predict")
		# for i in range(1, len(input_value) - 1, 2):
		# test1.train_thunder(input_value[i], input_value[i+1], "test1")
		# test1.predict_thunder(input_value[i], input_value[i+1], "test1")
		# svm_translate(cv_prediction_ids_test1, "test1", input_value[i], input_value[i + 1], "thunder", "cv")
		# svm_evaluate(Svmlocal(input_file['window_size']), "test1", input_value[i], input_value[i + 1], "thunder", "cv")

		# svm_prepare(test2, training_ids_test2, "cv", "train")
		# svm_prepare(test2, cv_prediction_ids_test2, "cv", "predict")
		# for i in range(1, len(input_value) - 1, 2):
		# 	test2.train_thunder(input_value[i], input_value[i+1], "test2")
		# 	test2.predict_thunder(input_value[i], input_value[i+1], "test2")
		# svm_translate(cv_prediction_ids_test2, "test2", input_value[i], input_value[i + 1], "thunder", "cv")
		# svm_evaluate(Svmlocal(input_file['window_size']), "test2", input_value[i], input_value[i + 1], "thunder", "cv")
		#
		# svm_prepare(test3, training_ids_test3, "cv", "train")
		# svm_prepare(test3, cv_prediction_ids_test3, "cv", "predict")
		# for i in range(1, len(input_value) - 1, 2):
		# 	test3.train_thunder(input_value[i], input_value[i+1], "test3")
		# 	test3.predict_thunder(input_value[i], input_value[i+1], "test3")
		# svm_translate(cv_prediction_ids_test3, "test3", input_value[i], input_value[i + 1], "thunder", "cv")
		# svm_evaluate(Svmlocal(input_file['window_size']), "test3", input_value[i], input_value[i + 1], "thunder", "cv")

		# svm_prepare(test4, training_ids_test4, "cv", "train")
		# svm_prepare(test4, cv_prediction_ids_test4, "cv", "predict")
		# for i in range(1, len(input_value) - 1, 2):
		# 	test4.train_thunder_cv(input_value[i], input_value[i+1], "test4")
		# 	test4.predict_thunder_cv(input_value[i], input_value[i+1], "test4")
		# svm_translate(cv_prediction_ids_test4, "test4", input_value[i], input_value[i + 1], "thunder", "cv")
		# svm_evaluate(Svmlocal(input_file['window_size']), "test4", input_value[i], input_value[i + 1], "thunder", "cv")

		#svm_prepare(blind_set, training_blind_ids, "cv", "train")
		svm_prepare(blind_set, blind_prediction_ids, "blind_set", "predict")
		#blind_set.train_thunder_blind(2.0, 0.5)
		blind_set.predict_thunder_blind(4.0, 0.5)
		svm_translate_blind(blind_prediction_ids, 4.0, 0.5, "thunder")
		svm_evaluate_blind(blind_set, 4.0, 0.5, "thunder")

		# for i in range(1, len(input_value)-1, 2):
		# 	test0.train_predict(input_value[i], input_value[i + 1], "test0")
		# 	test1.train_predict(input_value[i], input_value[i + 1], "test1")
		# 	test2.train_predict(input_value[i], input_value[i + 1], "test2")
		# 	test3.train_predict(input_value[i], input_value[i + 1], "test3")
		# 	test4.train_predict(input_value[i], input_value[i + 1], "test4")
