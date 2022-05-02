#!/usr/bin/env python3

import time, os, sys
from optparse import OptionParser
from config.configFile import ConfigFile
from constants.utils import Util
from constants.process_SGE import ProcessSGE

__version__ = "3.2"

class ProcessCLI(object):

	util = Util()
	
	def __init__(self, b_degub):
		self.config_file = ConfigFile()
		self.vect_files_processed = []
		self.vect_manage_process = []
		self.b_degub = b_degub

	def __search_end_process__(self):
		#test all process in the list
		for i in range(self.config_file.get_processors()):
			if (self.vect_manage_process[i] != -1 and self.vect_manage_process[i] != 111010001):
				# print "find Process %d" % (self.vect_manage_process[i])
				(p, v) = os.waitpid(self.vect_manage_process[i], os.WNOHANG)
				if (p != 0): self.vect_manage_process[i] = -1 # process already finish
	#END searchEndProcess				

	def __is_all_end__(self):
		nCount = 0 
		self.__search_end_process__()
		for nProcess in self.vect_manage_process:
			if (nProcess == -1): nCount += 1
		if (nCount == self.config_file.get_processors()): return True
		return False
	#END isAllEnd


	def __get_pos_process__(self):
		while 1:
			self.__search_end_process__()
			for i in range(self.config_file.get_processors()):
				if (self.vect_manage_process[i] == -1 and self.vect_manage_process[i] != 111010001):
					self.vect_manage_process[i] = 111010001	#put some data to prevent to others alloc in the same spot
					return i
			time.sleep(0.1 if self.config_file.fast_processing else 10)
		return -1
	#END getPosProcess


	###
	def process_config_file(self, config_file_name):
		
		## read config file
		self.config_file.read_file(config_file_name)
		
		### test output path
		if (self.config_file.has_output_dir()):
			if (not self.b_degub and os.path.exists(self.config_file.get_output_path())):
				sz_value = input("The output directory '" + self.config_file.get_output_path() + "' exist.\nDo you want proceed [y|n]?")
				if (sz_value == " "): sys.exit(0)
				if (sz_value != 'y' and sz_value != 'Y'): sys.exit(0)
		
		### print all information to run...
		self.config_file.print_command_lines_to_run()
		if (self.config_file.get_confirm_after_collect_data()):
			sz_value = input("Do you want to proceed [y|n]: ")
			if (sz_value == " "): sys.exit(0)
			if (sz_value != 'y' and sz_value != 'Y'): sys.exit(0)
		
		### create the directory if necessary
		if (self.config_file.has_output_dir()):
			if not os.path.exists(self.config_file.get_output_path()): os.makedirs(self.config_file.get_output_path())
		
			### copy config file to persist
			self.util.copy_file(config_file_name, os.path.join(self.config_file.get_output_path(), config_file_name.split('/')[-1]))
		
		self.config_file.write_log_start_process()
		### write message, files not to run
		if (self.config_file.get_len_vect_files_not_to_process() > 0):
			self.config_file.write_log_single_message(self.config_file.get_files_not_to_run())
				
		if self.config_file.is_sge():	### sge
			
			process_sge = ProcessSGE()
			
			cmd = "mkdir -p " + ConfigFile.SGE_OUT_SCRIPT_DIR
			exit_status = os.system(cmd)
			if (exit_status != 0):
				### don't kill with exit status different than zero, because some command lines, exit with different than zero in success 
				print("Exit_status {}, Cmd: {}".format(exit_status, cmd))
			
			### for each sample
			jobs_submitted, jobs_not_submitted = (0, 0)
			path_save_job = os.path.join(os.getcwd(), ConfigFile.SGE_OUT_SCRIPT_DIR) 
			for vect_cmd_to_run in self.config_file.get_vect_cmd_to_run():
				
				### set a sge submit
				qsub_file = self.util.get_file_by_progress(ConfigFile.SGE_OUT_SCRIPT_DIR, "sge_to_submit", ".sh")
				process_sge.set_script_run_sge(path_save_job, 
									self.config_file.queue_name, self.config_file.sge_cores_requested, 
									vect_cmd_to_run, qsub_file)
				try:
					sge_id = process_sge.submitte_job(qsub_file)
					self.config_file.write_log_finish_process("Job submitted:\n{}".format(vect_cmd_to_run))
					
					sz_message = "Submit job with id: {}   scriptJob: {}".format(sge_id, qsub_file)
					self.config_file.write_log_single_message(sz_message)
					print(sz_message)
					jobs_submitted += 1
				except Exception as e:
					print(str(e))
					sz_message = "Job not submitted"
					self.config_file.write_log_single_message(sz_message)
					print(sz_message)
					jobs_not_submitted += 1
			
			### 	
			sz_message = "Jobs submitted: {}    jobs not submitted: {}".format(jobs_submitted, jobs_not_submitted)
			self.config_file.write_log_single_message(sz_message)
			
			### write the log that everythinf is finished
			self.config_file.write_log_finish_process("All jobs submitted")
			
			print("\nAll SGE scripts are in {}".format(path_save_job))
			print("You can check all your jobs running with:\n$ qstat -f\n")
		else:	### threading...
			### threads			
			self.vect_manage_process = self.config_file.get_processors() * [-1]	# list to the process available
															
			## for each file 
			n_count_task = 1
			for vect_cmd_to_run in self.config_file.get_vect_cmd_to_run():
				n_pos_vect = self.__get_pos_process__()	# get a new position to a process, otherwise wait till have a slot available
				self.config_file.write_log_processing_task(n_count_task)
				n_count_task += 1
				if (n_pos_vect == -1):
					raise Exception("Error getting a process ID %s"  % time.ctime())
	
				new_ID = os.fork()
				if new_ID < 0:
					raise Exception("Error forking the main process, time: %s"  % time.ctime())
				elif new_ID == 0: # is the child
					for cmd_to_run in vect_cmd_to_run:
						print("Command line: " + cmd_to_run)
						exit_status = os.system(cmd_to_run)
						if (exit_status != 0):
							### don't kill with exit status different than zero, because some command lines, exit with different than zero in success 
							print("Exit_status {}".format(exit_status))
							if (not cmd_to_run.startswith('grep')):
								self.config_file.write_log_message(n_count_task, "Error: this command line failed - {}".format(cmd_to_run))
								sys.exit(0)
					sys.exit(0)
				else: self.vect_manage_process[n_pos_vect] = new_ID # it is the present but the ID is from the child
				
			########
			# waiting till the end
			while 1:
				if self.config_file.fast_processing: time.sleep(1)
				else: time.sleep(1 if self.b_degub else 10)
				if (self.__is_all_end__()): break
		
			### write the log that everythinf is finished
			self.config_file.write_log_finish_process()
		
		### read all exit status...
		print("Finished...")


if __name__ == '__main__':

	"""
	V3.2 release 28/4/2022
		FIX - replace variables without double quote
	V3.1 release 15/2/2022
		Add - SGE cores requested
	V3.0 release 3/5/2021
		Add - SGE option 
	V2.2 release 04/05/2018
		Add - progress report 
	V2.1 release 24/04/2018
		Add - several fixes 
	V2.0 release 16/04/2018
		Add - add cmd_one_file, cmd_two_files and add a possibility of change files 
	V1.9 release 29/03/2018
		Add - other way to process the 'cmd'
	V1.8 release 3/10/2017
		Add - it is possible to put environment variables in the InputDirectories paths
	"""
	
	b_debug = False
	if (b_debug):
		input_config_file = "tests/files/config_to_run_2.txt"
		input_config_file = "tests/files/config_temp_files.txt"
		input_config_file = "/home/projects/pipeline_quality/config_to_run_pair.txt"
	else:
		parser = OptionParser(usage="%prog [-h] [-i]", version="%prog " + __version__, add_help_option=False)
		parser.add_option("-i", "--input", type="string", dest="input", help="Input file with all configurations.\nPlease check the 'config.txt' files inside of 'example_config' directory ", metavar="IN_FILE")
		parser.add_option('-h', '--help', dest='help', action='store_true', help='show this help message and exit')
	
		(options, args) = parser.parse_args()
		
		if (options.help):
			parser.print_help()
			print("\nexample: processCLI -i config.txt")
			print
			print("""
			TAGs that can be in config file:
			1)  TAG processors=  -> Process commands in parallel, only Threading mode;
			2)  TAG output_path=  -> global path where the data is going to be saved;
			3)  TAG extension_1=  -> extensions of files to look;
			4)  TAG extension_2=  -> extensions of files to look;
			5)  TAG confirm_after_collect_data=  -> Set True to human confirmation after collecting all the data;
			6)  TAG log_file=  		-> log file name;
			7)  TAG cmd=  			-> commands to run, can be more than one;
			8)  TAG expecting_all_paired_files=  -> True if all fastq.gz files are paired 
			9)  TAG fast_processing=  -> Set this to True if call commands fasted in Threading mode, decrease time between calls;
			10) TAG queue_name=  ->Set queue name if you want to submit the commands to SGE;
			11) TAG SGE_threads= ->Set number of cores requested for SGE, default is 1. Activate SGE tag #$ -pe smp <cores requested>"
			
			Variables:
			1)	FILE1					-> reads_R1.fastq.gz/reads_R1.fastq/reads_R1.fasta.gz/reads_R1.fasta 
			2)	FILE2					-> reads_R2.fastq.gz/reads_R2.fastq/reads_R2.fasta.gz/reads_R2.fasta

			1)	FILE1_CHANGED			-> GSE96700_GSM2538511/reads_R1.fastq.gz  ->  GSE96700_GSM2538511/GSE96700_GSM2538511_R1.fastq.gz 
			2)	FILE2_CHANGED			-> GSE96700_GSM2538511/reads_R2.fastq.gz  ->  GSE96700_GSM2538511/GSE96700_GSM2538511_R2.fastq.gz

			OR		If not identify any _R1.<extension> in directory start looking for files ended with (fastq.gz, fastq, fasta.gz or fasta) 

			1)  FILE1					-> reads.fastq.gz/reads.fastq/reads.fasta.gz/reads.fasta

			3)	PREFIX_FILES_OUT		-> reads
			4)	OUT_FOLDER				-> outData/reads/....

			5) TEMP variables			-> you can create temporary files as you want.
										-> only need to start with "TEMPORARY_" word. It is going to create a file where the data is going to be saved. 
										-> and at the end it's is going to be remove automatically.
										-> Ex: TEMPORARY_a, TEMPORARY_b, TEMPORARY_c
			6) INDEX_PROCESS			-> Number of set of pair of files/file to process

			""")
			sys.exit(0)
			
		if (len(args) != 0):
			parser.error("incorrect number of arguments")
	
		if not options.input:   # 
			parser.error('Configuration file is not specified')
	
	processCLI = ProcessCLI(b_debug)
	
	if (b_debug): processCLI.process_config_file(input_config_file)
	else: processCLI.process_config_file(options.input)




