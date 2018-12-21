import os 
from os import listdir
from os.path import isfile, join
from collections import OrderedDict

MYPATH = os.getcwd() + "\\KoreanList"
onlyfiles = [f for f in listdir(MYPATH) if isfile(join(MYPATH, f))]

def EmptyLineRemover():
	EmptyLines= 0
	for each in onlyfiles:
		new_temp= []
		target_file= MYPATH+"\\"+each
		name, ext = os.path.splitext(each)

		if(ext == ".txt"):
			f = open(target_file,"r")
			lines = f.readlines()
			f.close()

			for line in lines:
				if line == "\n":
					EmptyLines = EmptyLines + 1
					continue
				else:
					new_temp.append(line)

			f = open(target_file,"w")
			for line in new_temp:
				f.write(line)
			f.close()
		print(str(EmptyLines) + " empty lines are reduced in filename:" + each)

def DuplicateRedundancyRemover():
	for each in onlyfiles:
		new_temp= []
		target_file= MYPATH+"\\"+each
		name, ext = os.path.splitext(each)

		if(ext == ".txt"):
			f = open(target_file,"r")
			lines = f.readlines()
			f.close()

			RemovedSet= list(set(lines))

			f = open(target_file,"w")
			for line in RemovedSet:
				f.write(line)
			f.close()

		print(str(len(lines) - len(RemovedSet)) + " duplicated lines are reduced in filename:" + each)
	

EmptyLineRemover()
DuplicateRedundancyRemover()