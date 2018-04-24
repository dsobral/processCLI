'''
Created on Oct 14, 2016

@author: mmp
'''
import unittest, os
from config.configFile import ConfigFile

class Test(unittest.TestCase):


	def setUp(self):
		pass


	def tearDown(self):
		pass


	def testFile(self):
		
		configFile = ConfigFile()
		configFile.read_file("files/config.txt")
			
		self.assertTrue(configFile.get_processors() == 2)
		self.assertTrue(configFile.get_output_path() == "outData")
		self.assertTrue(len(configFile.get_vect_cmd()) == 1)
		self.assertFalse(configFile.get_confirm_after_collect_data())
		self.assertEqual(configFile.get_vect_cmd()[0], "bash tests/cmd/process.sh OUT_FOLDER PREFIX_FILES_OUT FILE1 FILE2")
		self.assertEqual(len(configFile.get_vect_files_not_to_process()), 1)
		self.assertEqual(configFile.get_vect_files_not_to_process()[0], "files/dir_with_files/Xpto2_A_L001_r1.fastq.gz")
		self.assertEqual(len(configFile.get_vect_files_to_process()), 3)
		
		n_count = 0
		for files_to_process in configFile.get_vect_files_to_process():
			if (files_to_process.get_prefix_file_out() == "Xpto3_A"):
				n_count += 1
				self.assertEqual(files_to_process.get_file1(), "files/dir_with_files/Xpto3_A_L001_r1.fastq.gz")
				self.assertEqual(files_to_process.get_file2(), "files/dir_with_files/Xpto3_A_L001_r2.fastq")
				self.assertEqual(files_to_process.get_command_line(configFile.get_output_path(), configFile.get_vect_cmd()[0]), 
						'bash tests/cmd/process.sh /home/mmp/eclipse_oxygen/processCLI/src/tests/outData/dir_with_files '\
						'Xpto3_A "files/dir_with_files/Xpto3_A_L001_r1.fastq.gz" "files/dir_with_files/Xpto3_A_L001_r2.fastq"')
			if (files_to_process.get_prefix_file_out() == "Xpto_A"):
				n_count += 1
				self.assertEqual(files_to_process.get_file1(), "files/dir_with_files/Xpto_A_L001_r1.fastq.gz")
				self.assertEqual(files_to_process.get_file2(), "files/dir_with_files/Xpto_A_L001_r2.fastq.gz")
		self.assertEquals(n_count, 2)


	
	def testFile_5(self):
		configFile = ConfigFile()
		configFile.read_file("files/config5.txt")
			
		self.assertTrue(configFile.get_processors() == 2)
		self.assertTrue(configFile.get_output_path() == "outData")
		self.assertTrue(len(configFile.get_vect_cmd()) == 1)
		self.assertFalse(configFile.get_confirm_after_collect_data())
		self.assertEqual(configFile.get_vect_cmd()[0], "bash tests/cmd/process.sh OUT_FOLDER PREFIX_FILES_OUT FILE1 FILE2")
		self.assertEqual(len(configFile.get_vect_files_not_to_process()), 0)
		self.assertEqual(len(configFile.get_vect_files_to_process()), 1)
		
		self.assertEqual(configFile.get_vect_files_to_process()[0].get_prefix_file_out(), "Xpto3_A_L001")
		self.assertEqual(configFile.get_vect_files_to_process()[0].get_file1(), "files/dir_with_files_9/Xpto3_A_L001_1.fastq")
		self.assertEqual(configFile.get_vect_files_to_process()[0].get_file2(), "files/dir_with_files_9/Xpto3_A_L001_2.fastq")
		self.assertEqual(configFile.get_vect_files_to_process()[0].get_command_line(configFile.get_output_path(), configFile.get_vect_cmd()[0]), 
					'bash tests/cmd/process.sh /home/mmp/eclipse_oxygen/processCLI/src/tests/outData/dir_with_files_9 '\
					'Xpto3_A_L001 "files/dir_with_files_9/Xpto3_A_L001_1.fastq" "files/dir_with_files_9/Xpto3_A_L001_2.fastq"')
		
	def testFile1(self):
		configFile = ConfigFile()
		try:
			configFile.read_file("files/config2_fail.txt")
		except Exception as e:
			self.assertEqual(e.args[0], "Error: the value 'Output Path' can't be empty")
			return
		self.fail("Must raise an error")
			
	def testFile2(self):
		configFile = ConfigFile()
		try:
			configFile.read_file("files/config3_fail.txt")
		except Exception as e:
			self.assertEqual(e.args[0], "Error: the value 'Command line to process cmd=' can't be empty")
			return
		self.fail("Must raise an ValueError exception on processors")
				
	def testFile3(self):
		configFile = ConfigFile()
		try:
			configFile.read_file("files/config4_fail.txt")
		except Exception as e:
			self.assertEqual(e.args[0], "Must have the 'InputDirectory' tag followed by directories that contain files")
			return
		self.fail("Must raise an Exception with InputDirectory")
				
	def testFile4(self):
		configFile = ConfigFile()
		try:
			configFile.read_file("files/config5_fail.txt")
		except Exception as e:
			self.assertEqual(e.args[0], "Must have files to process. Insert directories after the tag 'InputDirectory' in the config file")
			return
		self.fail("Must raise an Exception on files to process")
	
	def testFile5(self):
		configFile = ConfigFile()
		try:
			configFile.read_file("files/config6_fail.txt")
	
		except Exception as e:
			self.assertEqual(e.args[0], "Error: this directory doesn't exist: files/dir_with_files_fail_xpto")
			return
		self.fail("Must raise an ValueError on errors")	
	
	def testFile6(self):
		configFile = ConfigFile()
		try:
			configFile.read_file("files/config7_fail.txt")
		except Exception as e:
			self.assertEqual(e.args[0], "Error: the file 'Xpto3_A_L001_r2.fastq' exist more than on time in the directory 'files/dir_with_files_fail'")
			return
		self.fail("Must raise an error")
	
	def testFile7(self):
		configFile = ConfigFile()
		configFile.read_file("files/config8_fail.txt")
		self.assertEqual(len(configFile.get_vect_files_not_to_process()), 1)
		self.assertEqual(configFile.get_vect_files_not_to_process()[0], "files/dir_with_files_fail_2/file.fastq")
			
	def testFile8(self):
		configFile = ConfigFile()
		configFile.read_file("files/config9.txt")
		self.assertEqual(len(configFile.get_vect_files_not_to_process()), 1)
		self.assertEqual(configFile.get_vect_files_not_to_process()[0], "files/dir_with_files_1/Xpto2_A.txt")
		self.assertTrue(configFile.get_confirm_after_collect_data())
		self.assertEqual(len(configFile.get_vect_files_to_process()), 4)
		n_count = 0
		for files_to_process in configFile.get_vect_files_to_process():
			if (files_to_process.get_prefix_file_out() == "Treponema_A_L001"):
				n_count += 1
				self.assertEqual(files_to_process.get_file1(), "files/dir_with_files_1/Treponema_A_L001.fastq.gz")
				self.assertEqual(files_to_process.get_file2(), "")
			elif (files_to_process.get_prefix_file_out() == "Xpto_A_L001"):
				n_count += 1
				self.assertEqual(files_to_process.get_file1(), "files/dir_with_files_1/Xpto_A_L001.fastq.gz")
				self.assertEqual(files_to_process.get_file2(), "")
			elif (files_to_process.get_prefix_file_out() == "Xpto_B"):
				n_count += 1
				self.assertEqual(files_to_process.get_file1(), "files/dir_with_files_1/Xpto_B.fastq")
				self.assertEqual(files_to_process.get_file2(), "")
			elif (files_to_process.get_prefix_file_out() == "Xpto2_A"):
				n_count += 1
				self.assertEqual(files_to_process.get_file1(), "files/dir_with_files_1/Xpto2_A.fastq.gz")
				self.assertEqual(files_to_process.get_file2(), "")
		self.assertEquals(n_count, 4)

	def testFile9(self):
		configFile = ConfigFile()
		configFile.read_file("files/config2.txt")
		self.assertEqual(len(configFile.get_vect_files_not_to_process()), 1)
		self.assertEqual(configFile.get_vect_files_not_to_process()[0], "files/dir_with_files_2/Xpto2_A.txt")
		self.assertEqual(len(configFile.get_vect_files_to_process()), 2)
		if (configFile.get_vect_files_to_process()[1].get_prefix_file_out() == "Xpto_B"):
			self.assertEqual(configFile.get_vect_files_to_process()[1].get_file1(), "files/dir_with_files_2/Xpto_B.fastq")
			self.assertEqual(configFile.get_vect_files_to_process()[1].get_file2(), "")
			self.assertEqual(configFile.get_vect_files_to_process()[0].get_file1(), "files/dir_with_files_2/Xpto2_A.fastq.gz")
			self.assertEqual(configFile.get_vect_files_to_process()[0].get_file2(), "")
		else:
			self.assertEqual(configFile.get_vect_files_to_process()[0].get_file1(), "files/dir_with_files_2/Xpto_B.fastq")
			self.assertEqual(configFile.get_vect_files_to_process()[0].get_file2(), "")
			self.assertEqual(configFile.get_vect_files_to_process()[1].get_file1(), "files/dir_with_files_2/Xpto2_A.fastq.gz")
			self.assertEqual(configFile.get_vect_files_to_process()[1].get_file2(), "")

	def testFile10(self):
		configFile = ConfigFile()
		configFile.read_file("files/config3.txt")
		self.assertEqual(len(configFile.get_vect_files_not_to_process()), 1)
		self.assertEqual(configFile.get_vect_files_not_to_process()[0], "files/dir_with_files_2/Xpto2_A.txt")
		self.assertEqual(len(configFile.get_vect_files_to_process()), 2)
		if (configFile.get_vect_files_to_process()[0].get_prefix_file_out() == "Xpto_B"):
			self.assertEqual(configFile.get_vect_files_to_process()[0].get_file1(), "files/dir_with_files_2/Xpto_B.fastq")
			self.assertEqual(configFile.get_vect_files_to_process()[0].get_file2(), "")
			self.assertEqual(configFile.get_vect_files_to_process()[1].get_file1(), "files/dir_with_files_2/Xpto2_A.fastq.gz")
			self.assertEqual(configFile.get_vect_files_to_process()[1].get_file2(), "")
		else:
			self.assertEqual(configFile.get_vect_files_to_process()[1].get_file1(), "files/dir_with_files_2/Xpto_B.fastq")
			self.assertEqual(configFile.get_vect_files_to_process()[1].get_file2(), "")
			self.assertEqual(configFile.get_vect_files_to_process()[0].get_file1(), "files/dir_with_files_2/Xpto2_A.fastq.gz")
			self.assertEqual(configFile.get_vect_files_to_process()[0].get_file2(), "")
		self.assertEqual(configFile.get_extensions_to_look(), ".fq.gz; .fq; .fastq.gz; .fastq; .fasta.gz; .fasta")
		
	def testFile11(self):
		configFile = ConfigFile()
		try:
			configFile.read_file("files/config4.txt")
		except Exception as e:
			self.assertEqual(e.args[0], "Must have files to process. Insert directories after the tag 'InputDirectory' in the config file")
			return
		self.fail("Must raise an error")
	
	def testFile12(self):
		configFile = ConfigFile()
		configFile.read_file("files/config10.txt")
		self.assertEqual(len(configFile.get_vect_files_not_to_process()), 1)
		self.assertEqual(len(configFile.get_vect_files_to_process()), 1)
		self.assertEqual(configFile.get_vect_files_to_process()[0].get_file1(), "files/dir_with_files_4/Xpto3_A_L001_1P.fastq")
		self.assertEqual(configFile.get_vect_files_to_process()[0].get_file2(), "files/dir_with_files_4/Xpto3_A_L001_2P.fastq")
		self.assertEqual(configFile.get_extensions_to_look(), ".fq.gz; .fq; .fastq.gz; .fastq; .fasta.gz; .fasta")
		
	def testFile12_11(self):
		configFile = ConfigFile()
		configFile.read_file("files/config11.txt")
		self.assertEqual(len(configFile.get_vect_files_not_to_process()), 1)
		self.assertEqual(configFile.get_vect_files_not_to_process()[0], "files/dir_with_files_6/temp2.txt")
		self.assertEqual(len(configFile.get_vect_files_to_process()), 2)
		if (configFile.get_vect_files_to_process()[0].get_prefix_file_out() == "Xpto3_A_L001"):
			self.assertEqual(configFile.get_vect_files_to_process()[0].get_file1(), "files/dir_with_files_6/Xpto3_A_L001_1P.fastq")
			self.assertEqual(configFile.get_vect_files_to_process()[0].get_file2(), "files/dir_with_files_6/Xpto3_A_L001_2P.fastq")
			self.assertEqual(configFile.get_vect_files_to_process()[0].get_prefix_file_out(), "Xpto3_A_L001")
			self.assertEqual(configFile.get_vect_files_to_process()[1].get_file1(), "files/dir_with_files_6/Xpto31_A_L001_1P.fastq")
			self.assertEqual(configFile.get_vect_files_to_process()[1].get_file2(), "files/dir_with_files_6/Xpto31_A_L001_2P.fastq")
			self.assertEqual(configFile.get_vect_files_to_process()[1].get_prefix_file_out(), "Xpto31_A_L001")
		else:
			self.assertEqual(configFile.get_vect_files_to_process()[1].get_file1(), "files/dir_with_files_6/Xpto3_A_L001_1P.fastq")
			self.assertEqual(configFile.get_vect_files_to_process()[1].get_file2(), "files/dir_with_files_6/Xpto3_A_L001_2P.fastq")
			self.assertEqual(configFile.get_vect_files_to_process()[1].get_prefix_file_out(), "Xpto3_A_L001")
			self.assertEqual(configFile.get_vect_files_to_process()[0].get_file1(), "files/dir_with_files_6/Xpto31_A_L001_1P.fastq")
			self.assertEqual(configFile.get_vect_files_to_process()[0].get_file2(), "files/dir_with_files_6/Xpto31_A_L001_2P.fastq")
			self.assertEqual(configFile.get_vect_files_to_process()[0].get_prefix_file_out(), "Xpto31_A_L001")
			
	def testFile12_12(self):
		configFile = ConfigFile()
		configFile.read_file("files/config12.txt")
		self.assertEqual(len(configFile.get_vect_files_not_to_process()), 2)
		self.assertEqual(configFile.get_vect_files_not_to_process()[0], "files/dir_with_files_5/Xpto3_A_L001_2P.fastq")
		self.assertEqual(configFile.get_vect_files_not_to_process()[1], "files/dir_with_files_5/Xpto3_A_L001_1P.fastq")
		self.assertEqual(len(configFile.get_vect_files_to_process()), 1)
		self.assertEqual(configFile.get_vect_files_to_process()[0].get_file1(), "files/dir_with_files_5/temp2.txt")
		self.assertEqual(configFile.get_vect_files_to_process()[0].get_file2(), "")
		self.assertEqual(configFile.get_vect_files_to_process()[0].get_prefix_file_out(), "temp2")
		self.assertEqual(configFile.get_extensions_to_look(), ".txt")

	def testFile12_13(self):
		configFile = ConfigFile()
		configFile.read_file("files/config13.txt")
		self.assertEqual(len(configFile.get_vect_files_not_to_process()), 2)
		self.assertEqual(configFile.get_vect_files_not_to_process()[0], "files/dir_with_files_7/temp2.txt")
		self.assertEqual(configFile.get_vect_files_not_to_process()[1], "files/dir_with_files_7/Xpto32_A_L001_2P.fastq")
		self.assertEqual(len(configFile.get_vect_files_to_process()), 2)
		if (configFile.get_vect_files_to_process()[0].get_prefix_file_out() == "Xpto3_A_L001"):
			self.assertEqual(configFile.get_vect_files_to_process()[0].get_file1(), "files/dir_with_files_7/Xpto3_A_L001_1P.fastq")
			self.assertEqual(configFile.get_vect_files_to_process()[0].get_file2(), "files/dir_with_files_7/Xpto3_A_L001_2P.fastq")
			self.assertEqual(configFile.get_vect_files_to_process()[0].get_prefix_file_out(), "Xpto3_A_L001")
			self.assertEqual(configFile.get_vect_files_to_process()[1].get_file1(), "files/dir_with_files_7/Xpto31_A_L001_1P.fastq")
			self.assertEqual(configFile.get_vect_files_to_process()[1].get_file2(), "files/dir_with_files_7/Xpto31_A_L001_2P.fastq")
			self.assertEqual(configFile.get_vect_files_to_process()[1].get_prefix_file_out(), "Xpto31_A_L001")
		else:
			self.assertEqual(configFile.get_vect_files_to_process()[1].get_file1(), "files/dir_with_files_7/Xpto3_A_L001_1P.fastq")
			self.assertEqual(configFile.get_vect_files_to_process()[1].get_file2(), "files/dir_with_files_7/Xpto3_A_L001_2P.fastq")
			self.assertEqual(configFile.get_vect_files_to_process()[1].get_prefix_file_out(), "Xpto3_A_L001")
			self.assertEqual(configFile.get_vect_files_to_process()[0].get_file1(), "files/dir_with_files_7/Xpto31_A_L001_1P.fastq")
			self.assertEqual(configFile.get_vect_files_to_process()[0].get_file2(), "files/dir_with_files_7/Xpto31_A_L001_2P.fastq")
			self.assertEqual(configFile.get_vect_files_to_process()[0].get_prefix_file_out(), "Xpto31_A_L001")
		self.assertEqual(configFile.has_all_pair_files(), True)

	def testFile12_13_1(self):
		configFile = ConfigFile()
		configFile.read_file("files/config13_1.txt")
		self.assertEqual(len(configFile.get_vect_files_not_to_process()), 1)
		self.assertEqual(configFile.get_vect_files_not_to_process()[0], "files/dir_with_files_7/temp2.txt")
		self.assertEqual(len(configFile.get_vect_files_to_process()), 3)
		n_count = 0
		for files_to_process in configFile.get_vect_files_to_process():
			if (files_to_process.get_prefix_file_out() == "Xpto3_A_L001"):
				n_count += 1
				self.assertEqual(files_to_process.get_file1(), "files/dir_with_files_7/Xpto3_A_L001_1P.fastq")
				self.assertEqual(files_to_process.get_file2(), "files/dir_with_files_7/Xpto3_A_L001_2P.fastq")
			elif (files_to_process.get_prefix_file_out() == "Xpto31_A_L001"):
				n_count += 1
				self.assertEqual(files_to_process.get_file1(), "files/dir_with_files_7/Xpto31_A_L001_1P.fastq")
				self.assertEqual(files_to_process.get_file2(), "files/dir_with_files_7/Xpto31_A_L001_2P.fastq")
			elif (files_to_process.get_prefix_file_out() == "Xpto32_A_L001"):
				n_count += 1
				self.assertEqual(files_to_process.get_file1(), "files/dir_with_files_7/Xpto32_A_L001_2P.fastq")
				self.assertEqual(files_to_process.get_file2(), "")
		self.assertEqual(configFile.has_all_pair_files(), False)
		self.assertEqual(n_count, 3)
				
	def testFile12_14(self):
		configFile = ConfigFile()
		configFile.read_file("files/config14.txt")
		self.assertEqual(len(configFile.get_vect_files_not_to_process()), 1)
		self.assertEqual(configFile.get_vect_files_not_to_process()[0], "files/dir_with_files_6/temp2.txt")
		self.assertEqual(len(configFile.get_vect_files_to_process()), 2)
		if (configFile.get_vect_files_to_process()[0].get_prefix_file_out() == "Xpto3_A_L001"):
			self.assertEqual(configFile.get_vect_files_to_process()[0].get_file1(), "files/dir_with_files_6/Xpto3_A_L001_1P.fastq")
			self.assertEqual(configFile.get_vect_files_to_process()[0].get_file2(), "files/dir_with_files_6/Xpto3_A_L001_2P.fastq")
			self.assertEqual(configFile.get_vect_files_to_process()[0].get_prefix_file_out(), "Xpto3_A_L001")
			self.assertEqual(configFile.get_vect_files_to_process()[1].get_file1(), "files/dir_with_files_6/Xpto31_A_L001_1P.fastq")
			self.assertEqual(configFile.get_vect_files_to_process()[1].get_file2(), "files/dir_with_files_6/Xpto31_A_L001_2P.fastq")
			self.assertEqual(configFile.get_vect_files_to_process()[1].get_prefix_file_out(), "Xpto31_A_L001")
		else:
			self.assertEqual(configFile.get_vect_files_to_process()[1].get_file1(), "files/dir_with_files_6/Xpto3_A_L001_1P.fastq")
			self.assertEqual(configFile.get_vect_files_to_process()[1].get_file2(), "files/dir_with_files_6/Xpto3_A_L001_2P.fastq")
			self.assertEqual(configFile.get_vect_files_to_process()[1].get_prefix_file_out(), "Xpto3_A_L001")
			self.assertEqual(configFile.get_vect_files_to_process()[0].get_file1(), "files/dir_with_files_6/Xpto31_A_L001_1P.fastq")
			self.assertEqual(configFile.get_vect_files_to_process()[0].get_file2(), "files/dir_with_files_6/Xpto31_A_L001_2P.fastq")
			self.assertEqual(configFile.get_vect_files_to_process()[0].get_prefix_file_out(), "Xpto31_A_L001")
		self.assertEqual(configFile.has_all_pair_files(), True)
		
		
	def testFile15(self):
		configFile = ConfigFile()
		
		## set environment variable
		os.environ['dir_with_files_variable'] = "dir_with_files_8"
		
		configFile.read_file("files/config15.txt")
		self.assertEqual(len(configFile.get_vect_files_not_to_process()), 0)
		self.assertEqual(len(configFile.get_vect_files_to_process()), 2)
		if (configFile.get_vect_files_to_process()[0].get_prefix_file_out() == "Xpto3_A_L001"):
			self.assertEqual(configFile.get_vect_files_to_process()[0].get_file1(), "files/dir_with_files_8/Xpto3_A_L001_1P.fastq")
			self.assertEqual(configFile.get_vect_files_to_process()[0].get_file2(), "files/dir_with_files_8/Xpto3_A_L001_2P.fastq")
			self.assertEqual(configFile.get_vect_files_to_process()[0].get_prefix_file_out(), "Xpto3_A_L001")
			self.assertEqual(configFile.get_vect_files_to_process()[1].get_file1(), "files/dir_with_files_8/Xpto31_A_L001_1P.fastq")
			self.assertEqual(configFile.get_vect_files_to_process()[1].get_file2(), "files/dir_with_files_8/Xpto31_A_L001_2P.fastq")
			self.assertEqual(configFile.get_vect_files_to_process()[1].get_prefix_file_out(), "Xpto31_A_L001")
		else:
			self.assertEqual(configFile.get_vect_files_to_process()[1].get_file1(), "files/dir_with_files_8/Xpto3_A_L001_1P.fastq")
			self.assertEqual(configFile.get_vect_files_to_process()[1].get_file2(), "files/dir_with_files_8/Xpto3_A_L001_2P.fastq")
			self.assertEqual(configFile.get_vect_files_to_process()[1].get_prefix_file_out(), "Xpto3_A_L001")
			self.assertEqual(configFile.get_vect_files_to_process()[0].get_file1(), "files/dir_with_files_8/Xpto31_A_L001_1P.fastq")
			self.assertEqual(configFile.get_vect_files_to_process()[0].get_file2(), "files/dir_with_files_8/Xpto31_A_L001_2P.fastq")
			self.assertEqual(configFile.get_vect_files_to_process()[0].get_prefix_file_out(), "Xpto31_A_L001")
		self.assertEqual(configFile.has_all_pair_files(), True)
		
	def testFile16(self):
		configFile = ConfigFile()
		
		## set environment variable
		os.environ['dir_with_files_variable'] = "dir_with_files_8"
		
		configFile.read_file("files/config16.txt")
		self.assertEqual(len(configFile.get_vect_files_not_to_process()), 0)
		self.assertEqual(len(configFile.get_vect_files_to_process()), 2)
		if (configFile.get_vect_files_to_process()[0].get_prefix_file_out() == "Xpto3_A_L001"):
			self.assertEqual(configFile.get_vect_files_to_process()[0].get_file1(), "files/dir_with_files_8/Xpto3_A_L001_1P.fastq")
			self.assertEqual(configFile.get_vect_files_to_process()[0].get_file2(), "files/dir_with_files_8/Xpto3_A_L001_2P.fastq")
			self.assertEqual(configFile.get_vect_files_to_process()[0].get_prefix_file_out(), "Xpto3_A_L001")
			self.assertEqual(configFile.get_vect_files_to_process()[1].get_file1(), "files/dir_with_files_8/Xpto31_A_L001_1P.fastq")
			self.assertEqual(configFile.get_vect_files_to_process()[1].get_file1_changed(), "files/dir_with_files_8/dir_with_files_8_1P.fastq")
			self.assertEqual(configFile.get_vect_files_to_process()[1].get_file2(), "files/dir_with_files_8/Xpto31_A_L001_2P.fastq")
			self.assertEqual(configFile.get_vect_files_to_process()[1].get_file2_changed(), "files/dir_with_files_8/dir_with_files_8_2P.fastq")
			self.assertEqual(configFile.get_vect_files_to_process()[1].get_prefix_file_out(), "Xpto31_A_L001")
			
			self.assertEquals(len(configFile.get_vect_cmd()), 2)
			self.assertEquals(len(configFile.get_vect_cmd_one_file()), 0)
			self.assertEquals(len(configFile.get_vect_cmd_two_files()), 0)
			
			self.assertEqual(configFile.get_vect_files_to_process()[0].get_command_line(\
				configFile.get_output_path(), configFile.get_vect_cmd()[0]),\
				'bash tests/cmd/process.sh --outdir /home/mmp/eclipse_oxygen/processCLI/src/tests/outData/dir_with_files_8 --prefix Xpto3_A_L001 '\
				'--file1 "files/dir_with_files_8/Xpto3_A_L001_1P.fastq" "files/dir_with_files_8/dir_with_files_8_1P.fastq"')
		else:
			self.assertEqual(configFile.get_vect_files_to_process()[1].get_file1(), "files/dir_with_files_8/Xpto3_A_L001_1P.fastq")
			self.assertEqual(configFile.get_vect_files_to_process()[1].get_file1_changed(), "files/dir_with_files_8/dir_with_files_8_1P.fastq")
			self.assertEqual(configFile.get_vect_files_to_process()[1].get_file2(), "files/dir_with_files_8/Xpto3_A_L001_2P.fastq")
			self.assertEqual(configFile.get_vect_files_to_process()[1].get_file2_changed(), "files/dir_with_files_8/dir_with_files_8_2P.fastq")
			self.assertEqual(configFile.get_vect_files_to_process()[1].get_prefix_file_out(), "Xpto3_A_L001")
			self.assertEqual(configFile.get_vect_files_to_process()[0].get_file1(), "files/dir_with_files_8/Xpto31_A_L001_1P.fastq")
			self.assertEqual(configFile.get_vect_files_to_process()[0].get_file2(), "files/dir_with_files_8/Xpto31_A_L001_2P.fastq")
			self.assertEqual(configFile.get_vect_files_to_process()[0].get_prefix_file_out(), "Xpto31_A_L001")
			
			self.assertEquals(len(configFile.get_vect_cmd()), 2)
			self.assertEquals(len(configFile.get_vect_cmd_one_file()), 0)
			self.assertEquals(len(configFile.get_vect_cmd_two_files()), 0)
			
			self.assertEqual(configFile.get_vect_files_to_process()[0].get_command_line(\
				configFile.get_output_path(), configFile.get_vect_cmd()[0]),\
				'bash tests/cmd/process.sh --outdir /home/mmp/eclipse_oxygen/processCLI/src/tests/outData/dir_with_files_8 --prefix Xpto31_A_L001 '\
				'--file1 "files/dir_with_files_8/Xpto31_A_L001_1P.fastq" "files/dir_with_files_8/dir_with_files_8_1P.fastq"')
			
		self.assertEqual(configFile.has_all_pair_files(), True)

		
if __name__ == "__main__":
	#import sys;sys.argv = ['', 'Test.testName']
	unittest.main()
	
