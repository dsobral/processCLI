'''
Created on Oct 12, 2016

@author: mmp
'''

import os, sys, re, glob
from os import listdir
from constants.utils import Util
from os.path import isfile, join

class ConfigFile(object):
	'''
	classdocs
	'''

	CONFIG_FILE_header_dir_file_name = "InputDirectories"
	CONFIG_FILE_processors = "processors="
	CONFIG_FILE_output_path = "output_path="
	CONFIG_FILE_extension_1 = "extension_1="
	CONFIG_FILE_extension_2 = "extension_2="
	CONFIG_FILE_confirm_after_collect_data = "confirm_after_collect_data="
	CONFIG_FILE_cmd= "cmd="
	CONFIG_FILE_cmd_one_file= "cmd_one_file="
	CONFIG_FILE_cmd_two_files= "cmd_two_files="
	CONFIG_FILE_expecting_all_paired_files = "expecting_all_paired_files="
	CONFIG_EXTENTION_TO_LOOK = "extension="

	VARIABLE_NAMES_FILE1 = "FILE1"
	VARIABLE_NAMES_FILE1_CHANGED = "FILE1_CHANGED"
	VARIABLE_NAMES_FILE2 = "FILE2"
	VARIABLE_NAMES_FILE2_CHANGED = "FILE2_CHANGED"
	VARIABLE_NAMES_PREFIX_FILES_OUT = "PREFIX_FILES_OUT"
	VARIABLE_NAMES_OUT_FOLDER = "OUT_FOLDER"
	

	def __init__(self):
		'''
		Constructor
		'''
		self.processors = 1					## number of processors
		self.output_path = ""
		self.vect_files_to_process = []		## files to process
		self.vec_cmds = []					## can use several commands; run always if they have one or two files
		self.vec_cmds_one_file = []			## can use several commands; run only when exist one fasta/fastq file
		self.vec_cmds_two_files = []		## can use several commands; run only when exist two fasta/fastq files
		self.extension_to_look_1 = ""			## extension to look
		self.extension_to_look_2 = ""			## extension to look
		self.confirm_after_collect_data = True
		self.expecting_all_paired_files = True
		self.util = Util()
		## print "Error: the file '" + file_name + "' doesn't have order number. Must be like <prefix>_r<number>_<extension>"
		self.vect_files_not_to_process = []
		
		## default extensions to look
		self.VECT_FILE_EXTENSIONS = [".fq.gz", ".fq", ".fastq.gz", ".fastq", ".fasta.gz", ".fasta"]
		
	### get several parameters
	def get_processors(self): return self.processors
	def get_output_path(self): return self.output_path
	def get_vect_cmd(self): return self.vec_cmds
	def get_vect_cmd_one_file(self): return self.vec_cmds_one_file
	def get_vect_cmd_two_files(self): return self.vec_cmds_two_files
	def get_confirm_after_collect_data(self): return self.confirm_after_collect_data

	def get_vect_files_not_to_process(self): return self.vect_files_not_to_process
	def clean_vect_files_not_to_process(self): self.vect_files_not_to_process = []
	def get_vect_files_to_process(self): return self.vect_files_to_process
	def has_all_pair_files(self):
		if (len(self.vect_files_to_process) == 0): return False
		for file_to_process in self.vect_files_to_process:
			if (len(file_to_process.get_file1()) == 0 or len(file_to_process.get_file2()) == 0): return False
		return True
	
	def read_file(self, file_name):
		'''
		read the config files
		'''
		
		### test file name
		if (not os.path.exists(file_name)):
			sys.exit("Error: config file doesn't exist '" + file_name + "'")
		
		handle = open(file_name)
		index_file_to_process = 0
		b_start_dir_file_description = False
		vect_directories_to_look = []
		for line in handle:
			sz_temp = line.strip().lower()
			if (len(sz_temp) == 0 or sz_temp[0] == '#'): continue

			## processors
			if (sz_temp.lower().find(self.CONFIG_FILE_processors.lower()) >= 0):
				try:
					self.processors = int(line.strip()[sz_temp.find(self.CONFIG_FILE_processors.lower()) + len(self.CONFIG_FILE_processors):].split()[0])
				except ValueError:
					raise ValueError("The processors must have an integer value")
				if (self.processors < 1): self.processors = 1
				continue

			## out_path
			if (sz_temp.lower().find(self.CONFIG_FILE_output_path.lower()) >= 0):
				self.output_path = line.strip()[sz_temp.find(self.CONFIG_FILE_output_path.lower()) + len(self.CONFIG_FILE_output_path):].split()[0]
				continue
			
			## extension_1
			if (sz_temp.lower().find(self.CONFIG_FILE_extension_1.lower()) >= 0):
				if (len(line.strip()[sz_temp.find(self.CONFIG_FILE_extension_1.lower()) + len(self.CONFIG_FILE_extension_1):]) > 0):
					self.extension_to_look_1 = line.strip()[sz_temp.find(self.CONFIG_FILE_extension_1.lower()) + len(self.CONFIG_FILE_extension_1):].split()[0]
				continue

			## extension_2
			if (sz_temp.lower().find(self.CONFIG_FILE_extension_2.lower()) >= 0):
				if (len(line.strip()[sz_temp.find(self.CONFIG_FILE_extension_2.lower()) + len(self.CONFIG_FILE_extension_2):]) > 0):
					self.extension_to_look_2 = line.strip()[sz_temp.find(self.CONFIG_FILE_extension_2.lower()) + len(self.CONFIG_FILE_extension_2):].split()[0]
				continue
			
			## confirm_after_collect_data
			if (sz_temp.lower().find(self.CONFIG_FILE_confirm_after_collect_data.lower()) >= 0):
				if (len(line.strip()[sz_temp.find(self.CONFIG_FILE_confirm_after_collect_data.lower()) + len(self.CONFIG_FILE_confirm_after_collect_data):]) > 0):
					sz_temp = line.strip()[sz_temp.find(self.CONFIG_FILE_confirm_after_collect_data.lower()) + len(self.CONFIG_FILE_confirm_after_collect_data):].split()[0].lower()
					if (sz_temp == "false" or sz_temp == "f" or sz_temp == "0"): self.confirm_after_collect_data = False
				continue
			
			## expecting_all_paired_files
			if (sz_temp.lower().find(self.CONFIG_FILE_expecting_all_paired_files.lower()) >= 0):
				if (len(line.strip()[sz_temp.find(self.CONFIG_FILE_expecting_all_paired_files.lower()) + len(self.CONFIG_FILE_expecting_all_paired_files):]) > 0):
					sz_temp = line.strip()[sz_temp.find(self.CONFIG_FILE_expecting_all_paired_files.lower()) + len(self.CONFIG_FILE_expecting_all_paired_files):].split()[0].lower()
					if (sz_temp == "false" or sz_temp == "f" or sz_temp == "0"): self.expecting_all_paired_files = False
				continue

			## out_global_report
			if (sz_temp.lower().find(self.CONFIG_FILE_cmd.lower()) == 0):
				self.vec_cmds.append(line.strip()[sz_temp.find(self.CONFIG_FILE_cmd.lower()) + len(self.CONFIG_FILE_cmd):])
				continue
			## out_global_report
			if (sz_temp.lower().find(self.CONFIG_FILE_cmd_one_file.lower()) == 0):
				self.vec_cmds_one_file.append(line.strip()[sz_temp.find(self.CONFIG_FILE_cmd_one_file.lower()) + len(self.CONFIG_FILE_cmd_one_file):])
				continue
			## out_global_report
			if (sz_temp.lower().find(self.CONFIG_FILE_cmd_two_files.lower()) == 0):
				self.vec_cmds_two_files.append(line.strip()[sz_temp.find(self.CONFIG_FILE_cmd_two_files.lower()) + len(self.CONFIG_FILE_cmd_two_files):])
				continue

			if (self.CONFIG_FILE_header_dir_file_name.lower().replace("\t", "").replace(" ", "") == sz_temp.lower().replace("\t", "").replace(" ", "")):
				b_start_dir_file_description = True
				continue

			if (b_start_dir_file_description):
				vect_directories_to_look.append(line.strip())
				(vect_file_to_process, index_file_to_process) = self.__get_files_to_process_from_directory__(line.strip(), index_file_to_process)
				self.vect_files_to_process.extend(vect_file_to_process)
		handle.close()
		
		if (not self.has_all_pair_files() and self.expecting_all_paired_files):
			n_index = 0
			vect_index_empty = []
			for file_to_process in self.vect_files_to_process:
				if (len(file_to_process.get_file1()) == 0 or len(file_to_process.get_file2()) == 0):
					self.vect_files_not_to_process.append(file_to_process.get_file_name())
					vect_index_empty.append(n_index)
				n_index += 1
		
			if (len(vect_index_empty) > 0):
				vect_index_empty.reverse()
				for n_index in vect_index_empty: self.vect_files_to_process.pop(n_index)
		
		self.__test_empty_patameter__(self.output_path, "Output Path")
		if ((len(self.vec_cmds) + len(self.vec_cmds_one_file) + len(self.vec_cmds_two_files)) == 0): 
			raise Exception("Error: the value 'Command line to process cmd=' can't be empty")
		if (not b_start_dir_file_description): raise Exception("Must have the 'InputDirectory' tag followed by directories that contain files")
		if (len(self.vect_files_to_process) == 0): 
			raise Exception("Must have files to process. Insert directories after the tag 'InputDirectory' in the config file")

	def __test_empty_patameter__(self, sz_value, sz_error):
		if (len(sz_value) == 0): raise Exception("Error: the value '" + sz_error + "' can't be empty")

	def __ends_with_extension(self, prefix_file_name):
		"""
		Test if the file ends with a specific extension
		"""
		if (len(self.extension_to_look_1) > 0 or len(self.extension_to_look_2) > 0):
			if (len(self.extension_to_look_1) > 0 and prefix_file_name.endswith(self.extension_to_look_1)): return True
			if (len(self.extension_to_look_2) > 0 and prefix_file_name.endswith(self.extension_to_look_2)): return True
		else:
			for extension in self.VECT_FILE_EXTENSIONS:
				if (prefix_file_name.endswith(extension)): return True
		return False
	
	def __get_files_to_process_from_directory__(self, sz_line_to_parse, index_file_to_process):
		"""
		get files from a directory
		###   files/dir_with_files_file_fail
		"""
		sz_line_to_parse = os.path.expandvars(sz_line_to_parse)
		lstData = sz_line_to_parse.split()
		dir_file_to_files_with_wild_char = ""
		dir_file_to_files = lstData[0]
		if (dir_file_to_files.split('/')[-1].find("*") != -1):
			dir_file_to_files_with_wild_char = dir_file_to_files
			if (len(dir_file_to_files.split('/')) == 1): dir_file_to_files = "."
			else: dir_file_to_files = "/".join(dir_file_to_files.split('/')[:-1])
		if (not os.path.exists(dir_file_to_files)):
			raise Exception("Error: this directory doesn't exist: " + dir_file_to_files)
		
		## test directory
		if (dir_file_to_files is None or len(dir_file_to_files) == 0):
			raise Exception("Error, there's no directory to parse in this line: " + sz_line_to_parse)

		### get files by prefix		
		vect_files_result = []
		dict_join_files = {}
		dict_out_normalized_files = {}
#		vect_files_to_read = glob.glob(dir_file_to_files_with_wild_char, recursive=True) if len(dir_file_to_files_with_wild_char) > 0 else  [f for f in listdir(dir_file_to_files) if isfile(join(dir_file_to_files, f))]
		vect_files_to_read = [os.path.join(dp, f) for dp, dn, filenames in os.walk(dir_file_to_files) for f in filenames]
		for file_name in vect_files_to_read:
			if (not self.__ends_with_extension(file_name.split('/')[-1])):
				self.vect_files_not_to_process.append(file_name)
				continue
			try:
				self.util.get_number_file(file_name)
			except Exception:
				### try to get the prefix file name
				prefix_file_name = self.get_prefix_file_name(file_name.split('/')[-1])
				if (len(prefix_file_name) > 0 and self.__ends_with_extension(file_name.split('/')[-1])):
					dict_join_files[prefix_file_name] = [file_name.replace(sz_line_to_parse, '')]
				else:
					self.vect_files_not_to_process.append(file_name)
				continue

			only_file_name = file_name.split('/')[-1]		## get only the name
			prefix_file_name = self.get_prefix_file_name(only_file_name)
			if (prefix_file_name in dict_join_files):
				if (self.remove_extensions_file_name(only_file_name) in dict_out_normalized_files): raise Exception("Error: the file '" + only_file_name + "' exist more than on time in the directory '" + dir_file_to_files + "'")
				dict_join_files[prefix_file_name].append(file_name.replace(sz_line_to_parse, ''))
				dict_out_normalized_files[self.remove_extensions_file_name(only_file_name)] = 1
			else: dict_join_files[prefix_file_name] = [file_name.replace(sz_line_to_parse, '')]

		### create lines by 
		for key_dir in dict_join_files:
			vect_files_result.append(FileToProcess(dir_file_to_files + "/" + dict_join_files[key_dir][0],\
										dir_file_to_files + "/" + dict_join_files[key_dir][1] if len(dict_join_files[key_dir]) > 1 else "",\
										key_dir, index_file_to_process, self.extension_to_look_1 , self.extension_to_look_2))
			index_file_to_process += 1
		return (vect_files_result, index_file_to_process)


	def get_prefix_file_name(self, file_name):
		## if has only one extension only looks for one file, not the pairs
		if (len(self.extension_to_look_1) > 0 and len(self.extension_to_look_2) == 0): return self.remove_extensions_file_name(file_name)
		
		m = re.search('[a-zA-Z0-9_\.]+(_[lL]\d+_[rR]\d+_\d+)_[a-zA-Z0-9_\.]+', file_name)
		if (not m is None): return file_name[:m.regs[1][0]]
		
		m = re.search('[a-zA-Z0-9_\.]+(_[lL]\d+_[rR]\d+)[a-zA-Z0-9_\.]+', file_name)
		if (not m is None): return file_name[:m.regs[1][0]]
		
		m = re.search('[a-zA-Z0-9_\.]+(_\d+[pP])[a-zA-Z0-9_\.]+', file_name)
		if (not m is None): return file_name[:m.regs[1][0]]

# 		m = re.search('[a-zA-Z0-9_\.]+(_[lL]\d+)[a-zA-Z0-9_\.]+', file_name)
# 		if (not m is None): return file_name[:m.regs[1][0]]
		
		m = re.search('[a-zA-Z0-9_\.]+(_[rR]\d+)[a-zA-Z0-9_\.]+', file_name)
		if (not m is None): return file_name[:m.regs[1][0]]
		
		return self.remove_extensions_file_name(file_name)


	def __get_files_to_process_from_directory_without_pair__(self, sz_line_to_parse, index_file_to_process):
		"""
		get files from a directory without pairs
		###   files/dir_with_files_file_fail
		"""
		sz_line_to_parse = os.path.expandvars(sz_line_to_parse)
		lstData = sz_line_to_parse.split()
		dir_file_to_files_with_wild_char = ""
		dir_file_to_files = lstData[0]
		if (dir_file_to_files.split('/')[-1].find("*") != -1):
			dir_file_to_files_with_wild_char = dir_file_to_files
			if (len(dir_file_to_files.split('/')) == 1): dir_file_to_files = "."
			else: dir_file_to_files = "/".join(dir_file_to_files.split('/')[:-1])
		if (not os.path.exists(dir_file_to_files)):
			raise Exception("Error: this directory doesn't exist: " + dir_file_to_files)
		
		## test directory
		if (dir_file_to_files is None or len(dir_file_to_files) == 0):
			raise Exception("Error, there's no directory to parse in this line: " + sz_line_to_parse)

		### get files by prefix		
		vect_files_result = []
		dict_join_files = {}
		dict_out_normalized_files = {}
		vect_files_to_read = glob.iglob(dir_file_to_files_with_wild_char) if len(dir_file_to_files_with_wild_char) > 0 else  [f for f in listdir(dir_file_to_files) if isfile(join(dir_file_to_files, f))]
		for file_name in vect_files_to_read:
			file_name = file_name.split('/')[-1]		## gt only the name
			if (not self.has_extension_file_name(file_name)):
				self.vect_files_not_to_process.append(file_name)
				continue
			
			prefix_file_name = self.remove_extensions_file_name(file_name)
			if (prefix_file_name in dict_join_files):
				if (prefix_file_name in dict_out_normalized_files): raise Exception("Error: the file '" + file_name + "' exist more than on time in the directory '" + dir_file_to_files + "'")
				dict_out_normalized_files[prefix_file_name] = 1
			else: dict_join_files[prefix_file_name] = [file_name]

		### create lines by 
		for key_dir in dict_join_files:
			vect_files_result.append(FileToProcess(os.path.join(dir_file_to_files, dict_join_files[key_dir][0]), 
										os.path.join(dir_file_to_files, dict_join_files[key_dir][1]) if len(dict_join_files[key_dir]) > 1 else "", 
										key_dir, index_file_to_process, self.extension_to_look_1 , self.extension_to_look_2, False))
			index_file_to_process += 1
		return (vect_files_result, index_file_to_process)

	def remove_extensions_file_name(self, file_name):
		if (len(self.extension_to_look_1) > 0 and file_name.find(self.extension_to_look_1) == len(file_name) - len(self.extension_to_look_1)): return file_name[:len(file_name) - len(self.extension_to_look_1)]
		if (len(self.extension_to_look_2) > 0 and file_name.find(self.extension_to_look_2) == len(file_name) - len(self.extension_to_look_2)): return file_name[:len(file_name) - len(self.extension_to_look_2)]
		if (len(self.extension_to_look_1) > 0 or len(self.extension_to_look_2) > 0): return file_name
		
		for to_search in self.VECT_FILE_EXTENSIONS:
			if (file_name.find(to_search) == len(file_name) - len(to_search)):
				return file_name[:len(file_name) - len(to_search)]
		return file_name

	def has_extension_file_name(self, file_name):
		if (len(self.extension_to_look_1) > 0 or len(self.extension_to_look_2) > 0):
			if (len(self.extension_to_look_1) > 0 and file_name.find(self.extension_to_look_1) == len(file_name) - len(self.extension_to_look_1)): return True
			if (len(self.extension_to_look_2) > 0 and file_name.find(self.extension_to_look_2) == len(file_name) - len(self.extension_to_look_2)): return True
			return False
		
		for to_search in self.VECT_FILE_EXTENSIONS:
			if (file_name.find(to_search) == len(file_name) - len(to_search)):
				return True
		return False
	
	def get_extensions_to_look(self):
		if (len(self.extension_to_look_1) > 0 or len(self.extension_to_look_2) > 0):
			if(len(self.extension_to_look_1) > 0): self.VECT_FILE_EXTENSIONS = [self.extension_to_look_1]
			if(len(self.extension_to_look_2) > 0 and self.extension_to_look_2 not in self.VECT_FILE_EXTENSIONS):
				self.VECT_FILE_EXTENSIONS = [self.extension_to_look_1]
		return '; '.join(self.VECT_FILE_EXTENSIONS)
	
	def get_repeated_files_names(self):
		"""
		return repeated files
		"""
		vect_files_out = []
		vect_files_repeated = []
		for file_to_process in self.vect_files_to_process:
			for file_name in file_to_process.get_vect_input_file():
				file_name_temp = "%s_%s_%s" % (file_name.split('/')[-1], file_to_process.get_box1(), file_to_process.get_box2()) 
				if file_name_temp in vect_files_out: vect_files_repeated.append(file_name)
				else:  vect_files_out.append(file_name_temp)
		return vect_files_repeated

	
	def print_command_lines_to_run(self):
		print
		print( "File extensions searched: " + self.get_extensions_to_look())
		
		print("Command lines to process:")
		for files_to_process in self.vect_files_to_process:
			for command_ in self.get_vect_cmd():
				print( "\t$ " + files_to_process.get_command_line(self.output_path, command_))
			print
			
		print("\tTotal to run: " + str(len(self.vect_files_to_process)))
		print
		if (len(self.vect_files_not_to_process) > 0):
			print( "Next files were not recognize as valid.")
			for file_name in self.vect_files_not_to_process:
				print("\t" + file_name)
			print("\tTotal: " + str(len(self.vect_files_not_to_process)))
			print("END - files were not recognize as valid.")
			print
	
	### return vect all command lines
	def get_vect_cmd_to_run(self):
		vect_cmd_to_process = []
		for files_to_process in self.vect_files_to_process:
			vect_command_to_run = []
			for comand in self.vec_cmds:
				vect_command_to_run.append(files_to_process.get_command_line(self.output_path, comand))
			
			### get commands one file only
			for comand in self.vec_cmds_one_file:
				vect_command_to_run.append(files_to_process.get_command_line(self.output_path, comand))
			
			### get commands two files only
			for comand in self.vec_cmds_two_files:
				if (files_to_process.has_two_files()):
					vect_command_to_run.append(files_to_process.get_command_line(self.output_path, comand))
			if (len(vect_command_to_run) > 0): vect_cmd_to_process.append(vect_command_to_run)
		return vect_cmd_to_process
	

		
			
class FileToProcess(object):
	'''
	classdocs
	'''


	def __init__(self, file1, file2, out_prefix, index_file_to_process, extension_1, extension_2):
		'''
		Constructor
		'''
		self.file1 = file1.replace('//', '/')
		self.file2 = file2.replace('//', '/')
		self.out_prefix = out_prefix		### clean file name
		self.index_file_to_process = index_file_to_process
		self.extension_1 = extension_1
		self.extension_2 = extension_2
		
		self.__set_order_files()

	#### get parameters		
	def get_file1(self): return self.file1
	def get_file2(self): return self.file2
	def get_file1_changed(self): return self.__get_change_name(self.file1)
	def get_file2_changed(self): return self.__get_change_name(self.file2)
	def get_prefix_file_out(self): return self.out_prefix
	def get_index_file_to_process(self): return self.index_file_to_process
	def get_file_name(self):
		if (len(self.file1) > 0): return self.file1
		if (len(self.file2) > 0): return self.file2
		return ""
	
	def __get_change_name(self, file_name):
		"""
		change name of the file for the name of the previous directory name
		ex: sds/second/xpoy.fasta.gz -> sds/second/second.fasta.gz
		"""
		lst_data = file_name.split('/')
		if (len(lst_data) > 1):
			return "/".join(lst_data[:-2]) + "/" + lst_data[-2] + "/" + lst_data[-1].replace(self.out_prefix, lst_data[-2])
		return file_name
		
		
	def has_two_files(self):
		if (len(self.file1) > 0 and len(self.file2) > 0): return True
		return False

	### has always one file
	def __set_order_files(self):
# 		if (len(self.extension_1) > 0 and len(self.extension_2) > 0):
# 			if (self.file1.find(self.extension_1) != len(self.file1) - len(self.extension_1)):
# 				temp = self.file1
# 				self.file1 = self.file2
# 				self.file2 = temp
# 		else:
		util = Util()
		if (len(self.file1) == 0): 
			self.file1 = self.file2
			self.file2 = ""
		if (len(self.file2) == 0): return
		if (util.get_number_file(self.file1) > util.get_number_file(self.file2)):
			temp = self.file1
			self.file1 = self.file2
			self.file2 = temp

	VARIABLE_NAMES_FILE1 = "FILE1"
	VARIABLE_NAMES_FILE2 = "FILE2"
	VARIABLE_NAMES_PREFIX_FILES_OUT = "PREFIX_FILES_OUT"
	VARIABLE_NAMES_OUT_FOLDER = "OUT_FOLDER"
		
	### get command line with replaced tags	
	def get_command_line(self, output_path, cmd):
		cmd_out = cmd.replace(ConfigFile.VARIABLE_NAMES_FILE1_CHANGED, self.get_file1_changed())
		cmd_out = cmd_out.replace(ConfigFile.VARIABLE_NAMES_FILE1, self.file1)
		if (len(self.file2) > 0): 
			cmd_out = cmd_out.replace(ConfigFile.VARIABLE_NAMES_FILE2_CHANGED, self.get_file1_changed())
			cmd_out = cmd_out.replace(ConfigFile.VARIABLE_NAMES_FILE2, self.file2)

		cmd_out = cmd_out.replace(ConfigFile.VARIABLE_NAMES_PREFIX_FILES_OUT, self.out_prefix)
				
		### create output path
		full_path = os.path.dirname(self.file1)
		full_path = os.path.join(os.getcwd(), output_path, "/".join(full_path.replace(os.getcwd(), '')[1:].split('/')[1:]))
		cmd = "mkdir -p {}".format(full_path)
		os.system(cmd)

		cmd_out = cmd_out.replace(ConfigFile.VARIABLE_NAMES_OUT_FOLDER, full_path)
		return cmd_out








