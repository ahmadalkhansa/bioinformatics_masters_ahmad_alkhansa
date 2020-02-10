from modules.paths import Path
from modules.evaluation import Sov
from sklearn import svm
from sklearn import metrics
import thundersvm
import pickle
import time
import datetime
import numpy as np

class Svmlocal(Sov):

	def __init__(self, window_size):
		super().__init__()
		self.window_size = window_size
		self.labels_train = []
		self.windows_train = []
		self.labels_predict = []
		self.windows_predict = []


	def context_extractor(self, profile, sec_struct_seq, state):
		labels = []
		windows = []
		for residue in range(self.window_size // 2, len(profile) - self.window_size // 2):
			if sec_struct_seq[residue - self.window_size // 2] == "H":
				labels.append(float(1))
				window = []
				for context in range(residue - self.window_size // 2, residue + self.window_size // 2):
					window.extend(profile[context])
				windows.append(window)
			elif sec_struct_seq[residue - self.window_size // 2] == "E":
				labels.append(float(2))
				window = []
				for context in range(residue - self.window_size // 2, residue + self.window_size // 2):
					window.extend(profile[context])
				windows.append(window)
			elif sec_struct_seq[residue - self.window_size // 2] == "-":
				labels.append(float(3))
				window = []
				for context in range(residue - self.window_size // 2, residue + self.window_size // 2):
					window.extend(profile[context])
				windows.append(window)
		if state == "train":
			self.windows_train.extend(windows)
			self.labels_train.extend(labels)
		elif state == "predict":
			self.windows_predict.extend(windows)
			self.labels_predict.extend(labels)


	def train_predict_cv(self, c_parameter, g_parameter,testname):
		mySVC = svm.SVC(C=float(c_parameter), kernel='rbf', gamma=float(g_parameter))
		mySVC.fit(self.windows_train, self.labels_train)
		pickle.dump(mySVC, Path.svm_dir+testname+"/model_results/model_"+str(c_parameter)+"_"+str(g_parameter))
		prediction = mySVC.predict(self.windows_predict)
		np.save(Path.svm_dir + testname + "/evaluation/prediction_" + str(c_parameter) + "_" + str(g_parameter)+".npy", prediction)
		print("Accuracy:", metrics.accuracy_score(self.labels_predict, prediction))

	def train_thunder_cv(self, c_parameter, g_parameter,testname):
		mySVC: thundersvm.SVC
		start_time = time.time()
		print(datetime.datetime.now().time())
		print(len(self.windows_train))
		print(len(self.labels_train))
		print(c_parameter, g_parameter)
		mySVC = thundersvm.SVC(C=float(c_parameter), kernel="rbf", gamma=float(g_parameter), max_mem_size=2000)
		mySVC.fit(self.windows_train, self.labels_train)
		mySVC.save_to_file(Path.svm_dir+testname+"/modeling_results/thundermodel_"+str(c_parameter)+"_"+str(g_parameter))
		print("execution duration = %s minutes" % (round((time.time() - start_time) / 60, 2)))

	def predict_thunder_cv(self, c_parameter, g_parameter,testname):
		mySVC: thundersvm.SVC
		model = Path.svm_dir+testname+"/modeling_results/thundermodel_"+str(c_parameter)+"_"+str(g_parameter)
		start_time = time.time()
		print(datetime.datetime.now().time())
		print(len(self.windows_predict))
		print(len(self.labels_predict))
		print(c_parameter, g_parameter)
		mySVC = thundersvm.SVC(C=float(c_parameter), kernel="rbf", gamma=float(g_parameter), max_mem_size=2000)
		mySVC.load_from_file(model)
		prediction = mySVC.predict(self.windows_predict)
		np.save(Path.svm_dir + testname + "/evaluation/thunderprediction_" + str(c_parameter) + "_" + str(g_parameter)+".npy", prediction)
		print("execution duration = %s minutes" % (round((time.time() - start_time) / 60, 2)))
		print("Accuracy:", metrics.accuracy_score(self.labels_predict, prediction))

	def train_thunder_blind(self, c_parameter, g_parameter):
		mySVC: thundersvm.SVC
		start_time = time.time()
		print(datetime.datetime.now().time())
		print(len(self.windows_train))
		print(len(self.labels_train))
		print(c_parameter, g_parameter)
		mySVC = thundersvm.SVC(C=float(c_parameter), kernel="rbf", gamma=float(g_parameter), max_mem_size=2000)
		mySVC.fit(self.windows_train, self.labels_train)
		mySVC.save_to_file(Path.blind_svm_dir + "modeling_results/thundermodel_" + str(c_parameter) + "_" + str(g_parameter))
		print("execution duration = %s minutes" % (round((time.time() - start_time) / 60, 2)))

	def predict_thunder_blind(self, c_parameter, g_parameter):
		mySVC: thundersvm.SVC
		model = Path.blind_svm_dir+"modeling_results/thundermodel_"+str(c_parameter)+"_"+str(g_parameter)
		start_time = time.time()
		print(datetime.datetime.now().time())
		print(len(self.windows_predict))
		print(len(self.labels_predict))
		print(c_parameter, g_parameter)
		mySVC = thundersvm.SVC(C=float(c_parameter), kernel="rbf", gamma=float(g_parameter), max_mem_size=2000)
		mySVC.load_from_file(model)
		prediction = mySVC.predict(self.windows_predict)
		np.save(Path.blind_svm_dir + "evaluation/thunderprediction_" + str(c_parameter) + "_" + str(g_parameter)+".npy", prediction)
		print("execution duration = %s minutes" % (round((time.time() - start_time) / 60, 2)))
		print("Accuracy:", metrics.accuracy_score(self.labels_predict, prediction))