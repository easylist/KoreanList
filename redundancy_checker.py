import os 
from os import listdir
from os.path import isfile, join

mypath = os.getcwd() + "\\KoreanList"
onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]

for each in onlyfiles:
	new_temp= []
	target_file= mypath+"\\"+each
	name, ext = os.path.splitext(each)

	if(ext == ".txt"):
		f = open(target_file,"r")
		lines = f.readlines()
		f.close()

		for line in lines:
			if line == "\n":
				continue
			else:
				new_temp.append(line)

		f = open(target_file,"w")
		for line in new_temp:
			f.write(line)
		f.close()