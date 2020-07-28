import os
from multiprocessing import Process

from os import listdir
from os.path import isfile, join

input_path = "../input/2018_7.2/"
#input_path = "input/2020_7.4/"


def arrange_files(input_path):
	"""
	Read a direcrtory and organize files to start reading in order
	"""

	# Create an empty object to allocate the files
	files_path = []
	_files_path = [[], []]

	# Loop over each sensor folder name
	for f in listdir(input_path):
		# Add that path to each sensor folder
		sensor_path = join(input_path,f)
		onlyfiles = [s for s in listdir(sensor_path) if isfile(join(sensor_path, s))]
		fpath = [sensor_path + "/" + f for f in onlyfiles]

		if len(fpath) == 1:
			files_path.append(fpath)
		elif len(fpath) == 2:
			_files_path[0].append(fpath[0])
			_files_path[1].append(fpath[1])

	if len(files_path) == 0:
		files_path = _files_path

	# Flattenig the list
	input_files = [val for sublist in files_path for val in sublist]

	return input_files


def f(name):
	command = 'python '+name+' &'
	print(command)
	os.system(command)


if __name__ == '__main__':
	# Read the directory and get all file names
	input_files = arrange_files(input_path)

	# Loop over the file names
	for file_name in input_files:
		print(file_name)
		# Run each input with sensor simulator
		p = Process(target=f, args=('sensor_simulator.py ' + file_name,))
		p.start()
