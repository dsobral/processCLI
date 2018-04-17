'''
Created on Nov 1, 2016

@author: mmp
'''
import unittest
from src.config.configFile import FileToProcess
from src.constants.utils import Util

class Test(unittest.TestCase):


	def testFileToProcess(self):
		fileToProcess = FileToProcess("fie_r1_temp", "fie_r2_temp", "temp", 3, ".fastq.gz", "fastq.gz", True)
		self.assertEqual(fileToProcess.get_file1(), "fie_r1_temp")
		self.assertEqual(fileToProcess.get_file2(), "fie_r2_temp")
		self.assertEqual(fileToProcess.get_prefix_file_out(), "temp")
		self.assertEqual(fileToProcess.extension_1, ".fastq.gz")
		self.assertEqual(fileToProcess.extension_2, "fastq.gz")
		self.assertEqual(fileToProcess.replace_file_name_by_folder_name, True)

		fileToProcess = FileToProcess("fie_r2_temp", "fie_r1_temp", "temp", 3, ".fastq.gz", ".fastq.gz", False)
		self.assertEqual(fileToProcess.get_file1(), "fie_r1_temp")
		self.assertEqual(fileToProcess.get_file2(), "fie_r2_temp")
		self.assertEqual(fileToProcess.replace_file_name_by_folder_name, False)


	def testNumberFile1(self):
		util = Util()
		self.assertEquals(util.get_number_file("sddsffdf_r2.fddf"), 2)
		self.assertEquals(util.get_number_file("sddsffdf_r2_00.fddf"), 2)
		self.assertEquals(util.get_number_file("sddsffdf_r12_00.fddf"), 12)
		try:
			self.assertEquals(util.get_number_file("sddsffdf_r2fddf"), 2)
		except Exception as e:
			self.assertEqual(e.args[0], "Error can't find the number of the file 'sddsffdf_r2fddf'")
			return 
		self.fail("Must raise a error for file name 'sddsffdf_r2fddf'")

if __name__ == "__main__":
	#import sys;sys.argv = ['', 'Test.testName']
	unittest.main()