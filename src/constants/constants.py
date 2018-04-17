'''
Created on Oct 15, 2016

@author: mmp
'''

class Constants(object):
	'''
	classdocs
	'''

	vect_ambigous = ['R', 'Y', 'K', 'M', 'S', 'W', 'B', 'D', 'H', 'V', 'N', '*']
	dt_ambigous = { 'R':'[AG]', 'Y':'[TC]', 'K':'[GT]', 'M':'[AC]', 'S':'[GC]', 
			'W':'[AT]', 'B':'[CGT]', 'D':'[AGT]', 'H':'[ACT]', 'V':'[ACG]',
			'N':'[ACGT]', '*':'.' }
	dict_complement = {'A': 'T', 'C': 'G', 'G': 'C', 'T': 'A',
					'R': 'Y', 
					'Y': 'R', 
					'K': 'M', 
					'M': 'K', 
					'S': 'S', 
					'W': 'W', 
					'B': 'V', 
					'D': 'H',
					'H': 'D',
					'V': 'B',
					'N': 'N'}

	def __init__(self):
		'''
		Constructor
		'''
		pass
	
	
	### complement
	def complement(self, seq):  
		complseq = [self.dict_complement[base] if base in self.dict_complement else base for base in seq]  
		return ''.join(complseq)
	
	#reverse
	def reverse_complement(self, seq):  
		seq = list(seq)  
		seq.reverse()   
		return self.complement(''.join(seq))
	
	
	###
	def ambiguos_to_unambiguous(self, sequence):
		for ambig in self.vect_ambigous:
			sequence = sequence.replace(ambig, self.dt_ambigous[ambig])
		#print sequence
		return sequence
