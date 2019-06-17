'''
Created on Oct 23, 2016

@author: mmp
'''

import os, random, pickle, gzip, re

class Util(object):
	'''
	classdocs
	'''
	EXTENSION_ZIP = ".gz"
	TEMP_DIRECTORY = "/tmp"
	PROCESS_CLI_TEMP_DIRECTORY = "processCLI"
	
	def __init__(self):
		'''
		Constructor
		'''
		pass

	def is_integer(self, sz_value):
		try:
			int(sz_value)
			return True
		except ValueError:
			return False
		
	def get_temp_file(self, file_name, sz_type):
		main_path = os.path.join(self.TEMP_DIRECTORY, self.PROCESS_CLI_TEMP_DIRECTORY)
		if (not os.path.exists(main_path)): os.makedirs(main_path)
		while 1:
			return_file = os.path.join(main_path, "process_cli_" + file_name + "_" + str(random.randrange(10000000, 99999999, 10)) + "_file" + sz_type)
			if (os.path.exists(return_file)): continue
			try:
				os.close(os.open(return_file, os.O_CREAT | os.O_EXCL))
				return return_file
			except FileExistsError:
				pass
	
	def get_temp_file_from_dir(self, dir_out, file_name, sz_type):
		"""
		return a temp file name
		"""
		if (not os.path.exists(dir_out)): os.makedirs(dir_out)
		while 1:
			return_file = os.path.join(dir_out, "process_cli_" + file_name + "_" + str(random.randrange(10000000, 99999999, 10)) + "_file" + sz_type)
			if (os.path.exists(return_file)): continue
			try:
				os.close(os.open(return_file, os.O_CREAT | os.O_EXCL))
				return return_file
			except FileExistsError:
				pass
	
	def get_temp_dir(self):
		"""
		return a temp directory
		"""
		main_path = os.path.join(self.TEMP_DIRECTORY, self.PROCESS_CLI_TEMP_DIRECTORY)
		if (not os.path.exists(main_path)): os.makedirs(main_path)
		while 1:
			return_path = os.path.join(main_path, "process_cli_" + str(random.randrange(10000000, 99999999, 10)))
			if (not os.path.exists(return_path)):
				os.makedirs(return_path)
				return return_path
					
	def remove_temp_file(self, sz_file_name):
		if os.path.exists(sz_file_name) and len(sz_file_name) > 0 and sz_file_name.find(self.TEMP_DIRECTORY) == 0:
			cmd = "rm " + sz_file_name
			os.system(cmd)

	def remove_dir(self, path_name):
		if (not path_name is None):
			cmd = "rm -r %s*" % (path_name); os.system(cmd)
			
	def copy_file(self, path_origin, path_destination):
		if os.path.exists(path_origin):
			cmd = "cp " + path_origin + " " + path_destination
			os.system(cmd)

	def write_class(self, sz_file_name, class_to_write, b_zip):
		if (b_zip): output = gzip.open(sz_file_name + self.EXTENSION_ZIP, 'wb')
		else: output = open(sz_file_name, 'wb')
		### write a file...
		pickle.dump(class_to_write, output)
		output.close()


	def read_class(self, sz_file_name, sz_old_class_name = "", sz_new_class_name = ""):
		b_zip = False
		if (not os.path.exists(sz_file_name)):
			## try the gzip file
			if (os.path.exists(sz_file_name + self.EXTENSION_ZIP)): 
				b_zip = True
				sz_file_name = sz_file_name + self.EXTENSION_ZIP
			else: raise Exception("Error: file not exist to read the class")
		
		if (b_zip): output = gzip.open(sz_file_name, 'rb')
		else: output = open(sz_file_name, 'rb')
		class_to_return = pickle.load(output)
		output.close()
		if (b_zip): os.unlink(sz_file_name)
		return class_to_return

	def get_number_file(self, file_name):
		m = re.search('[a-zA-Z0-9_\.]+_([rR]\d+)[_\.][a-zA-Z0-9_\.]+', file_name)
		if (not m is None and self.is_integer(file_name[m.regs[1][0] + 1:m.regs[1][1]])): return int(file_name[m.regs[1][0] + 1:m.regs[1][1]])
		m = re.search('[a-zA-Z0-9_\.]+_(\d+[pP])[_\.][a-zA-Z0-9_\.]+', file_name)
		if (not m is None and self.is_integer(file_name[m.regs[1][0]:m.regs[1][1] - 1])): return int(file_name[m.regs[1][0]:m.regs[1][1] -1])
		m = re.search('[a-zA-Z0-9_\.]+_(\d+)[\.][a-zA-Z0-9_\.]+', file_name)
		if (not m is None and self.is_integer(file_name[m.regs[1][0]:m.regs[1][1]])): return int(file_name[m.regs[1][0]:m.regs[1][1]]) 
		raise Exception("Error can't find the number of the file '" + file_name + "'")


	def is_false(self, sz_temp):
		sz_temp = sz_temp.lower()
		return sz_temp == "false" or sz_temp == "f" or sz_temp == "0" or sz_temp == "no"


