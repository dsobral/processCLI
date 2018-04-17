'''
Created on Oct 15, 2016

@author: mmp
'''
import unittest
from src.constants.constants import Constants 

class Test(unittest.TestCase):


	def testConstants(self):
		
		constants = Constants()
		self.assertEqual(constants.complement("AAATTTCCC"), "TTTAAAGGG", "must be equal")
		self.assertEqual(constants.complement("AAATTGGGTCCC"), "TTTAACCCAGGG", "must be equal")
		self.assertEqual(constants.reverse_complement("AAGGGATTTCCC"), "GGGAAATCCCTT", "must be equal")
		self.assertEqual(constants.reverse_complement("AAATTAGTCCC"), "GGGACTAATTT", "must be equal")
		self.assertEqual(constants.ambiguos_to_unambiguous("YARWATTTCCC"), "[TC]A[AG][AT]ATTTCCC", "must be equal")
		self.assertEqual(constants.ambiguos_to_unambiguous("RYKMSWBDHVN"), "[AG][TC][GT][AC][GC][AT][CGT][AGT][ACT][ACG][ACGT]", "must be equal")
		self.assertEqual(constants.complement("RYKMSWBDHVN"), "YRMKSWVHDBN", "must be equal")

if __name__ == "__main__":
	#import sys;sys.argv = ['', 'Test.testConstants']
	unittest.main()