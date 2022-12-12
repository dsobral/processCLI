'''
Created on Oct 14, 2016

@author: mmp
'''
import unittest, os
from config.configFile import ConfigFile
from constants.utils import Util

### run command line
# export PYTHONPATH='/home/mmp/git/processCLI/src'
### IMPORTANT, need to be inside of 'tests' because of the paths
# cd tests/
# python3 -m unittest
class Test(unittest.TestCase):

	utils = Util()
	
	def setUp(self):
		self.temp_file = self.utils.get_temp_file("config", ".txt") 


	def tearDown(self):
		if os.path.exists(self.temp_file):
			os.unlink(self.temp_file)

	def _change_config_file(self, file_name_in):
		
		cmd = "sed 's-files/dir_with-{}/files/dir_with-' {} > {}".format(
			os.path.dirname(os.path.abspath(__file__)),
			file_name_in, self.temp_file )
		exist_status = os.system(cmd)
		if (exist_status != 0):
			self.assertFail("Fail to run cmd.\n{}".format(cmd))
		
	def testFile(self):
		WORKING_PATH_TEST = os.path.dirname(os.path.abspath(__file__))
		
		configFile = ConfigFile()
		self._change_config_file(os.path.join(os.path.dirname(os.path.abspath(__file__)), "files/config.txt"))
		configFile.read_file(self.temp_file)
		
		self.assertTrue(configFile.get_processors() == 2)
		self.assertTrue(configFile.get_output_path() == "outData")
		self.assertTrue(len(configFile.get_vect_cmd()) == 1)
		self.assertFalse(configFile.get_confirm_after_collect_data())
		self.assertEqual(configFile.get_vect_cmd()[0], "bash tests/cmd/process.sh OUT_FOLDER PREFIX_FILES_OUT FILE1 FILE2")
		self.assertEqual(len(configFile.get_vect_files_not_to_process()), 1)
		self.assertTrue(configFile.get_vect_files_not_to_process()[0].endswith("files/dir_with_files/Xpto2_A_L001_r1.fastq.gz"))
		self.assertEqual(len(configFile.get_vect_files_to_process()), 3)
		
		n_count = 0
		for files_to_process in configFile.get_vect_files_to_process():
			if (files_to_process.get_prefix_file_out() == "Xpto3_A"):
				n_count += 1
				self.assertEqual(files_to_process.get_file1(),
					os.path.join(os.path.dirname(os.path.abspath(__file__)), "files/dir_with_files/Xpto3_A_L001_r1.fastq.gz"))
				self.assertEqual(files_to_process.get_file2(),
					os.path.join(os.path.dirname(os.path.abspath(__file__)), "files/dir_with_files/Xpto3_A_L001_r2.fastq"))
				self.assertEqual(files_to_process.get_command_line(configFile.get_output_path(), configFile.get_vect_cmd()[0]), 
						'bash tests/cmd/process.sh {}/outData/ '.format(WORKING_PATH_TEST) +\
						'Xpto3_A "{}/files/dir_with_files/Xpto3_A_L001_r1.fastq.gz" '.format(WORKING_PATH_TEST) +\
						'"{}/files/dir_with_files/Xpto3_A_L001_r2.fastq"'.format(WORKING_PATH_TEST))
			if (files_to_process.get_prefix_file_out() == "Xpto_A"):
				n_count += 1
				self.assertEqual(files_to_process.get_file1(),
					os.path.join(os.path.dirname(os.path.abspath(__file__)), "files/dir_with_files/Xpto_A_L001_r1.fastq.gz"))
				self.assertEqual(files_to_process.get_file2(),
					os.path.join(os.path.dirname(os.path.abspath(__file__)), "files/dir_with_files/Xpto_A_L001_r2.fastq.gz"))
		self.assertEqual(n_count, 2)


	
	def testFile_5(self):
		WORKING_PATH_TEST_51 = os.path.dirname(os.path.abspath(__file__))
		
		configFile = ConfigFile()
		self._change_config_file(os.path.join(WORKING_PATH_TEST_51, "files/config5.txt"))
		configFile.read_file(self.temp_file)
			
		self.assertTrue(configFile.get_processors() == 2)
		self.assertTrue(configFile.get_output_path() == "outData")
		self.assertTrue(len(configFile.get_vect_cmd()) == 1)
		self.assertFalse(configFile.get_confirm_after_collect_data())
		self.assertEqual(configFile.get_vect_cmd()[0], "bash tests/cmd/process.sh OUT_FOLDER PREFIX_FILES_OUT FILE1 FILE2")
		self.assertEqual(len(configFile.get_vect_files_not_to_process()), 0)
		self.assertEqual(len(configFile.get_vect_files_to_process()), 1)
		
		self.assertEqual(configFile.get_vect_files_to_process()[0].get_prefix_file_out(), "Xpto3_A_L001")
		self.assertTrue(configFile.get_vect_files_to_process()[0].get_file1().endswith(
			"files/dir_with_files_9/Xpto3_A_L001_1.fastq"))
		self.assertTrue(configFile.get_vect_files_to_process()[0].get_file2().endswith(
			"files/dir_with_files_9/Xpto3_A_L001_2.fastq"))
		self.assertEqual(configFile.get_vect_files_to_process()[0].get_command_line(configFile.get_output_path(), configFile.get_vect_cmd()[0]), 
					'bash tests/cmd/process.sh {}/outData/ '.format(WORKING_PATH_TEST_51) +\
					'Xpto3_A_L001 "{}/files/dir_with_files_9/Xpto3_A_L001_1.fastq" '.format(WORKING_PATH_TEST_51) +\
					'"{}/files/dir_with_files_9/Xpto3_A_L001_2.fastq"'.format(WORKING_PATH_TEST_51))
		
	
	def testFile51(self):
		WORKING_PATH_TEST_51 = os.path.dirname(os.path.abspath(__file__))

		configFile = ConfigFile()
		self._change_config_file(os.path.join(os.path.dirname(os.path.abspath(__file__)), "files/config51.txt"))
		configFile.read_file(self.temp_file)
			
		self.assertTrue(configFile.get_processors() == 2)
		self.assertTrue(configFile.get_output_path() == "outData")
		self.assertTrue(len(configFile.get_vect_cmd()) == 1)
		self.assertFalse(configFile.get_confirm_after_collect_data())
		self.assertEqual(configFile.get_vect_cmd()[0], "bash tests/cmd/process.sh OUT_FOLDER PREFIX_FILES_OUT FILE1 FILE2")
		self.assertEqual(len(configFile.get_vect_files_not_to_process()), 0)
		self.assertEqual(len(configFile.get_vect_files_to_process()), 2)
		
		self.assertEqual(configFile.get_vect_files_to_process()[0].get_prefix_file_out(), "Xpto31_A_L001")
		self.assertEqual(configFile.get_vect_files_to_process()[0].get_file1(),
			os.path.join(os.path.dirname(os.path.abspath(__file__)), "files/dir_test_outputpath/fastq/Xpto31_A_L001_1P.fastq"))
		self.assertEqual(configFile.get_vect_files_to_process()[0].get_file2(),
			os.path.join(os.path.dirname(os.path.abspath(__file__)), "files/dir_test_outputpath/fastq/Xpto31_A_L001_2P.fastq"))
		self.assertEqual(configFile.get_vect_files_to_process()[0].get_command_line(configFile.get_output_path(), configFile.get_vect_cmd()[0]), 
					'bash tests/cmd/process.sh {}/outData/ Xpto31_A_L001 "{}/files/dir_test_outputpath/fastq/Xpto31_A_L001_1P.fastq" '.format(
						WORKING_PATH_TEST_51, WORKING_PATH_TEST_51) +\
					'"{}/files/dir_test_outputpath/fastq/Xpto31_A_L001_2P.fastq"'.format(WORKING_PATH_TEST_51))
		self.assertEqual(configFile.get_vect_files_to_process()[1].get_command_line(configFile.get_output_path(), configFile.get_vect_cmd()[0]), 
					'bash tests/cmd/process.sh {}/outData/input Xpto3_A_L001 "{}/files/dir_test_outputpath/fastq/input/Xpto3_A_L001_1P.fastq" '.format(
						WORKING_PATH_TEST_51, WORKING_PATH_TEST_51) +\
					'"{}/files/dir_test_outputpath/fastq/input/Xpto3_A_L001_2P.fastq"'.format(WORKING_PATH_TEST_51))
		
		
	def testFile1(self):
		configFile = ConfigFile()
		try:
			self._change_config_file(os.path.join(os.path.dirname(os.path.abspath(__file__)), "files/config2_fail.txt"))
			configFile.read_file(self.temp_file)
		except Exception as e:
			self.assertEqual(e.args[0], "Error: the value 'Output Path' can't be empty")
			return
		self.fail("Must raise an error")
			
	def testFile2(self):
		configFile = ConfigFile()
		try:
			self._change_config_file(os.path.join(os.path.dirname(os.path.abspath(__file__)), "files/config3_fail.txt"))
			configFile.read_file(self.temp_file)
		except Exception as e:
			self.assertEqual(e.args[0], "Error: the value 'Command line to process cmd=' can't be empty")
			return
		self.fail("Must raise an ValueError exception on processors")
				
	def testFile3(self):
		configFile = ConfigFile()
		try:
			self._change_config_file(os.path.join(os.path.dirname(os.path.abspath(__file__)), "files/config4_fail.txt"))
			configFile.read_file(self.temp_file)
		except Exception as e:
			self.assertEqual(e.args[0], "Must have the 'InputDirectories' tag followed by directories that contain files")
			return
		self.fail("Must raise an Exception with InputDirectory")
				
	def testFile4(self):
		configFile = ConfigFile()
		try:
			self._change_config_file(os.path.join(os.path.dirname(os.path.abspath(__file__)), "files/config5_fail.txt"))
			configFile.read_file(self.temp_file)
		except Exception as e:
			self.assertEqual(e.args[0], "Must have files to process. Insert directories after the tag 'InputDirectories' in the config file")
			return
		self.fail("Must raise an Exception on files to process")
	
	def testFile5(self):
		configFile = ConfigFile()
		WORKING_PATH_TEST = os.path.dirname(os.path.abspath(__file__))
		try:
			self._change_config_file(os.path.join(os.path.dirname(os.path.abspath(__file__)), "files/config6_fail.txt"))
			configFile.read_file(self.temp_file)
	
		except Exception as e:
			self.assertEqual(e.args[0], "Error: this directory doesn't exist: {}/files/dir_with_files_fail_xpto".format(WORKING_PATH_TEST))
			return
		self.fail("Must raise an ValueError on errors")	
	
	def testFile6(self):
		configFile = ConfigFile()
		WORKING_PATH_TEST = os.path.dirname(os.path.abspath(__file__))
		try:
			self._change_config_file(os.path.join(os.path.dirname(os.path.abspath(__file__)), "files/config7_fail.txt"))
			configFile.read_file(self.temp_file)
		except Exception as e:
			self.assertEqual(e.args[0], "Error: the file 'Xpto3_A_L001_r2.fastq.gz' exist more than on time in the directory, or in sub-directories " +\
							"'{}/files/dir_with_files_fail'".format(WORKING_PATH_TEST))
			return
		self.fail("Must raise an error")
	
	def testFile7(self):
		WORKING_PATH_TEST = os.path.dirname(os.path.abspath(__file__))
		
		configFile = ConfigFile()
		self._change_config_file(os.path.join(os.path.dirname(os.path.abspath(__file__)), "files/config8_fail.txt"))
		configFile.read_file(self.temp_file)
		self.assertEqual(len(configFile.get_vect_files_not_to_process()), 1)
		self.assertEqual(configFile.get_vect_files_not_to_process()[0],
				"{}/files/dir_with_files_fail_2/file.fastq".format(WORKING_PATH_TEST))
			
	def testFile8(self):
		configFile = ConfigFile()
		WORKING_PATH_TEST = os.path.dirname(os.path.abspath(__file__))
		
		self._change_config_file(os.path.join(os.path.dirname(os.path.abspath(__file__)), "files/config9.txt"))
		configFile.read_file(self.temp_file)
		self.assertEqual(len(configFile.get_vect_files_not_to_process()), 1)
		self.assertTrue(configFile.get_vect_files_not_to_process()[0].endswith(
			"files/dir_with_files_1/Xpto2_A.txt"))
		self.assertTrue(configFile.get_confirm_after_collect_data())
		self.assertEqual(len(configFile.get_vect_files_to_process()), 4)
		n_count = 0
		for files_to_process in configFile.get_vect_files_to_process():
			if (files_to_process.get_prefix_file_out() == "Treponema_A_L001"):
				n_count += 1
				self.assertTrue(files_to_process.get_file1().endswith("files/dir_with_files_1/Treponema_A_L001.fastq.gz"))
				self.assertEqual(files_to_process.get_file2(), "")
			elif (files_to_process.get_prefix_file_out() == "Xpto_A_L001"):
				n_count += 1
				self.assertTrue(files_to_process.get_file1().endswith("files/dir_with_files_1/Xpto_A_L001.fastq.gz"))
				self.assertEqual(files_to_process.get_file2(), "")
			elif (files_to_process.get_prefix_file_out() == "Xpto_B"):
				n_count += 1
				self.assertTrue(files_to_process.get_file1().endswith("files/dir_with_files_1/Xpto_B.fastq"))
				self.assertEqual(files_to_process.get_file2(), "")
			elif (files_to_process.get_prefix_file_out() == "Xpto2_A"):
				n_count += 1
				self.assertTrue(files_to_process.get_file1().endswith("files/dir_with_files_1/Xpto2_A.fastq.gz"))
				self.assertEqual(files_to_process.get_file2(), "")
		self.assertEqual(n_count, 4)

	def testFile9(self):
		configFile = ConfigFile()
		self._change_config_file(os.path.join(os.path.dirname(os.path.abspath(__file__)), "files/config2.txt"))
		configFile.read_file(self.temp_file)
		self.assertEqual(len(configFile.get_vect_files_not_to_process()), 1)
		self.assertTrue(configFile.get_vect_files_not_to_process()[0].endswith("files/dir_with_files_2/Xpto2_A.txt"))
		self.assertEqual(len(configFile.get_vect_files_to_process()), 2)
		if (configFile.get_vect_files_to_process()[1].get_prefix_file_out() == "Xpto_B"):
			self.assertTrue(configFile.get_vect_files_to_process()[1].get_file1().endswith("files/dir_with_files_2/Xpto_B.fastq"))
			self.assertEqual(configFile.get_vect_files_to_process()[1].get_file2(), "")
			self.assertTrue(configFile.get_vect_files_to_process()[0].get_file1().endswith("files/dir_with_files_2/Xpto2_A.fastq.gz"))
			self.assertEqual(configFile.get_vect_files_to_process()[0].get_file2(), "")
		else:
			self.assertTrue(configFile.get_vect_files_to_process()[0].get_file1().endswith("files/dir_with_files_2/Xpto_B.fastq"))
			self.assertEqual(configFile.get_vect_files_to_process()[0].get_file2(), "")
			self.assertTrue(configFile.get_vect_files_to_process()[1].get_file1().endswith("files/dir_with_files_2/Xpto2_A.fastq.gz"))
			self.assertEqual(configFile.get_vect_files_to_process()[1].get_file2(), "")

	def testFile10(self):
		configFile = ConfigFile()
		self._change_config_file(os.path.join(os.path.dirname(os.path.abspath(__file__)), "files/config3.txt"))
		configFile.read_file(self.temp_file)
		self.assertEqual(len(configFile.get_vect_files_not_to_process()), 1)
		self.assertTrue(configFile.get_vect_files_not_to_process()[0].endswith("files/dir_with_files_2/Xpto2_A.txt"))
		self.assertEqual(len(configFile.get_vect_files_to_process()), 2)
		if (configFile.get_vect_files_to_process()[0].get_prefix_file_out() == "Xpto_B"):
			self.assertTrue(configFile.get_vect_files_to_process()[0].get_file1().endswith("files/dir_with_files_2/Xpto_B.fastq"))
			self.assertEqual(configFile.get_vect_files_to_process()[0].get_file2(), "")
			self.assertTrue(configFile.get_vect_files_to_process()[1].get_file1().endswith("files/dir_with_files_2/Xpto2_A.fastq.gz"))
			self.assertEqual(configFile.get_vect_files_to_process()[1].get_file2(), "")
		else:
			self.assertTrue(configFile.get_vect_files_to_process()[1].get_file1().endswith("files/dir_with_files_2/Xpto_B.fastq"))
			self.assertEqual(configFile.get_vect_files_to_process()[1].get_file2(), "")
			self.assertTrue(configFile.get_vect_files_to_process()[0].get_file1().endswith("files/dir_with_files_2/Xpto2_A.fastq.gz"))
			self.assertEqual(configFile.get_vect_files_to_process()[0].get_file2(), "")
		self.assertEqual(configFile.get_extensions_to_look(), ".fq.gz; .fq; .fastq.gz; .fastq; .fasta.gz; .fasta; .fa; .fa.gz")
		
	def testFile11(self):
		configFile = ConfigFile()
		try:
			self._change_config_file(os.path.join(os.path.dirname(os.path.abspath(__file__)), "files/config4.txt"))
			configFile.read_file(self.temp_file)
		except Exception as e:
			self.assertEqual(e.args[0], "You have files but you have the flag 'expecting_all_paired_files=' yes. Please, check if you expect paired files.")
			return
		self.fail("Must raise an error")
	
	def testFile12(self):
		configFile = ConfigFile()
		self._change_config_file(os.path.join(os.path.dirname(os.path.abspath(__file__)), "files/config10.txt"))
		configFile.read_file(self.temp_file)
		self.assertEqual(len(configFile.get_vect_files_not_to_process()), 1)
		self.assertEqual(len(configFile.get_vect_files_to_process()), 1)
		self.assertTrue(configFile.get_vect_files_to_process()[0].get_file1().endswith("files/dir_with_files_4/Xpto3_A_L001_1P.fastq"))
		self.assertTrue(configFile.get_vect_files_to_process()[0].get_file2().endswith("files/dir_with_files_4/Xpto3_A_L001_2P.fastq"))
		self.assertEqual(configFile.get_extensions_to_look(), ".fq.gz; .fq; .fastq.gz; .fastq; .fasta.gz; .fasta; .fa; .fa.gz")
		
	def testFile12_11(self):
		configFile = ConfigFile()
		self._change_config_file(os.path.join(os.path.dirname(os.path.abspath(__file__)), "files/config11.txt"))
		configFile.read_file(self.temp_file)
		self.assertEqual(len(configFile.get_vect_files_not_to_process()), 1)
		self.assertTrue(configFile.get_vect_files_not_to_process()[0].endswith("files/dir_with_files_6/temp2.txt"))
		self.assertEqual(len(configFile.get_vect_files_to_process()), 2)
		if (configFile.get_vect_files_to_process()[0].get_prefix_file_out() == "Xpto3_A_L001"):
			self.assertTrue(configFile.get_vect_files_to_process()[0].get_file1().endswith("files/dir_with_files_6/Xpto3_A_L001_1P.fastq"))
			self.assertTrue(configFile.get_vect_files_to_process()[0].get_file2().endswith("files/dir_with_files_6/Xpto3_A_L001_2P.fastq"))
			self.assertEqual(configFile.get_vect_files_to_process()[0].get_prefix_file_out(), "Xpto3_A_L001")
			self.assertTrue(configFile.get_vect_files_to_process()[1].get_file1().endswith("files/dir_with_files_6/Xpto31_A_L001_1P.fastq"))
			self.assertTrue(configFile.get_vect_files_to_process()[1].get_file2().endswith("files/dir_with_files_6/Xpto31_A_L001_2P.fastq"))
			self.assertEqual(configFile.get_vect_files_to_process()[1].get_prefix_file_out(), "Xpto31_A_L001")
		else:
			self.assertTrue(configFile.get_vect_files_to_process()[1].get_file1().endswith("files/dir_with_files_6/Xpto3_A_L001_1P.fastq"))
			self.assertTrue(configFile.get_vect_files_to_process()[1].get_file2().endswith("files/dir_with_files_6/Xpto3_A_L001_2P.fastq"))
			self.assertEqual(configFile.get_vect_files_to_process()[1].get_prefix_file_out(), "Xpto3_A_L001")
			self.assertTrue(configFile.get_vect_files_to_process()[0].get_file1().endswith("files/dir_with_files_6/Xpto31_A_L001_1P.fastq"))
			self.assertTrue(configFile.get_vect_files_to_process()[0].get_file2().endswith("files/dir_with_files_6/Xpto31_A_L001_2P.fastq"))
			self.assertEqual(configFile.get_vect_files_to_process()[0].get_prefix_file_out(), "Xpto31_A_L001")
	
	def testFile11_11(self):
		configFile = ConfigFile()
		self._change_config_file(os.path.join(os.path.dirname(os.path.abspath(__file__)), "files/config17.txt"))
		configFile.read_file(self.temp_file)
		self.assertEqual(len(configFile.get_vect_files_not_to_process()), 0)
		self.assertEqual(len(configFile.get_vect_files_to_process()), 3)
		vect_prefix_out_expected = sorted(["T0_CA_R1", "T0_ITR1_R2", "T0_ITR2_R2"])
		vect_prefix_out = sorted([configFile.get_vect_files_to_process()[_].get_prefix_file_out() for \
					_ in range(len(configFile.get_vect_files_to_process()))])
		self.assertEqual(vect_prefix_out_expected, vect_prefix_out)
			
	def testFile12_12(self):
		configFile = ConfigFile()
		self._change_config_file(os.path.join(os.path.dirname(os.path.abspath(__file__)), "files/config12.txt"))
		configFile.read_file(self.temp_file)
		self.assertEqual(len(configFile.get_vect_files_not_to_process()), 2)
		self.assertTrue(configFile.get_vect_files_not_to_process()[0].endswith("files/dir_with_files_5/Xpto3_A_L001_1P.fastq"))
		self.assertTrue(configFile.get_vect_files_not_to_process()[1].endswith("files/dir_with_files_5/Xpto3_A_L001_2P.fastq"))
		self.assertEqual(len(configFile.get_vect_files_to_process()), 1)
		self.assertTrue(configFile.get_vect_files_to_process()[0].get_file1().endswith("files/dir_with_files_5/temp2.txt"))
		self.assertEqual(configFile.get_vect_files_to_process()[0].get_file2(), "")
		self.assertEqual(configFile.get_vect_files_to_process()[0].get_prefix_file_out(), "temp2")
		self.assertEqual(configFile.get_extensions_to_look(), ".txt")

	def testFile12_13(self):
		configFile = ConfigFile()
		self._change_config_file(os.path.join(os.path.dirname(os.path.abspath(__file__)), "files/config13.txt"))
		configFile.read_file(self.temp_file)
		self.assertEqual(len(configFile.get_vect_files_not_to_process()), 2)
		self.assertTrue(configFile.get_vect_files_not_to_process()[0].endswith("files/dir_with_files_7/temp2.txt"))
		self.assertTrue(configFile.get_vect_files_not_to_process()[1].endswith("files/dir_with_files_7/Xpto32_A_L001_2P.fastq"))
		self.assertEqual(len(configFile.get_vect_files_to_process()), 2)
		if (configFile.get_vect_files_to_process()[0].get_prefix_file_out() == "Xpto3_A_L001"):
			self.assertTrue(configFile.get_vect_files_to_process()[0].get_file1().endswith("files/dir_with_files_7/Xpto3_A_L001_1P.fastq"))
			self.assertTrue(configFile.get_vect_files_to_process()[0].get_file2().endswith("files/dir_with_files_7/Xpto3_A_L001_2P.fastq"))
			self.assertEqual(configFile.get_vect_files_to_process()[0].get_prefix_file_out(), "Xpto3_A_L001")
			self.assertTrue(configFile.get_vect_files_to_process()[1].get_file1().endswith("files/dir_with_files_7/Xpto31_A_L001_1P.fastq"))
			self.assertTrue(configFile.get_vect_files_to_process()[1].get_file2().endswith("files/dir_with_files_7/Xpto31_A_L001_2P.fastq"))
			self.assertEqual(configFile.get_vect_files_to_process()[1].get_prefix_file_out(), "Xpto31_A_L001")
		else:
			self.assertTrue(configFile.get_vect_files_to_process()[1].get_file1().endswith("files/dir_with_files_7/Xpto3_A_L001_1P.fastq"))
			self.assertTrue(configFile.get_vect_files_to_process()[1].get_file2().endswith("files/dir_with_files_7/Xpto3_A_L001_2P.fastq"))
			self.assertEqual(configFile.get_vect_files_to_process()[1].get_prefix_file_out(), "Xpto3_A_L001")
			self.assertTrue(configFile.get_vect_files_to_process()[0].get_file1().endswith("files/dir_with_files_7/Xpto31_A_L001_1P.fastq"))
			self.assertTrue(configFile.get_vect_files_to_process()[0].get_file2().endswith("files/dir_with_files_7/Xpto31_A_L001_2P.fastq"))
			self.assertEqual(configFile.get_vect_files_to_process()[0].get_prefix_file_out(), "Xpto31_A_L001")
		self.assertEqual(configFile.has_all_pair_files(), True)

	def testFile12_13_1(self):
		configFile = ConfigFile()
		self._change_config_file(os.path.join(os.path.dirname(os.path.abspath(__file__)), "files/config13_1.txt"))
		configFile.read_file(self.temp_file)
		self.assertEqual(len(configFile.get_vect_files_not_to_process()), 1)
		self.assertTrue(configFile.get_vect_files_not_to_process()[0].endswith("files/dir_with_files_7/temp2.txt"))
		self.assertEqual(len(configFile.get_vect_files_to_process()), 3)
		n_count = 0
		for files_to_process in configFile.get_vect_files_to_process():
			if (files_to_process.get_prefix_file_out() == "Xpto3_A_L001"):
				n_count += 1
				self.assertTrue(files_to_process.get_file1().endswith("files/dir_with_files_7/Xpto3_A_L001_1P.fastq"))
				self.assertTrue(files_to_process.get_file2().endswith("files/dir_with_files_7/Xpto3_A_L001_2P.fastq"))
			elif (files_to_process.get_prefix_file_out() == "Xpto31_A_L001"):
				n_count += 1
				self.assertTrue(files_to_process.get_file1().endswith("files/dir_with_files_7/Xpto31_A_L001_1P.fastq"))
				self.assertTrue(files_to_process.get_file2().endswith("files/dir_with_files_7/Xpto31_A_L001_2P.fastq"))
			elif (files_to_process.get_prefix_file_out() == "Xpto32_A_L001"):
				n_count += 1
				self.assertTrue(files_to_process.get_file1().endswith("files/dir_with_files_7/Xpto32_A_L001_2P.fastq"))
				self.assertEqual(files_to_process.get_file2(), "")
		self.assertEqual(configFile.has_all_pair_files(), False)
		self.assertEqual(n_count, 3)
				
	def testFile12_14(self):
		configFile = ConfigFile()
		self._change_config_file(os.path.join(os.path.dirname(os.path.abspath(__file__)), "files/config14.txt"))
		configFile.read_file(self.temp_file)
		self.assertEqual(len(configFile.get_vect_files_not_to_process()), 1)
		self.assertTrue(configFile.get_vect_files_not_to_process()[0].endswith("files/dir_with_files_6/temp2.txt"))
		self.assertEqual(len(configFile.get_vect_files_to_process()), 2)
		if (configFile.get_vect_files_to_process()[0].get_prefix_file_out() == "Xpto3_A_L001"):
			self.assertTrue(configFile.get_vect_files_to_process()[0].get_file1().endswith("files/dir_with_files_6/Xpto3_A_L001_1P.fastq"))
			self.assertTrue(configFile.get_vect_files_to_process()[0].get_file2().endswith("files/dir_with_files_6/Xpto3_A_L001_2P.fastq"))
			self.assertEqual(configFile.get_vect_files_to_process()[0].get_prefix_file_out(), "Xpto3_A_L001")
			self.assertTrue(configFile.get_vect_files_to_process()[1].get_file1().endswith("files/dir_with_files_6/Xpto31_A_L001_1P.fastq"))
			self.assertTrue(configFile.get_vect_files_to_process()[1].get_file2().endswith("files/dir_with_files_6/Xpto31_A_L001_2P.fastq"))
			self.assertEqual(configFile.get_vect_files_to_process()[1].get_prefix_file_out(), "Xpto31_A_L001")
		else:
			self.assertTrue(configFile.get_vect_files_to_process()[1].get_file1().endswith("files/dir_with_files_6/Xpto3_A_L001_1P.fastq"))
			self.assertTrue(configFile.get_vect_files_to_process()[1].get_file2().endswith("files/dir_with_files_6/Xpto3_A_L001_2P.fastq"))
			self.assertEqual(configFile.get_vect_files_to_process()[1].get_prefix_file_out(), "Xpto3_A_L001")
			self.assertTrue(configFile.get_vect_files_to_process()[0].get_file1().endswith("files/dir_with_files_6/Xpto31_A_L001_1P.fastq"))
			self.assertTrue(configFile.get_vect_files_to_process()[0].get_file2().endswith("files/dir_with_files_6/Xpto31_A_L001_2P.fastq"))
			self.assertEqual(configFile.get_vect_files_to_process()[0].get_prefix_file_out(), "Xpto31_A_L001")
		self.assertEqual(configFile.has_all_pair_files(), True)
		
		
	def testFile15(self):
		configFile = ConfigFile()
		
		## set environment variable
		os.environ['dir_with_files_variable'] = "dir_with_files_8"
		self._change_config_file(os.path.join(os.path.dirname(os.path.abspath(__file__)), "files/config15.txt"))
		configFile.read_file(self.temp_file)
		self.assertEqual(len(configFile.get_vect_files_not_to_process()), 0)
		self.assertEqual(len(configFile.get_vect_files_to_process()), 2)
		if (configFile.get_vect_files_to_process()[0].get_prefix_file_out() == "Xpto3_A_L001"):
			self.assertTrue(configFile.get_vect_files_to_process()[0].get_file1().endswith("files/dir_with_files_8/Xpto3_A_L001_1P.fastq"))
			self.assertTrue(configFile.get_vect_files_to_process()[0].get_file2().endswith("files/dir_with_files_8/Xpto3_A_L001_2P.fastq"))
			self.assertEqual(configFile.get_vect_files_to_process()[0].get_prefix_file_out(), "Xpto3_A_L001")
			self.assertTrue(configFile.get_vect_files_to_process()[1].get_file1().endswith("files/dir_with_files_8/Xpto31_A_L001_1P.fastq"))
			self.assertTrue(configFile.get_vect_files_to_process()[1].get_file2().endswith("files/dir_with_files_8/Xpto31_A_L001_2P.fastq"))
			self.assertEqual(configFile.get_vect_files_to_process()[1].get_prefix_file_out(), "Xpto31_A_L001")
		else:
			self.assertTrue(configFile.get_vect_files_to_process()[1].get_file1().endswith("files/dir_with_files_8/Xpto3_A_L001_1P.fastq"))
			self.assertTrue(configFile.get_vect_files_to_process()[1].get_file2().endswith("files/dir_with_files_8/Xpto3_A_L001_2P.fastq"))
			self.assertEqual(configFile.get_vect_files_to_process()[1].get_prefix_file_out(), "Xpto3_A_L001")
			self.assertTrue(configFile.get_vect_files_to_process()[0].get_file1().endswith("files/dir_with_files_8/Xpto31_A_L001_1P.fastq"))
			self.assertTrue(configFile.get_vect_files_to_process()[0].get_file2().endswith("files/dir_with_files_8/Xpto31_A_L001_2P.fastq"))
			self.assertEqual(configFile.get_vect_files_to_process()[0].get_prefix_file_out(), "Xpto31_A_L001")
		self.assertEqual(configFile.has_all_pair_files(), True)
		
	def testFile16(self):
		WORKING_PATH_TEST = os.path.dirname(os.path.abspath(__file__))
		configFile = ConfigFile()
		
		## set environment variable
		os.environ['dir_with_files_variable'] = "dir_with_files_8"
		self._change_config_file(os.path.join(os.path.dirname(os.path.abspath(__file__)), "files/config16.txt"))
		configFile.read_file(self.temp_file)
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
			
			self.assertEqual(len(configFile.get_vect_cmd()), 2)
			self.assertEqual(len(configFile.get_vect_cmd_one_file()), 0)
			self.assertEqual(len(configFile.get_vect_cmd_two_files()), 0)
			
			self.assertEqual(configFile.get_vect_files_to_process()[0].get_command_line(\
				configFile.get_output_path(), configFile.get_vect_cmd()[0]),\
				'bash tests/cmd/process.sh --outdir {}/outData/dir_with_files_8 --prefix Xpto3_A_L001 '.format(WORKING_PATH_TEST) +\
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
			
			self.assertEqual(len(configFile.get_vect_cmd()), 2)
			self.assertEqual(len(configFile.get_vect_cmd_one_file()), 0)
			self.assertEqual(len(configFile.get_vect_cmd_two_files()), 0)
			
			self.assertEqual(configFile.get_vect_files_to_process()[0].get_command_line(\
				configFile.get_output_path(), configFile.get_vect_cmd()[0]),\
				'bash tests/cmd/process.sh --outdir {}/outData/dir_with_files_8 --prefix Xpto31_A_L001 '.format(WORKING_PATH_TEST) +\
				'--file1 "files/dir_with_files_8/Xpto31_A_L001_1P.fastq" "files/dir_with_files_8/dir_with_files_8_1P.fastq"')
			
		self.assertEqual(configFile.has_all_pair_files(), True)

	def testFile_20(self):
		
		configFile = ConfigFile()
		self._change_config_file(os.path.join(os.path.dirname(os.path.abspath(__file__)), "files/config_20.txt"))
		configFile.read_file(self.temp_file)
		
		self.assertTrue(configFile.get_processors() == 2)
		self.assertTrue(configFile.get_output_path() == "outData")
		self.assertEqual(1, len(configFile.get_vect_cmd()))
		self.assertTrue(configFile.get_confirm_after_collect_data())
		self.assertEqual(configFile.get_vect_cmd()[0], "bash tests/cmd/process.sh OUT_FOLDER PREFIX_FILES_OUT FILE1 FILE2")
		self.assertEqual(len(configFile.get_vect_files_not_to_process()), 2)
		self.assertTrue(configFile.get_vect_files_not_to_process()[0].endswith("files/dir_files_10/631_EX1_unpair.fastq.gz"))
		self.assertEqual(len(configFile.get_vect_files_to_process()), 2)
		
if __name__ == "__main__":
	#import sys;sys.argv = ['', 'Test.testName']
	unittest.main()
	
