from sklearn.metrics import confusion_matrix
import numpy as np
from math import sqrt
from abc import ABCMeta, abstractmethod
# metaclass=ABCMeta


class Evaluation:

	obs_seq: list
	pred_seq: list

	def __init__(self):
		self.labels = ['H', 'E', '-']
		self.obs_seq = []
		self.pred_seq = []
		self.specific_confusion = {}
		self.general_confusion = []
		self.accuracy = 0
		self.H_parameters = {"true_positive": 0, \
				  "false_positive": 0, \
				  "true_negative": 0, \
				  "false_negative": 0, \
				  "accuracy": 0, \
				  "precision": 0, \
				  "sensitivity": 0, \
				  "MCC": 0}
		self.E_parameters = {"true_positive": 0, \
				  "false_positive": 0, \
				  "true_negative": 0, \
				  "false_negative": 0, \
				  "accuracy": 0, \
				  "precision": 0, \
				  "sensitivity": 0, \
				  "MCC": 0}
		self.C_parameters = {"true_positive": 0, \
				  "false_positive": 0, \
				  "true_negative": 0, \
				  "false_negative": 0, \
				  "accuracy": 0, \
				  "precision": 0, \
				  "sensitivity": 0, \
				  "MCC": 0}

	def reset(self):
		dic = vars(self)
		for key in dic.keys():
			if dic[key] is list:
				dic[key] = []
			elif dic[key] is dict:
				for inside_keys in dic[key].keys():
					dic[key][inside_keys] = 0
			elif dic[key] is int:
				dic[key] = 0




	def confusion_matrix(self):
			self.general_confusion = confusion_matrix(self.obs_seq, self.pred_seq, labels=['H', 'E', '-'])
			true_positives = 0
			for true_positive in range(len(self.general_confusion)):
				true_positives += self.general_confusion[true_positive][true_positive]
			self.accuracy = round((true_positives / len(self.obs_seq)) * 100, 2)


	def confusion_reducer(self, secondary_structure: str):
		reduced_confusion = [[0,0],[0,0]]
		for predicted in range(len(self.general_confusion)):
			for observed in range(len(self.general_confusion[predicted])):
				if predicted == self.labels.index(secondary_structure) and observed == self.labels.index(secondary_structure):
					reduced_confusion[0][0] += self.general_confusion[predicted][observed]
				elif predicted == self.labels.index(secondary_structure) and observed != self.labels.index(secondary_structure):
					reduced_confusion[0][1] += self.general_confusion[predicted][observed]
				elif predicted != self.labels.index(secondary_structure) and observed == self.labels.index(secondary_structure):
					reduced_confusion[1][0] += self.general_confusion[predicted][observed]
				elif predicted != self.labels.index(secondary_structure) and observed != self.labels.index(secondary_structure):
					reduced_confusion[1][1] += self.general_confusion[predicted][observed]
		self.specific_confusion[secondary_structure] = np.array(reduced_confusion)

	def parameters(self, secondary_structure:str):
		attribute = {}
		confusion = self.specific_confusion[secondary_structure]
		if secondary_structure == "H":
			attribute = self.H_parameters
		elif secondary_structure == "E":
			attribute = self.E_parameters
		elif secondary_structure == "-":
			attribute = self.C_parameters

		attribute["true_positive"] = confusion[0][0]
		attribute["false_positive"] = confusion[0][1]
		attribute["true_negative"] = confusion[1][1]
		attribute["false_negative"] = confusion[1][0]
		attribute["accuracy"] = round((float(attribute["true_positive"])+float(attribute["true_negative"]))/\
									   (float(attribute["true_positive"])+float(attribute["true_negative"])+\
										float(attribute["false_positive"])+float(attribute["false_negative"])),2)
		attribute["precision"] = round(float(attribute["true_positive"]) / (attribute["true_positive"]+attribute["false_positive"]),2)
		attribute["sensitivity"] = round(float(attribute["true_positive"]) / (attribute["true_positive"] +attribute["false_negative"]),2)
		attribute["MCC"] = round(((attribute["true_positive"]*attribute["true_negative"])-(attribute["false_positive"]*attribute["false_negative"]))/ \
								 sqrt((attribute["true_positive"] + attribute["false_positive"]) * (
											 attribute["true_positive"] + attribute["false_negative"]) * \
									  (attribute["true_negative"] + attribute["false_positive"]) * (
												  attribute["true_negative"] + attribute["false_negative"])),2)

		if secondary_structure == "H":
			self.H_parameters = attribute
		elif secondary_structure == "E":
			self.E_parameters = attribute
		elif secondary_structure == "-":
			self.C_parameters = attribute

class Sov(Evaluation):

	def __init__(self):
		super(Sov, self).__init__()
		# the first two need to have b and e around each sequence and they contain all the sequences
		self.sov_obs_seq = ""
		self.sov_pred_seq = ""
		self.sov_H = 0
		self.sov_E = 0
		self.sov_C = 0
		self.pre_sov_H = 0
		self.pre_sov_E = 0
		self.pre_sov_C = 0


		self.sov_H_parameters = {"ov_min": [], \
								 "ov_max": [], \
								 "l_obs_segs": [], \
								 "l_pred_segs": [], \
								 "normalize": 0, \
								 "segment_indices_obs": [], \
								 "segment_indices_pred": [], \
								 "delta": []}

		self.sov_E_parameters = {"ov_min": [], \
								 "ov_max": [], \
								 "l_obs_segs": [], \
								 "l_pred_segs": [], \
								 "normalize": 0, \
								 "segment_indices_obs": [], \
								 "segment_indices_pred": [], \
								 "delta": []}

		self.sov_C_parameters = {"ov_min": [], \
								 "ov_max": [], \
								 "l_obs_segs": [], \
								 "l_pred_segs": [], \
								 "normalize": 0, \
								 "segment_indices_obs": [], \
								 "segment_indices_pred": [], \
								 "delta": []}


	def segment_detector(self, ss: str):
		def slider(instance_seq):
			segment_indices = []
			for residue in range(len(instance_seq)):
				if instance_seq[residue] == ss:
					if instance_seq[residue] == instance_seq[residue-1]:
						pass
					else:
						segment_indices.append(residue-1)
				else:
					if instance_seq[residue-1] == ss:
						segment_indices.append(residue - 2)
			return segment_indices

		if ss == "H":
			self.sov_H_parameters["segment_indices_obs"] = slider(self.sov_obs_seq)
			self.sov_H_parameters["segment_indices_pred"] = slider(self.sov_pred_seq)
		elif ss == "E":
			self.sov_E_parameters["segment_indices_obs"] = slider(self.sov_obs_seq)
			self.sov_E_parameters["segment_indices_pred"] = slider(self.sov_pred_seq)
		elif ss == "-":
			self.sov_C_parameters["segment_indices_obs"] = slider(self.sov_obs_seq)
			self.sov_C_parameters["segment_indices_pred"] = slider(self.sov_pred_seq)

	def ov_norm(self, ss: str):

		mark = []
		ov_min = []
		ov_max = []
		l_obs = []
		l_pred = []
		normalize = 0
		obs_s = []
		pred_s = []

		if ss == "H":
			obs_s = self.sov_H_parameters["segment_indices_obs"]
			pred_s = self.sov_H_parameters["segment_indices_pred"]
		elif ss == "E":
			obs_s = self.sov_E_parameters["segment_indices_obs"]
			pred_s = self.sov_E_parameters["segment_indices_pred"]
		elif ss == "-":
			obs_s = self.sov_C_parameters["segment_indices_obs"]
			pred_s = self.sov_C_parameters["segment_indices_pred"]


		for k in range(len(obs_s)):
			mark.append(['1'])
		#   print(mark)
		for i in range(0, len(obs_s), 2):
			for j in range(0, len(pred_s), 2):
				if int(pred_s[j]) < int(obs_s[i]) and int(pred_s[j + 1]) < int(obs_s[i]):
					continue
				elif int(pred_s[j]) > int(obs_s[i + 1]):
					continue
				elif int(pred_s[j]) <= int(obs_s[i]) and int(pred_s[j + 1]) >= int(obs_s[i + 1]):
					ov_min.append(int(obs_s[i + 1] - obs_s[i]) + 1)
					ov_max.append(int(pred_s[j + 1] - pred_s[j]) + 1)
					l_obs.append(int(obs_s[i + 1] - obs_s[i]) + 1)
					l_pred.append(int(pred_s[j + 1] - pred_s[j]) + 1)
					mark[i].append('2')
					continue
				elif int(pred_s[j]) <= int(obs_s[i]) and int(pred_s[j + 1]) <= int(obs_s[i + 1]):
					ov_min.append(int(pred_s[j + 1] - obs_s[i]) + 1)
					ov_max.append(int(obs_s[i + 1] - pred_s[j]) + 1)
					l_obs.append(int(obs_s[i + 1] - obs_s[i]) + 1)
					l_pred.append(int(pred_s[j + 1] - pred_s[j]) + 1)
					mark[i].append('2')
					continue
				elif int(pred_s[j]) >= int(obs_s[i]) and int(pred_s[j + 1]) >= int(obs_s[i + 1]):
					ov_min.append(int(obs_s[i + 1] - pred_s[j]) + 1)
					ov_max.append(int(pred_s[j + 1] - obs_s[i]) + 1)
					l_obs.append(int(obs_s[i + 1] - obs_s[i]) + 1)
					l_pred.append(int(pred_s[j + 1] - pred_s[j]) + 1)
					mark[i].append('2')
					continue
				elif int(pred_s[j]) >= int(obs_s[i]) and int(pred_s[j + 1]) <= int(obs_s[i + 1]):
					ov_min.append(int(pred_s[j + 1] - pred_s[j]) + 1)
					ov_max.append(int(obs_s[i + 1] - obs_s[i]) + 1)
					l_obs.append(int(obs_s[i + 1] - obs_s[i]) + 1)
					l_pred.append(int(pred_s[j + 1] - pred_s[j]) + 1)
					mark[i].append('2')
					continue
				else:
					print('error')
					print(obs_s[i], obs_s[i + 1])
					print(pred_s[j], pred_s[j + 1])
					continue

		if len(mark) > 1:
			for segment_index in range(0, len(mark), 2):
				if len(mark[segment_index]) == 1:
					normalize += (len(mark[segment_index]))*(obs_s[segment_index+1]-obs_s[segment_index]+1)
				elif len(mark[segment_index]) > 1:
					normalize += (len(mark[segment_index])-1) * (obs_s[segment_index + 1] - obs_s[segment_index] + 1)
		else:
			normalize = 0

		if ss == "H":
			self.sov_H_parameters["ov_min"] = ov_min
			self.sov_H_parameters["ov_max"] = ov_max
			self.sov_H_parameters["l_obs_segs"] = l_obs
			self.sov_H_parameters["l_pred_segs"] = l_pred
			self.sov_H_parameters["normalize"] = normalize

		elif ss == "E":
			self.sov_E_parameters["ov_min"] = ov_min
			self.sov_E_parameters["ov_max"] = ov_max
			self.sov_E_parameters["l_obs_segs"] = l_obs
			self.sov_E_parameters["l_pred_segs"] = l_pred
			self.sov_E_parameters["normalize"] = normalize

		elif ss == "-":
			self.sov_C_parameters["ov_min"] = ov_min
			self.sov_C_parameters["ov_max"] = ov_max
			self.sov_C_parameters["l_obs_segs"] = l_obs
			self.sov_C_parameters["l_pred_segs"] = l_pred
			self.sov_C_parameters["normalize"] = normalize

	def delta(self, ss:str):
		def min_adder(l_obs_segs, l_pred_segs, ov_min, ov_max):
			delta_values = []
			# delta_list = []
			for seg_pos in range(len(l_obs_segs)):
				temp_ov_max = ov_max[seg_pos]
				temp_ov_min = ov_min[seg_pos]
				temp_l_obs = float(l_obs_segs[seg_pos])/2
				temp_l_pred = float(l_pred_segs[seg_pos])/2
				delta_list = [temp_ov_max - temp_ov_min, temp_l_obs, temp_l_pred]
				delta_values.append(min(delta_list))
			return delta_values
		if ss == "H":
			self.sov_H_parameters["delta"] = min_adder(self.sov_H_parameters["l_obs_segs"], \
													   self.sov_H_parameters["l_pred_segs"], \
													   self.sov_H_parameters["ov_min"], self.sov_H_parameters["ov_max"])
		elif ss == "E":
			self.sov_E_parameters["delta"] = min_adder(self.sov_E_parameters["l_obs_segs"], \
													   self.sov_E_parameters["l_pred_segs"], \
													   self.sov_E_parameters["ov_min"], self.sov_E_parameters["ov_max"])
		elif ss == "-":
			self.sov_C_parameters["delta"] = min_adder(self.sov_C_parameters["l_obs_segs"], \
													   self.sov_C_parameters["l_pred_segs"], \
													   self.sov_C_parameters["ov_min"], self.sov_C_parameters["ov_max"])

	def sov_calculate(self, ss: str):
		if ss == "H":
			for segment in range(len(self.sov_H_parameters["l_obs_segs"])):
				self.pre_sov_H += (float(self.sov_H_parameters["ov_min"][segment])+\
								  float(self.sov_H_parameters["delta"][segment]))*\
								  float(self.sov_H_parameters["l_obs_segs"][segment])/\
						   float(self.sov_H_parameters["ov_max"][segment])
			self.sov_H = self.pre_sov_H * 100 / self.sov_H_parameters["normalize"]
		elif ss == "E":
			for segment in range(len(self.sov_E_parameters["l_obs_segs"])):
				self.pre_sov_E += (float(self.sov_E_parameters["ov_min"][segment])+\
						float(self.sov_E_parameters["delta"][segment]))*\
								  float(self.sov_E_parameters["l_obs_segs"][segment])/\
						   float(self.sov_E_parameters["ov_max"][segment])
			self.sov_E = self.pre_sov_E * 100 / self.sov_H_parameters["normalize"]
		elif ss == "-":
			for segment in range(len(self.sov_C_parameters["l_obs_segs"])):
				self.pre_sov_C += (float(self.sov_C_parameters["ov_min"][segment])+\
						float(self.sov_C_parameters["delta"][segment]))*\
								  float(self.sov_C_parameters["l_obs_segs"][segment])/\
						   float(self.sov_C_parameters["ov_max"][segment])
			self.sov_C = self.pre_sov_C * 100 / self.sov_H_parameters["normalize"]

		self.normalize = self.sov_H_parameters["normalize"] + self.sov_E_parameters["normalize"] + \
						 self.sov_C_parameters["normalize"]
		self.sov = (self.pre_sov_H + self.pre_sov_E + self.pre_sov_C) * 100 / self.normalize








