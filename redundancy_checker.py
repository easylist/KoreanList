import os 
from os import listdir
from os.path import isfile, join
from collections import OrderedDict

# on windows
#pathDelimeter = "\\"
# on mac
pathDelimeter = "/"

MYPATH = os.getcwd() + pathDelimeter + "KoreanList"
onlyfiles = [f for f in listdir(MYPATH) if isfile(join(MYPATH, f))]

def f7(seq):
    seen = set()
    seen_add = seen.add
    return [x for x in seq if not (x in seen or seen_add(x))]

def EmptyLineRemover():
	EmptyLines= 0
	for each in onlyfiles:
		new_temp= []
		target_file= MYPATH+ pathDelimeter +each
		#target_file= MYPATH+"\\"+each
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
		target_file= MYPATH+pathDelimeter +each
		name, ext = os.path.splitext(each)

		if(ext == ".txt"):
			f = open(target_file,"r")
			lines = f.readlines()
			f.close()

			lines_wo_rn = []
			for line in lines:
				lines_wo_rn.append(line.replace('\n', '').replace('\r', ''))

			RedundancedList= f7(lines_wo_rn)

			f = open(target_file,"w")
			for line in RedundancedList:
				f.write(line + "\n")
			f.close()

		print(str(len(lines_wo_rn) - len(RedundancedList)) + " duplicated lines are reduced in filename:" + each)
	

EmptyLineRemover()
DuplicateRedundancyRemover()