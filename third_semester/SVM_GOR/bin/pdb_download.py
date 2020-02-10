import os
from eval_gor_svm_prj.bin.modules.paths import Path

if __name__ == "__main__":
	idlistdown = ""
	idlistnom = ""
	profile_list = os.listdir(Path.blind_profile_dir)
	nomids = open(Path.blind_nominated_chids, "w+")
	idstodownload = open("../results/blind_set/downloadingids.txt", "w+")
	for i in range(150):
		pdb_id = profile_list[i]
		idlistdown+=pdb_id.split("_")[0]+"\n"
		idlistnom+=pdb_id.split("_")[0] + "_" + pdb_id.split("_")[1]+"\n"
	nomids.write(idlistnom)
	idstodownload.write(idlistdown)
	nomids.close()
	idstodownload.close()