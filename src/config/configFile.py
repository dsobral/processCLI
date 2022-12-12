'''
Created on Oct 12, 2016

@author: mmp
'''

import os, sys, re, glob
from os import listdir
from constants.utils import Util
from os.path import isfile, join
from datetime import datetime

class ConfigFile(object):
	'''
	classdocs
	'''
	SGE_OUT_SCRIPT_DIR = "qsub"

	CONFIG_FILE_header_dir_file_name = "InputDirectories"
	CONFIG_FILE_processors = "processors="
	CONFIG_FILE_output_path = "output_path="
	CONFIG_FILE_extension_1 = "extension_1="
	CONFIG_FILE_extension_2 = "extension_2="
	CONFIG_FILE_confirm_after_collect_data = "confirm_after_collect_data="
	CONFIG_FILE_LOG="log_file="
	CONFIG_FILE_cmd= "cmd="
	CONFIG_FILE_cmd_one_file= "cmd_one_file="
	CONFIG_FILE_cmd_two_files= "cmd_two_files="
	CONFIG_FILE_expecting_all_paired_files = "expecting_all_paired_files="
	CONFIG_FILE_fast_processing = "fast_processing="	##   no wait for 
	CONFIG_FILE_clean_file_name_to_get_sample_name = "clean_file_name_to_get_sample_name="	## clean sample file name to get the sample name
	CONFIG_FILE_queue_name = "queue_name="				##	 If name of queue exist set all on SGE
	CONFIG_FILE_sge_cores_requested = "SGE_cores_requested="	##	 Cores requested to run in SGE

	VARIABLE_NAMES_FILE1 = "FILE1"
	VARIABLE_NAMES_FILE1_CHANGED = "FILE1_CHANGED"
	VARIABLE_NAMES_FILE2 = "FILE2"
	VARIABLE_NAMES_FILE2_CHANGED = "FILE2_CHANGED"
	VARIABLE_NAMES_PREFIX_FILES_OUT = "PREFIX_FILES_OUT"
	VARIABLE_NAMES_OUT_FOLDER = "OUT_FOLDER"
	VARIABLE_TEMPORARY = "TEMPORARY_"
	VARIABLE_INDEX_PROCESS = "INDEX_PROCESS"
	

	def __init__(self):
		'''
		Constructor
		'''
		self.processors = 1					## number of processors
		self.output_path = ""
		self.log_file = ""					## log output file
		self.vect_files_to_process = []		## files to process
		self.vec_cmds = []					## can use several commands; run always if they have one or two files
		self.vec_cmds_one_file = []			## can use several commands; run only when exist one fasta/fastq file
		self.vec_cmds_two_files = []		## can use several commands; run only when exist two fasta/fastq files
		self.extension_to_look_1 = ""			## extension to look
		self.extension_to_look_2 = ""			## extension to look
		self.queue_name = ""				## If name of queue exist set all on SGE
		self.sge_cores_requested = 1		## Cores requested for SGE
		self.confirm_after_collect_data = True
		self.expecting_all_paired_files = True
		self.clean_file_name_to_get_sample_name = True
		self.fast_processing = False		## if the trigger to check the cmd will be fast
											## True if the cmd are fast to run
		self.util = Util()
		## print "Error: the file '" + file_name + "' doesn't have order number. Must be like <prefix>_r<number>_<extension>"
		self.vect_files_not_to_process = []
		
		## default extensions to look
		self.VECT_FILE_EXTENSIONS = [".fq.gz", ".fq", ".fastq.gz", ".fastq", ".fasta.gz",
					".fasta", ".fa", ".fa.gz"]
		
	### get several parameters
	def get_processors(self): return self.processors
	def get_output_path(self): return self.output_path
	def get_log_file_name(self): return self.log_file
	def get_vect_cmd(self): return self.vec_cmds
	def get_vect_cmd_one_file(self): return self.vec_cmds_one_file
	def get_vect_cmd_two_files(self): return self.vec_cmds_two_files
	def get_confirm_after_collect_data(self): return self.confirm_after_collect_data

	def get_vect_files_not_to_process(self): return self.vect_files_not_to_process
	def get_len_vect_files_not_to_process(self): return len(self.vect_files_not_to_process)
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
		
		index_file_to_process = 0
		b_start_dir_file_description = False
		vect_directories_to_look = []
		with open(file_name) as handle:
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
	
				### test fast_processing has other value
				if (sz_temp.lower().find(self.CONFIG_FILE_fast_processing.lower()) >= 0):
					try:
						self.fast_processing = not self.util.is_false(line.strip()[sz_temp.find(self.CONFIG_FILE_fast_processing.lower()) + len(self.CONFIG_FILE_fast_processing):].split()[0])
					except ValueError:
						raise ValueError("The fast_processing must have an boolean value")
					continue
	
				## log output file
				if (sz_temp.lower().find(self.CONFIG_FILE_LOG.lower()) >= 0):
					self.log_file = line.strip()[sz_temp.find(self.CONFIG_FILE_LOG.lower()) + len(self.CONFIG_FILE_LOG):].split()[0]
					continue
	
				## out_path
				if (sz_temp.lower().find(self.CONFIG_FILE_output_path.lower()) >= 0):
					self.output_path = line.strip()[sz_temp.find(self.CONFIG_FILE_output_path.lower()) + len(self.CONFIG_FILE_output_path):].split()[0]
					continue
				
				## clean_file_name_to_get_sample_name
				if (sz_temp.lower().find(self.CONFIG_FILE_clean_file_name_to_get_sample_name.lower()) >= 0):
					try:
						self.clean_file_name_to_get_sample_name = not self.util.is_false(line.strip()[sz_temp.find(self.CONFIG_FILE_clean_file_name_to_get_sample_name.lower()) +\
										len(self.CONFIG_FILE_clean_file_name_to_get_sample_name):].split()[0])
					except ValueError:
						raise ValueError("The clean_file_name_to_get_sample_name must have an boolean value")
					continue
				
				## queue_name
				if (sz_temp.lower().find(self.CONFIG_FILE_queue_name.lower()) >= 0):
					self.queue_name = line.strip()[sz_temp.find(self.CONFIG_FILE_queue_name.lower()) + len(self.CONFIG_FILE_queue_name):].split()[0]
					continue
				
				## SGE cores requested
				if (sz_temp.lower().find(self.CONFIG_FILE_sge_cores_requested.lower()) >= 0):
					try:
						self.sge_cores_requested = int(line.strip()[sz_temp.find(self.CONFIG_FILE_sge_cores_requested.lower()) + len(self.CONFIG_FILE_sge_cores_requested):].split()[0])
					except ValueError:
						raise ValueError("The sge_cores_requested must have an integer value")
					if (self.sge_cores_requested < 2): self.sge_cores_requested = 1
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
						if (self.util.is_false(sz_temp)): self.confirm_after_collect_data = False
					continue
				
				## expecting_all_paired_files
				if (sz_temp.lower().find(self.CONFIG_FILE_expecting_all_paired_files.lower()) >= 0):
					if (len(line.strip()[sz_temp.find(self.CONFIG_FILE_expecting_all_paired_files.lower()) + len(self.CONFIG_FILE_expecting_all_paired_files):]) > 0):
						sz_temp = line.strip()[sz_temp.find(self.CONFIG_FILE_expecting_all_paired_files.lower()) + len(self.CONFIG_FILE_expecting_all_paired_files):].split()[0].lower()
						if (self.util.is_false(sz_temp)): self.expecting_all_paired_files = False
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
		
		vect_index_empty = []
		if (not self.has_all_pair_files() and self.expecting_all_paired_files):
			n_index = 0
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
		if (not b_start_dir_file_description): raise Exception("Must have the '{}' tag followed by directories that contain files".format(ConfigFile.CONFIG_FILE_header_dir_file_name))
		if (len(self.vect_files_to_process) == 0):
			if (self.expecting_all_paired_files and len(vect_index_empty) > 0):
				raise Exception("You have files but you have the flag '{}' yes. Please, check if you expect paired files.".format(ConfigFile.CONFIG_FILE_expecting_all_paired_files))
			raise Exception("Must have files to process. Insert directories after the tag '{}' in the config file".format(ConfigFile.CONFIG_FILE_header_dir_file_name))

		## set log file on output folder
		if (len(self.log_file) > 0):
			self.log_file =  os.path.join(self.output_path, self.log_file)
		
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
		dir_file_to_files = lstData[0]
		if (dir_file_to_files.split('/')[-1].find("*") != -1):
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
			only_file_name = os.path.basename(file_name)		## get only the name
			if (not self.__ends_with_extension(only_file_name)):
				self.vect_files_not_to_process.append(file_name)
				continue
			try:
				self.util.get_number_file(file_name)
			except Exception:
				### try to get the prefix file name
				prefix_file_name = self.get_prefix_file_name(only_file_name)
				if (len(prefix_file_name) > 0 and self.__ends_with_extension(only_file_name)):
					dict_join_files[prefix_file_name] = [file_name.replace(sz_line_to_parse, '', 1)]
				else:
					self.vect_files_not_to_process.append(file_name)
				continue

			prefix_file_name = self.get_prefix_file_name(only_file_name)
			if (prefix_file_name in dict_join_files):
				if (self.remove_extensions_file_name(only_file_name) in dict_out_normalized_files): raise Exception("Error: the file '" + only_file_name + "' exist more than on time in the directory, or in sub-directories '" + dir_file_to_files + "'")
				dict_join_files[prefix_file_name].append(file_name.replace(sz_line_to_parse, '', 1))
				dict_out_normalized_files[self.remove_extensions_file_name(only_file_name)] = 1
			else: 
				dict_join_files[prefix_file_name] = [file_name.replace(sz_line_to_parse, '', 1)]
				
				### small caveat
				if (len(self.extension_to_look_1) == 0): dict_out_normalized_files[self.remove_extensions_file_name(only_file_name)] = 1


		### create lines by 
		for key_dir in dict_join_files:
			vect_files_result.append(FileToProcess(dir_file_to_files + "/" + dict_join_files[key_dir][0],\
										dir_file_to_files + "/" + dict_join_files[key_dir][1] if len(dict_join_files[key_dir]) > 1 else "",\
										key_dir, index_file_to_process, self.extension_to_look_1 , self.extension_to_look_2, dir_file_to_files))
			index_file_to_process += 1
		return (vect_files_result, index_file_to_process)

	def is_sge(self):
		"""
		test if is going to run a sge qconf
		"""
		return len(self.queue_name) > 0


	def get_prefix_file_name(self, file_name):
		
		## not clean file name to get sample name. Only remove extension from file name
		if not self.clean_file_name_to_get_sample_name:
			return self.remove_extensions_file_name(file_name)
		
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
		
		m = re.search('[a-zA-Z0-9_\.]+(_[rR]\d)[_][a-zA-Z0-9_\.]+', file_name)
		if (not m is None): return file_name[:m.regs[1][0]]
		
		m = re.search('[a-zA-Z0-9_\.]+(_\d+)[\.][a-zA-Z0-9_\.]+', file_name)
		if (not m is None): return file_name[:m.regs[1][0]]
		
		m = re.search('[a-zA-Z0-9_\.]+(_\d+)[_\.][a-zA-Z0-9_\.]+', file_name)
		if (not m is None): return file_name[:m.regs[1][0]]
		
		m = re.search('[a-zA-Z0-9_\.]+(_\d+)[_][a-zA-Z0-9_\.]+', file_name)
		if (not m is None): return file_name[:m.regs[1][0]]
		
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
				if (prefix_file_name in dict_out_normalized_files): raise Exception("Error: the file '" + file_name + "' exist more than on time in the directory, or in sub-directories '" + dir_file_to_files + "'")
				dict_out_normalized_files[prefix_file_name] = 1
			else: 
				dict_join_files[prefix_file_name] = [file_name]

				### small caveat
				if (len(self.extension_to_look_1) == 0): dict_out_normalized_files[self.remove_extensions_file_name(file_name)] = 1

		### create lines by 
		for key_dir in dict_join_files:
			vect_files_result.append(FileToProcess(os.path.join(dir_file_to_files, dict_join_files[key_dir][0]), 
										os.path.join(dir_file_to_files, dict_join_files[key_dir][1]) if len(dict_join_files[key_dir]) > 1 else "", 
										key_dir, index_file_to_process, self.extension_to_look_1 , self.extension_to_look_2, False, dir_file_to_files))
			index_file_to_process += 1
		return (vect_files_result, index_file_to_process)

	def remove_extensions_file_name(self, file_name):
		if (len(self.extension_to_look_1) > 0 and file_name.endswith(self.extension_to_look_1)): return file_name[:len(file_name) - len(self.extension_to_look_1)]
		if (len(self.extension_to_look_2) > 0 and file_name.endswith(self.extension_to_look_2)): return file_name[:len(file_name) - len(self.extension_to_look_2)]
		if (len(self.extension_to_look_1) > 0 or len(self.extension_to_look_2) > 0): return file_name
		
		for to_search in self.VECT_FILE_EXTENSIONS:
			if (file_name.endswith(to_search)):
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
				self.VECT_FILE_EXTENSIONS.append(self.extension_to_look_2)
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
		print( "Fast processing: " + str(self.fast_processing))
		
		print("Command lines to process:")
		for vect_to_run in self.get_vect_cmd_to_run():
			for command_ in vect_to_run:
				print( "\t$ " + command_)
			print("#######################")
		
		if self.is_sge():
			print("\tImportant:\n\tAll commands will be submitted to SGE queue management...\n")
		print("\tTotal to run: " + str(len(self.vect_files_to_process)))
		print
		if (self.get_len_vect_files_not_to_process() > 0):
			print( "\tFiles were not recognized as valid:")
			for _, file_name in enumerate(self.vect_files_not_to_process):
				print("\t" + file_name)
				if _ >= 9: 
					print("\t....... more '{}' files but not show.\nAll files on log file '{}'".format(
						int(self.get_len_vect_files_not_to_process()) - 10, self.log_file))
					break
			print("\tTotal: " + str(self.get_len_vect_files_not_to_process()))
			print("END - files were not recognized as valid.")
			print
	
	def get_files_not_to_run(self):
		"""
		return files not to run message
		"""
		sz_message = "Next files were not recognized as valid.\n"
		for _, file_name in enumerate(self.vect_files_not_to_process):
			sz_message += "\t" + file_name + "\n"
		sz_message += "\tTotal: " + str(self.get_len_vect_files_not_to_process()) + "\n"
		sz_message += "END - files were not recognized as valid.\n"
		return sz_message
	
	
	### return vect all command lines
	def get_vect_cmd_to_run(self):
		vect_cmd_to_process = []
		vect_index_to_remove = []
		for _, files_to_process in enumerate(self.vect_files_to_process):
			vect_command_to_run = []
			for comand in self.vec_cmds:
				vect_command_to_run.append(files_to_process.get_command_line(self.output_path, comand, _))
			
			### get commands one file only
			if (files_to_process.has_two_files()):
				### get commands two files only
				for comand in self.vec_cmds_two_files:
					vect_command_to_run.append(files_to_process.get_command_line(self.output_path, comand, _))
			else:
				for comand in self.vec_cmds_one_file:
					vect_command_to_run.append(files_to_process.get_command_line(self.output_path, comand, _))
				
			if (len(vect_command_to_run) > 0): vect_cmd_to_process.append(vect_command_to_run)
			else: vect_index_to_remove.append(_)
		
		## to remove files without cmds to process	
		vect_index_to_remove = sorted(vect_index_to_remove, reverse=True)
		for index_to_remove in vect_index_to_remove:
			self.vect_files_to_process.pop(index_to_remove)
		
		return vect_cmd_to_process
	
	def has_output_dir(self):
		"""
		Test if in commands exist OUT_FOLDER variable
		"""
		for command in self.vec_cmds:
			if (command.find(ConfigFile.VARIABLE_NAMES_OUT_FOLDER) != -1): return True
		for command in self.vec_cmds_one_file:
			if (command.find(ConfigFile.VARIABLE_NAMES_OUT_FOLDER) != -1): return True
		for command in self.vec_cmds_two_files:
			if (command.find(ConfigFile.VARIABLE_NAMES_OUT_FOLDER) != -1): return True
		return False
	
	def write_log_start_process(self):
		"""
		write the start of tasks
		"""
		if (len(self.log_file) > 0):
			self.util.make_path(os.path.dirname(self.log_file))
			with open(self.log_file, 'a') as handle_out:
				handle_out.write("\n###############################\n###############################\n"+\
					"It is going to process {} tasks -> {}\n".format(len(self.vect_files_to_process), str(datetime.now())))

	def write_log_finish_process(self, sz_message = "Everything is finished"):
		"""
		write the start of tasks
		"""
		if (len(self.log_file) > 0):
			with open(self.log_file, 'a') as handle_out:
				handle_out.write("\n###############################\n###############################\n"+\
					"{} -> {}\n".format(sz_message, str(datetime.now())))
				
	def write_log_processing_task(self, n_task):
		"""
		write the progressing of process
		"""
		if (len(self.log_file) > 0):
			with open(self.log_file, 'a') as handle_out:
				handle_out.write("####\nProcessing {}/{}  ->  {}\n".format(n_task, len(self.vect_files_to_process), str(datetime.now())))
		
	def write_log_single_message(self, message):
		if (len(self.log_file) > 0):
			with open(self.log_file, 'a') as handle_out:
				handle_out.write("####\nMessage\n{}\n{}\n".format(str(datetime.now()), message))
				
	def write_log_message(self, n_task, message):
		"""
		write the progressing of process
		"""
		if (len(self.log_file) > 0):
			with open(self.log_file, 'a') as handle_out:
				handle_out.write("####\nMessage for process {}/{}  ->  {}\n{}\n".format(n_task,
							len(self.vect_files_to_process), str(datetime.now()), message))
		
	
class FileToProcess(object):
	'''
	classdocs
	'''

	utils = Util()
	
	def __init__(self, file1, file2, out_prefix, index_file_to_process, extension_1, extension_2, dir_file_to_files):
		'''
		Constructor
		'''
		self.file1 = file1.replace('//', '/')
		self.file2 = file2.replace('//', '/')
		self.out_prefix = out_prefix[:-1] if out_prefix.endswith('.') else out_prefix ### clean file name
		self.index_file_to_process = index_file_to_process
		self.extension_1 = extension_1
		self.extension_2 = extension_2
		
		self.__set_order_files()
		
		## at the end all of them are removed
		self.dt_temp_files = {}			## holds all temporary files
		self.temp_directory = ""
		
		### remove end 
		while len(dir_file_to_files) > 0:
			if (dir_file_to_files.endswith('/')): dir_file_to_files = dir_file_to_files[:-1]
			else: break
		self.dir_file_to_files = dir_file_to_files	### has the directory of source files
		
	def __exit__(self, exc_type, exc_value, traceback):
		if (not self.temp_directory is None and len(self.temp_directory) > 0):
			self.utils.remove_dir(self.temp_directory)

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

	def _replace_file_name(self, cmd_out, variable_name, replace_string):
		"""
		replace file name
		"""
		cmd_out = cmd_out.replace(" " + variable_name + " ", ' "' + replace_string + '" ')
		cmd_out = cmd_out.replace(" " + variable_name, ' "' + replace_string + '"')	## could be in the end of the command line
		return cmd_out.replace(variable_name, replace_string)	## last chance
		
	### get command line with replaced tags	
	def get_command_line(self, output_path, cmd, index_to_process = -1):
		
		### create temp directories and files
		for word in cmd.split("'"):
			if (word.startswith(ConfigFile.VARIABLE_TEMPORARY)):
				if (word not in self.dt_temp_files):
					if (len(self.temp_directory) == 0): self.temp_directory = self.utils.get_temp_dir()
					self.dt_temp_files[word] = self.utils.get_temp_file_from_dir(self.temp_directory, "cmd", "")

		cmd_out = self._replace_file_name(cmd, ConfigFile.VARIABLE_NAMES_FILE1_CHANGED, self.get_file1_changed())
		cmd_out = self._replace_file_name(cmd_out, ConfigFile.VARIABLE_NAMES_FILE1, self.file1)
		if (len(self.file2) > 0):
			cmd_out = self._replace_file_name(cmd_out, ConfigFile.VARIABLE_NAMES_FILE2_CHANGED, self.get_file2_changed())
			cmd_out = self._replace_file_name(cmd_out, ConfigFile.VARIABLE_NAMES_FILE2, self.file2)

		cmd_out = cmd_out.replace(ConfigFile.VARIABLE_NAMES_PREFIX_FILES_OUT, self.out_prefix)
		if (index_to_process >= 0):
			cmd_out = cmd_out.replace(ConfigFile.VARIABLE_INDEX_PROCESS, str(index_to_process))
				
		### create output path if necessary
		if (cmd_out.find(ConfigFile.VARIABLE_NAMES_OUT_FOLDER) != -1):
			full_path = os.path.dirname(self.file1)
		#	print(full_path, output_path, os.getcwd(), self.dir_file_to_files)
		#	/storage/home/areis/JOANA_VIEIRA2019/smallRNA/raw_data     fastqc_beforetrim    /storage/home/areis/JOANA_VIEIRA2019/smallRNA/pre-analysis
		#	files/dir_with_files outData /home/mmp/git/processCLI/src/tests
			if (output_path.startswith('/')): full_path = self.get_path_equal(output_path, full_path)
			elif (self.dir_file_to_files.startswith('/')): 
				temp_path = full_path.replace(self.dir_file_to_files, "")
				if (temp_path.startswith('/')): temp_path = temp_path[1:]
				full_path = os.path.join(os.getcwd(), output_path, temp_path)
			else: 
				full_path = os.path.join(os.getcwd(), output_path, "/".join( full_path.replace(os.getcwd(), '')[1:].split('/')[1:] ))
		#	print(full_path)
			cmd = "mkdir -p {}".format(full_path)
			os.system(cmd)
	
			cmd_out = cmd_out.replace(ConfigFile.VARIABLE_NAMES_OUT_FOLDER, full_path)
			
		### replace temp files
		for key in self.dt_temp_files:
			cmd_out = cmd_out.replace("'" + key + "'", self.dt_temp_files[key])
		
		cmd_out = cmd_out.replace('//', '/')	### only to clean paths
		return cmd_out

	def get_path_equal(self, output_path, full_path):
		"""
		output_path = /home/projects/pipeline_quality/fastqc_trim
		full_path = /home/projects/pipeline_quality/original_data/xpto/zpt
		return = /home/projects/pipeline_quality/fastqc_trim/xpto/zpt
		"""
		lst_out_path = output_path.split('/')
		lst_full_path = full_path.split('/')
		vect_return_path = []
		b_equal_begin = True
		for i in range(len(lst_full_path)):
			if (b_equal_begin and lst_full_path[i] == lst_out_path[i]): 
				vect_return_path.append(lst_full_path[i])
				continue
			else:
				if (b_equal_begin):		## first time different
					vect_return_path.append(lst_out_path[i])
				else: vect_return_path.append(lst_full_path[i])
				b_equal_begin = False
		return "/".join(vect_return_path)






