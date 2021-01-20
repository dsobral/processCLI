'''
Created on Nov 1, 2016

@author: mmp
'''
import unittest
from config.configFile import FileToProcess, ConfigFile
from constants.utils import Util

class Test(unittest.TestCase):


	def testFileToProcess(self):
		fileToProcess = FileToProcess("fie_r1_temp", "fie_r2_temp", "temp", 3, ".fastq.gz", "fastq.gz", "")
		self.assertEqual(fileToProcess.get_file1(), "fie_r1_temp")
		self.assertEqual(fileToProcess.get_file2(), "fie_r2_temp")
		self.assertEqual(fileToProcess.get_prefix_file_out(), "temp")
		self.assertEqual(fileToProcess.extension_1, ".fastq.gz")
		self.assertEqual(fileToProcess.extension_2, "fastq.gz")

		fileToProcess = FileToProcess("fie_r2_temp", "fie_r1_temp", "temp", 3, ".fastq.gz", ".fastq.gz", "")
		self.assertEqual(fileToProcess.get_file1(), "fie_r1_temp")
		self.assertEqual(fileToProcess.get_file2(), "fie_r2_temp")


	def testNumberFile1(self):
		util = Util()
		self.assertEquals(util.get_number_file("sddsffdf_2.fddf"), 2)
		self.assertEquals(util.get_number_file("sddsffdf_21.fddf"), 21)
		self.assertEquals(util.get_number_file("sddsffdf_1.fddf"), 1)
		self.assertEquals(util.get_number_file("sddsffdf_1_2.fddf"), 2)
		self.assertEquals(util.get_number_file("sddsffdf_r2.fddf"), 2)
		self.assertEquals(util.get_number_file("sddsffdf_r2_0.fddf"), 0)
		self.assertEquals(util.get_number_file("sddsffdf_r12_2.fddf"), 2)
		self.assertEquals(util.get_number_file("sddsffdf_r12_2_xpto.fddf"), 2)
		self.assertEquals(util.get_number_file("sddsffdf_r12_2_.fddf"), 2)
		self.assertEquals(util.get_number_file("sddsffdf_r12_.fddf"), 12)
		try:
			self.assertEquals(util.get_number_file("sddsffdf_r2fddf"), 2)
		except Exception as e:
			self.assertEqual(e.args[0], "Error can't find the number of the file 'sddsffdf_r2fddf'")
			return 
		self.fail("Must raise a error for file name 'sddsffdf_r2fddf'")

	def test_get_prefix_file_name(self):
		
		config_file = ConfigFile()
		self.assertEquals("sddsffdf", config_file.get_prefix_file_name("sddsffdf_2.fddf"))
		self.assertEquals("sddsffdf", config_file.get_prefix_file_name("sddsffdf_L2_R1_1.fddf"))
		self.assertEquals("sddsffdf_r2", config_file.get_prefix_file_name("sddsffdf_r2_0.fddf"))
		self.assertEquals("sddsffdf_r12", config_file.get_prefix_file_name("sddsffdf_r12_2_xpto.fddf"))
		self.assertEquals("sddsffdf_1", config_file.get_prefix_file_name("sddsffdf_1_2.fddf"))
		self.assertEquals("sddsffdf_1", config_file.get_prefix_file_name("sddsffdf_1_2_.fddf"))
		self.assertEquals("sddsffdf", config_file.get_prefix_file_name("sddsffdf_r12_.fddf"))
		self.assertEquals("sddsffdf_r12", config_file.get_prefix_file_name("sddsffdf_r12_2.fddf"))
		
		
		
		
if __name__ == "__main__":
	#import sys;sys.argv = ['', 'Test.testName']
	unittest.main()